import { defineConfig } from 'vitest/config';

// Using dynamic import for ESM-only @sveltejs/vite-plugin-svelte
export default defineConfig(async () => {
  const { svelte } = await import('@sveltejs/vite-plugin-svelte');
  return {
    plugins: [
      svelte({ hot: !process.env.VITEST })
    ],
    test: {
      environment: 'jsdom',
      globals: true,
      // setupFiles line is intentionally removed
    },
  };
});
