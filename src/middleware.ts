import { defineMiddleware } from 'astro:middleware';

import blogSlugs from './data/blog/slugs.json' with { type: 'json' };

const legacyBlogSlugs = new Set(blogSlugs);

/**
 * Normalize trailing slashes for SSR requests and map legacy root blog URLs.
 *
 * Astro trailingSlash "never" only auto-redirects on-demand pages in production.
 * In dev, mismatched slashes show Astro's warning 404 (by design). Prerendered
 * pages use Netlify _redirects (scripts/generate-redirects.mjs catch-all rule).
 */
export const onRequest = defineMiddleware((context, next) => {
	const { pathname, search } = context.url;

	if (pathname.length > 1 && pathname.endsWith('/')) {
		const normalized = pathname.replace(/\/+$/, '');

		if (normalized.startsWith('/blog/')) {
			return context.redirect(normalized + search, 301);
		}

		const slug = normalized.slice(1);
		if (legacyBlogSlugs.has(slug)) {
			return context.redirect(`/blog/${slug}` + search, 301);
		}

		return context.redirect(normalized + search, 301);
	}

	return next();
});
