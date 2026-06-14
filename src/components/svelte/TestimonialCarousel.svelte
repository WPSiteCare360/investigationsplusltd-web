<script lang="ts">
	import Carousel from './Carousel.svelte';

	interface Testimonial {
		heading: string;
		body: string;
		name: string;
	}

	interface Props {
		items: Testimonial[];
	}

	let { items }: Props = $props();
</script>

<Carousel label="Client testimonials">
	{#each items as item (item.name)}
		<article class="carousel-slide testimonial-card">
			<h3>{item.heading}</h3>
			<p>{item.body}</p>
			<p class="testimonial-name">{item.name}</p>
		</article>
	{/each}
</Carousel>

<style>
	.testimonial-card {
		background: var(--color-white);
		padding: var(--space-8);
		box-shadow: var(--shadow-sm);
		border-left: 4px solid var(--color-theme);
	}

	.testimonial-card h3 {
		font-size: var(--font-size-lg);
		margin: 0 0 var(--space-3);
		font-family: var(--font-heading);
		font-weight: var(--font-weight-bold);
	}

	.testimonial-card p {
		color: var(--color-muted);
		line-height: var(--line-height-relaxed);
		font-style: italic;
		margin: 0 0 var(--space-4);
	}

	.testimonial-name {
		margin-top: var(--space-4);
		margin-bottom: 0;
		font-family: var(--font-heading);
		font-weight: var(--font-weight-semibold);
		font-style: normal;
		color: var(--color-black);
	}
</style>
