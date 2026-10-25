const { test, before, after } = require('node:test');
const assert = require('node:assert');
const app = require('../server');

let server;
let base;

before(async () => {
  server = app.listen(0);
  await new Promise((resolve) => server.once('listening', resolve));
  base = `http://127.0.0.1:${server.address().port}`;
});

after(() => server.close());

test('gets a user', async () => {
  const res = await fetch(`${base}/users/1`);
  assert.strictEqual(res.status, 200);
  assert.deepStrictEqual(await res.json(), { id: 1, name: 'Ada' });
});

test('unknown user is a 404', async () => {
  const res = await fetch(`${base}/users/99`);
  assert.strictEqual(res.status, 404);
  assert.strictEqual(await res.text(), 'Not found');
});

test('creates a user from JSON', async () => {
  const res = await fetch(`${base}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Grace' }),
  });
  assert.strictEqual(res.status, 201);
  assert.deepStrictEqual(await res.json(), { id: 3, name: 'Grace' });
});

test('creates a user from a form', async () => {
  const res = await fetch(`${base}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'name=Alan',
  });
  assert.strictEqual(res.status, 201);
  assert.strictEqual((await res.json()).name, 'Alan');
});

test('deletes a user', async () => {
  const res = await fetch(`${base}/users/2`, { method: 'DELETE' });
  assert.strictEqual(res.status, 204);
  assert.strictEqual((await fetch(`${base}/users/2`)).status, 404);
});

test('serves files from public/, including nested paths', async () => {
  const res = await fetch(`${base}/files/hello.txt`);
  assert.strictEqual(res.status, 200);
  assert.strictEqual((await res.text()).trim(), 'hello from public');
});

test('report month is optional', async () => {
  assert.deepStrictEqual(await (await fetch(`${base}/reports/2024`)).json(), { year: '2024', month: 'all' });
  assert.deepStrictEqual(await (await fetch(`${base}/reports/2024/05`)).json(), { year: '2024', month: '05' });
});

test('logout sends you back where you came from', async () => {
  const withReferrer = await fetch(`${base}/logout`, { redirect: 'manual', headers: { Referer: 'http://example.com/page' } });
  assert.strictEqual(withReferrer.status, 302);
  assert.strictEqual(withReferrer.headers.get('location'), 'http://example.com/page');
  const without = await fetch(`${base}/logout`, { redirect: 'manual' });
  assert.strictEqual(without.headers.get('location'), '/');
});
