// Renders the app to HTML with React's server renderer and checks what the user would see.
// esbuild only turns the JSX into plain JavaScript; React itself comes from node_modules.
const { test } = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const esbuild = require('esbuild');

function loadApp() {
  // Written inside the project so `require('react')` resolves from its node_modules.
  const out = path.join(__dirname, '.build', 'App.cjs');
  esbuild.buildSync({
    entryPoints: [path.join(__dirname, '..', 'src', 'App.js')],
    outfile: out, bundle: true, packages: 'external', platform: 'node', format: 'cjs',
    loader: { '.js': 'jsx' }, jsx: 'automatic', logLevel: 'silent',
  });
  delete require.cache[out];
  const mod = require(out);
  return mod.default || mod;
}

function render() {
  const React = require('react');
  const { renderToString } = require('react-dom/server');
  // React marks boundaries between text nodes with <!-- --> comments; they're not visible.
  return renderToString(React.createElement(loadApp())).replace(/<!-- -->/g, '');
}

test('greets the visitor with the default name', () => {
  assert.match(render(), /<h2>Hello, stranger<\/h2>/);
});

test('search box starts with the initial query', () => {
  const html = render();
  assert.match(html, /<input[^>]*value="react"/);
});

test('renders the greeting before the search box', () => {
  const html = render();
  assert.ok(html.indexOf('<h2>') < html.indexOf('<input'));
});
