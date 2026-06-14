<script lang="ts">
	import Carousel from './Carousel.svelte';

	interface Partner {
		name: string;
		image: string;
		href?: string;
	}

	interface Props {
		items: Partner[];
	}

	let { items }: Props = $props();
</script>

<Carousel label="Partner organizations">
	{#each items as partner (partner.name)}
		<div class="carousel-slide partner-card">
			{#if partner.href}
				<a href={partner.href} target="_blank" rel="noopener noreferrer">
					<img src={partner.image} alt={partner.name} loading="lazy" />
				</a>
			{:else}
				<img src={partner.image} alt={partner.name} loading="lazy" />
			{/if}
		</div>
	{/each}
</Carousel>

<style>
	.partner-card {
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--color-white);
		padding: var(--space-6);
		min-height: 120px;
		border: 1px solid var(--color-surface);
	}

	.partner-card img {
		max-height: 80px;
		width: auto;
		object-fit: contain;
	}
</style>
