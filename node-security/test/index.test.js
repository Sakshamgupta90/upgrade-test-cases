const { test, before, after } = require('node:test');
const assert = require('node:assert');
const { server } = require('../index');

let base;

before(async () => {
  server.listen(0);
  await new Promise((resolve) => server.once('listening', resolve));
  base = `http://127.0.0.1:${server.address().port}`;
});

after(() => server.close());

test('settings merge user choices over the defaults', async () => {
  const res = await fetch(`${base}/settings?key=theme&value=dark&key=notifications.sms&value=true`);
  assert.strictEqual(res.status, 200);
  assert.deepStrictEqual(await res.json(), { theme: 'dark', notifications: { email: true, sms: 'true' } });
});

test('settings with no input are the defaults', async () => {
  assert.deepStrictEqual(await (await fetch(`${base}/settings`)).json(),
    { theme: 'light', notifications: { email: true, sms: false } });
});

test('greets by name with the default template', async () => {
  assert.strictEqual(await (await fetch(`${base}/greet?name=Ada`)).text(), 'Hello, Ada!');
  assert.strictEqual(await (await fetch(`${base}/greet`)).text(), 'Hello, guest!');
});

test('avatar without a source is an error, not a crash', async () => {
  const res = await fetch(`${base}/avatar`);
  assert.ok(res.status >= 400, `expected an error status, got ${res.status}`);
  assert.strictEqual((await fetch(`${base}/greet?name=Bob`)).status, 200); // server still up
});

test('unknown paths are a 404', async () => {
  assert.strictEqual((await fetch(`${base}/nope`)).status, 404);
});
