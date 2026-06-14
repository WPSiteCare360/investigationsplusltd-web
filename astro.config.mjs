// @ts-check
import { defineConfig } from 'astro/config';

import svelte from '@astrojs/svelte';

import netlify from '@astrojs/netlify';

import blogSlugs from './src/data/blog/slugs.json' with { type: 'json' };
import { legacyLocationRedirects } from './src/data/contact.ts';

/** @type {import('astro').AstroUserConfig['redirects']} */
const redirects = {
	...Object.fromEntries(blogSlugs.map((slug) => [`/${slug}`, `/blog/${slug}`])),
	...legacyLocationRedirects,
};

// https://astro.build/config
export default defineConfig({
	trailingSlash: 'never',
	integrations: [svelte()],
	adapter: netlify(),
	redirects,
	server: {
		host: true,
		allowedHosts: ['192.168.1.123', '100.100.2.3', 'localhost', '127.0.0.1'],
	},
});
