const path = require('path');

module.exports = {
	entry: './javascript/assignments.js',  // path to our input file
	output: {
		filename: 'index-bundle.js',  // output bundle file name
		path: path.resolve('./app_uniplan/static/js'),  // path to our Django static directory
	},
};