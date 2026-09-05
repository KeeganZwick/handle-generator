#!/usr/bin/env node
'use strict';
// Re-export minify.js's main logic for the `minify:js` npm script.
// The single-file approach keeps the implementation in minify.js.
process.argv = [process.argv[0], 'minify-js', 'js'];
require('./minify.js');
