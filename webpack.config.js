const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const extractSass = new ExtractTextPlugin('css/styles.css');

module.exports = {
  devtool: 'eval',
  entry: [path.join(__dirname, 'src/browser.js')],
  output: {
    path: path.join(__dirname, './public/'),
    publicPath: '/public',
    filename: 'js/bundle.js'
  },
  devServer: {
    historyApiFallback: true,
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
