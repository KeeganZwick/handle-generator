#!/usr/bin/env node
/**
 * Minify CSS and JS for production deploy.
 *
 * Outputs:
 *   public/css/style.min.css       (from public/css/style.css)
 *   public/js/*.min.js             (from each public/js/*.js, excluding
 *                                   any existing *.min.js)
 *
 * Usage:
 *   npm run minify          — both CSS and JS
 *   npm run minify:css      — CSS only
 *   npm run minify:js       — JS only (calls scripts/minify-js.js)
 *
 * Idempotent: safe to run repeatedly. Doesn't touch the originals.
 *
 * This is a build artifact: the live site serves the *.min.* files
 * from public/. When you change an original (.css or .js), run this
 * script before re-deploying, otherwise the served HTML will reference
 * stale minified assets.
 */

'use strict';

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const CSS_SRC = path.join(ROOT, 'public', 'css', 'style.css');
const CSS_OUT = path.join(ROOT, 'public', 'css', 'style.min.css');
const JS_DIR = path.join(ROOT, 'public', 'js');

function minifyCss() {
  if (!fs.existsSync(CSS_SRC)) {
    console.error(`\n=== BUILD FAILURE ===`);
    console.error(`CSS source not found: ${CSS_SRC}`);
    console.error(`This means the minify build step ran in a context where`);
    console.error(`public/css/style.css is missing. Check the build working dir.`);
    process.exit(1);
  }
  const before = fs.statSync(CSS_SRC).size;
  execFileSync(
    path.join(ROOT, 'node_modules', '.bin', 'cleancss'),
    ['-o', CSS_OUT, CSS_SRC],
    { stdio: 'inherit' }
  );
  const after = fs.statSync(CSS_OUT).size;
  const pct = ((1 - after / before) * 100).toFixed(1);
  console.log(`CSS: ${before} B → ${after} B (${pct}% smaller)  →  ${path.relative(ROOT, CSS_OUT)}`);
}

function minifyJs() {
  // Source files: only unhashed *.js. Excludes:
  //   - *.min.js           (already minified)
  //   - *.min.{hash}.js    (hashed minified from a previous build)
  //   - anything else weird in the directory
  // The filter `endsWith('.js') && !endsWith('.min.js')` is too loose:
  // it matches `client-shim.min.abc12345.js` because that file ends
  // in `.js` (not in `.min.js`). We'd then re-minify the already-
  // minified hashed file, producing a `*.min.abc12345.min.js` mess.
  const entries = fs.readdirSync(JS_DIR).filter(
    (f) => /^[a-z][a-z0-9-]*\.js$/.test(f)
  );
  if (entries.length === 0) {
    console.error(`\n=== BUILD FAILURE ===`);
    console.error(`No .js source files found in ${JS_DIR}`);
    console.error(`This means the minify build step ran in a context where`);
    console.error(`public/js/*.js is missing. Check the build working dir.`);
    process.exit(1);
  }
  let totalBefore = 0;
  let totalAfter = 0;
  const terser = path.join(ROOT, 'node_modules', '.bin', 'terser');
  for (const file of entries) {
    const src = path.join(JS_DIR, file);
    const out = path.join(JS_DIR, file.replace(/\.js$/, '.min.js'));
    const before = fs.statSync(src).size;
    execFileSync(terser, [src, '-c', '-m', '-o', out], { stdio: 'pipe' });
    const after = fs.statSync(out).size;
    const pct = ((1 - after / before) * 100).toFixed(1);
    totalBefore += before;
    totalAfter += after;
    console.log(
      `JS:  ${before.toString().padStart(7)} B → ${after.toString().padStart(7)} B ` +
        `(${pct.padStart(4)}% smaller)  →  ${path.relative(ROOT, out)}`
    );
  }
  const totalPct = ((1 - totalAfter / totalBefore) * 100).toFixed(1);
  console.log(
    `JS total: ${totalBefore} B → ${totalAfter} B (${totalPct}% smaller across ${entries.length} files)`
  );
  console.log('=== minify complete: ' + entries.length + ' JS + 1 CSS regenerated ===');
}

const which = process.argv[2] || 'all';
if (which === 'css') {
  minifyCss();
} else if (which === 'js') {
  minifyJs();
} else if (which === 'all') {
  minifyCss();
  minifyJs();
} else {
  console.error(`Unknown target: ${which}. Use 'css', 'js', or omit for both.`);
  process.exit(1);
}
