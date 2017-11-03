// @flow
const express = require('express');
const path = require('path');
const fs = require('fs');
const webpack = require('webpack');
const app = express();
const port = 8080

app.use(express.static(path.resolve(__dirname, 'public')));

app.get(/[^\.(css|js)]/, (req, res) => {
  res.sendFile(path.resolve(__dirname, 'public', 'index.html'));
});

app.listen(port, () => { console.log(`Listening on http://localhost:${port}`) });