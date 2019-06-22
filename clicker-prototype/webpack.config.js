const path = require('path');

module.exports = {
  entry: [
    './app/App.js'
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
        exclude: /(node_modules)/,
        loader: 'babel-loader'
      }
    ]
  }
};
