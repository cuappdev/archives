const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const extractSass = new ExtractTextPlugin('css/styles.css');

module.exports = {
  // For showing line-numbers
  devtool: 'eval',
  // I/O of webpack
  entry: [path.join(__dirname, '/src/browser.js')],
  output: {
    path: path.join(__dirname, 'public'),
    publicPath: '/',
    filename: 'js/bundle.js'
  },
  // webpack-dev-server configuration for both
  // REST-API calls and Socket.io calls
  devServer: {
    historyApiFallback: true,
    proxy: {
      '/api/**': {
        target: 'http://localhost:3000'
      },
      '/socket.io/**': {
        target: 'http://localhost:3000',
        ws: true
      }
    }
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        exclude: /(node_modules)/,
        query: { presets: ['es2015', 'react', 'stage-2'] }
      },
      {
        test: /\.scss$/,
        use: extractSass.extract({
          use: [
            { loader: 'css-loader' },
            { loader: 'sass-loader' }
          ]
        })
      },
      {
        test: /\.jpe?g$|\.gif$|\.png$/i,
        loader: 'file-loader?name=images/[name].[ext]'
      }
    ]
  },
  plugins: [
    extractSass
  ]
};
