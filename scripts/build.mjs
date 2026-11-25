#!/usr/bin/env node
// Build the Roku sideload zip: roku/manifest, source/, data/ and images/ at the zip root.
//   node scripts/build.mjs            -> dist/recipes_roku.zip
// Copied from leftbrain847/kart_roku; run `python build_roku.py` first if recipes.py changed.
import { readFileSync, readdirSync, statSync, lstatSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { makeZip } from './zip.mjs';

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const loadConfig = (path = join(ROOT, 'scripts', 'package.config.json')) => JSON.parse(readFileSync(resolve(ROOT, path), 'utf8'));
export const CONFIG = loadConfig();

function walk(abs) {
  const st = lstatSync(abs);
  if (st.isSymbolicLink()) throw new Error(`${abs}: symlinks are not allowed in the package`);
  if (st.isFile()) return [abs];
  return readdirSync(abs).sort().flatMap((n) => walk(join(abs, n)));
}

export function collect(root = ROOT, cfg = CONFIG) {
  const base = join(root, cfg.root ?? '');
  return cfg.include.flatMap((p) => walk(join(base, p))).map((abs) => ({
    name: relative(base, abs).split(sep).join('/'),
    data: readFileSync(abs),
  }));
}

export function build(root = ROOT, cfg = CONFIG) {
  const zip = makeZip(collect(root, cfg));
  mkdirSync(join(root, cfg.outDir), { recursive: true });
  const out = join(root, cfg.outDir, cfg.zipName);
  writeFileSync(out, zip);
  return out;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? '').href) {
  const cfg = process.argv[2] ? loadConfig(process.argv[2]) : CONFIG;
  const out = build(ROOT, cfg);
  console.log(`built ${relative(ROOT, out)} (${statSync(out).size} bytes)`);
}
