const path = require("path");

module.exports = ({ config, mode }) => {
  config.module.rules.push({
    test: /\.css$/,
    use: [
      {
        loader: "postcss-loader",
        options: {
          sourceMap: true,
          config: {
            path: "./.storybook/",
          },
        },
      },
    ],
    include: path.resolve(__dirname, "../storybook/"),
  });

  return config;
};
