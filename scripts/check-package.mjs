#!/usr/bin/env node
// Security gate for the sideload zip. The release workflow publishes the zip only if this passes.
// Checks: only allowed files, manifest at the root with required keys, no network or store APIs in code,
// no secret-looking strings anywhere, size limit.
//   node scripts/check-package.mjs [zip] [config.json]
// A config may list allowedUrls (prefixes): then code may contain http(s) URLs, but only ones starting with those.
import { readFileSync } from 'node:fs';
import { extname, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { readZip } from './zip.mjs';
import { ROOT, CONFIG, loadConfig } from './build.mjs';

function regex(src) {
  // Allow a leading (?i) for case-insensitive patterns in the JSON config.
  return src.startsWith('(?i)') ? new RegExp(src.slice(4), 'i') : new RegExp(src);
}

// Every URL-looking thing (any scheme, any case) must start with an allowed prefix exactly, with no path tricks
// (.., %-escapes, @, backslashes), and no scheme may be split across strings ("https:" + "//...").
// Limit: this is a text scan. Code that assembles a URL from pieces ("https" + Chr(58) + ...) can't be caught here;
// that is what code review is for.
export function urlProblems(name, text, allowed) {
  const out = [];
  for (const [url] of text.matchAll(/[a-z][a-z0-9+.-]*:\/\/[^\s"'<>]*/gi)) {
    if (!allowed.some((p) => url.startsWith(p))) out.push(`${name}: URL not on the allowlist: ${url}`);
    else if (/\.\.|%|@|\\/.test(url)) out.push(`${name}: URL has a path trick: ${url}`);
  }
  for (const [hit] of text.matchAll(/\bhttps?:(?!\/\/)/gi)) out.push(`${name}: split URL scheme (${hit})`);
  return out;
}

export function checkZip(buf, cfg = CONFIG) {
  const problems = [];
  if (buf.length > cfg.maxBytes) problems.push(`zip is ${buf.length} bytes, over ${cfg.maxBytes}`);
  const entries = readZip(buf);
  const names = entries.map((e) => e.name);
  if (!names.includes('manifest')) problems.push('manifest missing from zip root');
  if (!names.some((n) => /^source\/main\.brs$/.test(n))) problems.push('source/main.brs missing');
  const secrets = cfg.secretPatterns.map(regex);
  for (const { name, data } of entries) {
    if (name.includes('..') || name.startsWith('/')) problems.push(`${name}: unsafe path`);
    const top = name.split('/')[0];
    if (!cfg.include.includes(top)) problems.push(`${name}: not in an allowed folder`);
    if (name !== 'manifest' && !cfg.allowedExtensions.includes(extname(name))) problems.push(`${name}: file type not allowed`);
    if (name.split('/').some((part) => part.startsWith('.'))) problems.push(`${name}: hidden file`);
    const text = data.toString('latin1');
    for (const re of secrets) if (re.test(text)) problems.push(`${name}: looks like a secret (${re.source})`);
    const isCode = name === 'manifest' || ['.brs', '.xml', '.json'].includes(extname(name));
    if (isCode) {
      // BrightScript is case-insensitive, so match banned words regardless of case.
      const lower = text.toLowerCase();
      for (const word of cfg.forbiddenCode) if (lower.includes(word.toLowerCase())) problems.push(`${name}: uses ${word} (the app makes no network calls of its own)`);
      if (cfg.allowedUrls) {
        problems.push(...urlProblems(name, text, cfg.allowedUrls));
        if (name.endsWith('.json')) {               // also scan the decoded strings, so \u escapes can't hide a URL
          let strings = [];
          try { JSON.parse(text, (k, v) => { if (typeof v === 'string') strings.push(v); if (typeof k === 'string') strings.push(k); return v; }); }
          catch { problems.push(`${name}: not valid JSON`); }
          problems.push(...urlProblems(name, strings.join('\n'), cfg.allowedUrls));
        }
      }
    }
    if (name === 'manifest') {
      const keys = new Set(text.split(/\r?\n/).map((l) => l.split('=')[0].trim()).filter(Boolean));
      for (const k of cfg.manifestRequired) if (!keys.has(k)) problems.push(`manifest: missing ${k}`);
    }
  }
  return { problems, files: names };
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? '').href) {
  const cfg = process.argv[3] ? loadConfig(process.argv[3]) : CONFIG;
  const path = process.argv[2] && process.argv[2] !== '-' ? process.argv[2] : join(ROOT, cfg.outDir, cfg.zipName);
  const { problems, files } = checkZip(readFileSync(path), cfg);
  if (problems.length) {
    console.error(`package check FAILED for ${path}:\n- ${problems.join('\n- ')}`);
    process.exit(1);
  }
  console.log(`package check passed: ${files.length} files, no network APIs${cfg.allowedUrls ? ', URLs only under ' + cfg.allowedUrls.join(' ') : ''}, no secrets`);
}
