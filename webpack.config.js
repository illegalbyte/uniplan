const path = require('path');

module.exports = {
	entry: './javascript/index.js',  // path to our input file
	output: {
		filename: 'index-bundle.js',  // output bundle file name
		path: path.resolve('./app_uniplan/static/js'),  // path to our Django static directory
	},
	module: {
		rules: [
			{
				test: /\.(js|jsx)$/,
				exclude: /node_modules/,
				loader: "babel-loader",
				options: { presets: ["@babel/preset-env", "@babel/preset-react"] }
			},
		]
	}
};