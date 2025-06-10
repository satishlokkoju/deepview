import { defineConfig } from 'vitest/config';

// Using dynamic import for ESM-only @sveltejs/vite-plugin-svelte
export default defineConfig(async () => {
  const { svelte } = await import('@sveltejs/vite-plugin-svelte');
  const { default: sveltePreprocess } = await import('svelte-preprocess');
  
  return {
    plugins: [
      svelte({ 
        hot: !process.env.VITEST,
        preprocess: sveltePreprocess() // Add TypeScript preprocessing
      })
    ],
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: ['./tests/setup.js'] // Add jest-dom matchers setup file
    },
  };
});
