const path = require("path");
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
	context: __dirname,

	entry: ['babel-polyfill', './backend_main/static/src/index'],

	output: {
		path: path.resolve('./backend_main/static/bundles/'),
		filename: "[name]-[hash].js",
	},

	plugins: [
		new BundleTracker({filename: './webpack-stats.json'}),
	],
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				use: ['babel-loader']
			}
		]
	},
	resolve: {
		extensions: ['*', '.js', '.jsx']
	}

};