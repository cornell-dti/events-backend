const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
  context: __dirname,

  entry: ["babel-polyfill", "./src/index"],

  output: {
    path: path.resolve("./assets/bundles/"),
    filename: "[name]-[hash].js"
  },

  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({ path: __dirname, filename: "./webpack-stats.json" })
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ["babel-loader"]
      }
    ]
  },
  resolve: {
    extensions: ["*", ".js", ".jsx"]
  }
};
