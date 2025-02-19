const path = require("path");

module.exports = ({ config, mode }) => {
  config.module.rules.push({
    test: /\.css$/,
    use: [
      {
        loader: "postcss-loader",
        options: {
          postcssOptions: {
            config: path.resolve(__dirname, './postcss.config.js'),
          },
          sourceMap: true
        },
      },
    ],
    include: path.resolve(__dirname, "../"),
  });

  return config;
};
