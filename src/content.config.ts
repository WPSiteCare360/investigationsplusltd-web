import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const seoSchema = z.object({
	title: z.string(),
	description: z.string(),
	canonical: z.string().optional(),
	ogTitle: z.string().optional(),
	ogDescription: z.string().optional(),
	ogImage: z.string().optional(),
	ogType: z.string().optional(),
	ogLocale: z.string().optional(),
	twitterCard: z.string().optional(),
	twitterSite: z.string().optional(),
	articlePublishedTime: z.string().optional(),
	articleModifiedTime: z.string().optional(),
	robots: z
		.object({
			index: z.string().optional(),
			follow: z.string().optional(),
		})
		.optional(),
});

const taxonomyItemSchema = z.object({
	slug: z.string(),
	name: z.string(),
});

const blog = defineCollection({
	loader: glob({ base: './src/content/blog', pattern: '**/*.md' }),
	schema: z.object({
		title: z.string(),
		description: z.string(),
		excerpt: z.string().optional(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		/** URL path segment, e.g. /blog/{slug} */
		slug: z.string(),
		categories: z.array(z.string()).default([]),
		tags: z.array(z.string()).default([]),
		taxonomy: z
			.object({
				categories: z.array(taxonomyItemSchema).default([]),
				tags: z.array(taxonomyItemSchema).default([]),
			})
			.optional(),
		author: z.object({
			id: z.number(),
			name: z.string(),
			slug: z.string().nullish(),
		}),
		seo: seoSchema,
		image: z
			.object({
				src: z.string(),
				alt: z.string().optional(),
			})
			.optional(),
		legacyId: z.number(),
	}),
});

export const collections = { blog };
