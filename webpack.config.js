const path = require('path');

module.exports = {
  entry: [
    './src/App.js'
  ],
  output: {
    path: path.resolve(__dirname, 'public', 'js'),
    publicPath: '/js/',
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: './public/',
    historyApiFallback: true
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader'
      }
    ]
  }
};