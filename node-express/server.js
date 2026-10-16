const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());

const users = { 1: { id: 1, name: 'Ada' }, 2: { id: 2, name: 'Linus' } };

app.get('/users/:id', (req, res) => {
  const user = users[req.param('id')];
  if (!user) return res.send(404, 'Not found');
  res.json(user);
});

app.post('/users', (req, res) => {
  const id = Object.keys(users).length + 1;
  users[id] = { id, ...req.body };
  res.json(users[id], 201);
});

app.del('/users/:id', (req, res) => {
  delete users[req.params.id];
  res.send(204);
});

app.get('/files/*', (req, res) => {
  res.sendfile(path.join(__dirname, 'public', req.params[0]));
});

app.get('/reports/:year/:month?', (req, res) => {
  res.json({ year: req.params.year, month: req.params.month || 'all' });
});

app.get('/logout', (req, res) => {
  res.redirect('back');
});

app.listen(3000, () => console.log('Listening on http://localhost:3000'));
