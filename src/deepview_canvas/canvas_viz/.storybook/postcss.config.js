const path = require('path');
var tailwindcss = require("tailwindcss");

module.exports = {
  plugins: [
    require("postcss-import")(),
    tailwindcss(path.resolve(__dirname, '../tailwind.config.js')),
    require("autoprefixer"),
  ],
};
