import path from 'path';
import preprocess from 'svelte-preprocess';

export default {
  stories: [{
    directory: '../stories',
    files:'**/*.stories.svelte',
    titlePrefix:'Demo'
  }],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-links',
    '@storybook/addon-svelte-csf'
  ],
  framework: {
    name: '@storybook/svelte-webpack5',
    options: {
      preprocess: preprocess({
        typescript: {
          tsconfigFile: path.resolve(__dirname, '../tsconfig.json'),
          transpileOnly: true,
          compilerOptions: {
            moduleResolution: 'node'
          }
        },
        sourceMap: true
      }),
      builder: {
        name: 'webpack5',
        options: {
          lazyCompilation: true
        }
      },
      onwarn: (warning, handler) => {
        if (
          warning.code === 'a11y-missing-content' ||
          warning.code === 'a11y-no-noninteractive-tabindex' ||
          warning.code === 'a11y-click-events-have-key-events' ||
          warning.code === 'a11y-no-static-element-interactions'
        ) {
          return;
        }

        handler(warning);
      }
    }
  },
  docs: {
    autodocs: "tag",
  },
  webpackFinal: async (config, { configType }) => {
    config.optimization = {
      minimize: configType === 'PRODUCTION'
    };

    config.resolve = {
      ...config.resolve,
      alias: {
        ...config.resolve?.alias,
        'betterwithdata/canvas_viz': path.resolve(__dirname, '../src/'),
      },
      extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.svelte'],
      mainFields: ['svelte', 'browser', 'module', 'main']
    };

    config.module = {
      ...config.module,
      rules: [
        ...config.module.rules,
        {
          test: /\.ts$/,
          use: [
            {
              loader: 'ts-loader',
              options: {
                transpileOnly: true,
                configFile: path.resolve(__dirname, '../tsconfig.json'),
              },
            },
          ],
          exclude: /node_modules/,
        },
      ],
    };

    return config;
  }
};
