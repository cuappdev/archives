const path = require('path');

module.exports = {
  entry: [path.join(__dirname, '/server.js')],
  output: {
    path: path.join(__dirname, './build/'),
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        exclude: /(node_modules)/,
        query: {
          presets: [
            'es2015',
            'stage-2',
          ]
        },
      },
    ],
  },
};
