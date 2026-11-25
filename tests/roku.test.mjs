// The Roku app end to end: lint the BrightScript, run the book unit tests and a scripted pass through
// every recipe and tab in the brs-cli simulator, build the sideload zip and pass it through the security gate.
import { test } from 'node:test';
import assert from 'node:assert';
import { execFileSync } from 'node:child_process';
import { readFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ROOT, CONFIG, build, collect } from '../scripts/build.mjs';
import { checkZip } from '../scripts/check-package.mjs';
import { makeZip, readZip } from '../scripts/zip.mjs';

const bin = (name) => join(ROOT, 'node_modules', '.bin', name);
const run = (cmd, args) => execFileSync(cmd, args, { cwd: ROOT, encoding: 'utf8', timeout: 240_000, stdio: ['ignore', 'pipe', 'pipe'] });
const book = JSON.parse(readFileSync(join(ROOT, 'roku', 'data', 'recipes.json'), 'utf8')).recipes;

test('BrightScript passes the brighterscript compiler checks', () => {
  const out = run(bin('bsc'), ['--project', 'bsconfig.json', '--stagingDir', join(mkdtempSync(join(tmpdir(), 'bsc-')), 'stage')]);
  assert.doesNotMatch(out, /error BS\d+/, out);
});

test('book rules: unit tests in the simulator', () => {
  const src = ['config', 'book'].map((f) => `roku/source/${f}.brs`);
  const out = run(bin('brs-cli'), ['-n', '-r', ROOT, 'tests/book_test.brs', ...src]);
  const m = out.match(/RESULT pass=(\d+) fail=(\d+)/);
  assert.ok(m, out);
  assert.equal(m[2], '0', out);
  assert.ok(Number(m[1]) >= 25, out);
});

test('the built zip opens every recipe and draws every page', () => {
  const out = run(bin('brs-cli'), ['-n', '-k', 'autotest=1', build()]);
  assert.match(out, /AUTOTEST OK/, out);
  const m = out.match(/AUTOTEST recipes=(\d+) pages=(\d+) checked=(\d+) frames=(\d+) overflows=(\d+) view=(\w+) last=(.*)/);
  assert.ok(m, out);
  const pages = book.reduce((n, r) => n + r.steps.length + (r.prep.length ? 1 : 0), 0);
  assert.equal(Number(m[1]), book.length);
  assert.ok(Number(m[2]) >= pages, `paged through all ${pages} step pages`);
  assert.equal(Number(m[3]), book.length, 'checked off an ingredient in each recipe');
  assert.equal(m[5], '0', 'every step page fits on the screen');
  assert.equal(m[6], 'menu', 'Back returned to the menu');
  assert.equal(m[7].trim(), book.at(-1).name);
});

test('the zip passes the security gate and carries the recipes', () => {
  const zip = readFileSync(build());
  const { problems, files } = checkZip(zip);
  assert.deepEqual(problems, []);
  for (const f of ['manifest', 'source/main.brs', 'data/recipes.json', 'images/icon_hd.png']) assert.ok(files.includes(f), f);
  assert.ok(files.every((f) => !f.startsWith('tests/') && !f.startsWith('node_modules/')));
  const data = readZip(zip).find((e) => e.name === 'data/recipes.json').data.toString('utf8');
  assert.ok(JSON.parse(data).recipes.some((r) => r.name === 'Thanksgiving Apple Pie'));
});

test('the security gate rejects secrets, network code and stray files', () => {
  const good = collect();
  const bad = (extra) => checkZip(makeZip([...good, ...extra])).problems.join('\n');
  assert.match(bad([{ name: 'source/net.brs', data: Buffer.from('x = CreateObject("ROURLTRANSFER")') }]), /roUrlTransfer/);
  assert.match(bad([{ name: 'data/x.json', data: Buffer.from('{"u":"https://example.com"}') }]), /https:\/\//);
  assert.match(bad([{ name: 'source/k.brs', data: Buffer.from('k = "ghp_' + 'a'.repeat(36) + '"') }]), /secret/);
  assert.match(bad([{ name: '.env', data: Buffer.from('X=1') }]), /not in an allowed folder/);
  assert.match(bad([{ name: 'source/run.sh', data: Buffer.from('echo') }]), /file type not allowed/);
});

test('builds are byte-identical and the manifest has a version', () => {
  assert.ok(readFileSync(build()).equals(readFileSync(build())));
  const manifest = readFileSync(join(ROOT, 'roku', 'manifest'), 'utf8');
  for (const k of CONFIG.manifestRequired) assert.match(manifest, new RegExp(`^${k}=\\S`, 'm'));
});
