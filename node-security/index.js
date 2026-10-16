const http = require('http');
const { URL } = require('url');
const _ = require('lodash');
const axios = require('axios');

const defaults = { theme: 'light', notifications: { email: true, sms: false } };

function buildSettings(keys, values) {
  return _.merge({}, defaults, _.zipObjectDeep(keys, values));
}

function renderGreeting(templateSource, data) {
  return _.template(templateSource)(data);
}

async function fetchAvatar(url) {
  const res = await axios.get(url, { responseType: 'arraybuffer', maxRedirects: 5 });
  return Buffer.from(res.data);
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  try {
    if (url.pathname === '/settings') {
      const keys = url.searchParams.getAll('key');
      const values = url.searchParams.getAll('value');
      res.setHeader('Content-Type', 'application/json');
      return res.end(JSON.stringify(buildSettings(keys, values)));
    }
    if (url.pathname === '/greet') {
      const template = url.searchParams.get('template') || 'Hello, <%= name %>!';
      return res.end(renderGreeting(template, { name: url.searchParams.get('name') || 'guest' }));
    }
    if (url.pathname === '/avatar') {
      const image = await fetchAvatar(url.searchParams.get('src'));
      res.setHeader('Content-Type', 'image/png');
      return res.end(image);
    }
    res.statusCode = 404;
    res.end('Not found');
  } catch (err) {
    res.statusCode = 500;
    res.end(err.message);
  }
});

server.listen(3001, () => console.log('Listening on http://localhost:3001'));
