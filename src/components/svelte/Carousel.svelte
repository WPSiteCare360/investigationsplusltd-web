<script lang="ts">
	interface Props {
		label: string;
	}

	let { label, children }: Props & { children: import('svelte').Snippet } = $props();

	let track: HTMLDivElement | undefined = $state();
	let canPrev = $state(false);
	let canNext = $state(false);

	function updateButtons() {
		if (!track) return;
		canPrev = track.scrollLeft > 4;
		canNext = track.scrollLeft + track.clientWidth < track.scrollWidth - 4;
	}

	function scrollByPage(direction: -1 | 1) {
		if (!track) return;
		track.scrollBy({ left: direction * track.clientWidth * 0.85, behavior: 'smooth' });
	}

	$effect(() => {
		updateButtons();
	});
</script>

<div class="carousel">
	<div
		class="carousel-track"
		bind:this={track}
		onscroll={updateButtons}
		aria-label={label}
		role="region"
	>
		{@render children()}
	</div>
	<div class="carousel-controls">
		<button type="button" class="carousel-btn" disabled={!canPrev} onclick={() => scrollByPage(-1)}>
			<span class="sr-only">Previous</span>
			<svg viewBox="0 0 1000 1000" aria-hidden="true"><path d="M646 125C629 125 613 133 604 142L308 442C296 454 292 471 292 487 292 504 296 521 308 533L604 854C617 867 629 875 646 875 663 875 679 871 692 858 704 846 713 829 713 812 713 796 708 779 692 767L438 487 692 225C700 217 708 204 708 187 708 171 704 154 692 142 675 129 663 125 646 125Z" /></svg>
		</button>
		<button type="button" class="carousel-btn" disabled={!canNext} onclick={() => scrollByPage(1)}>
			<span class="sr-only">Next</span>
			<svg viewBox="0 0 1000 1000" aria-hidden="true"><path d="M696 533C708 521 713 504 713 487 713 471 708 454 696 446L400 146C388 133 375 125 354 125 338 125 325 129 313 142 300 154 292 171 292 187 292 204 296 221 308 233L563 492 304 771C292 783 288 800 288 817 288 833 296 850 308 863 321 871 338 875 354 875 371 875 388 867 400 854L696 533Z" /></svg>
		</button>
	</div>
</div>

<style>
	.carousel-track {
		display: flex;
		gap: var(--space-4);
		overflow-x: auto;
		scroll-snap-type: x mandatory;
		scrollbar-width: none;
		padding-bottom: var(--space-2);
	}

	.carousel-track::-webkit-scrollbar {
		display: none;
	}

	.carousel-controls {
		display: flex;
		justify-content: center;
		gap: var(--space-3);
		margin-top: var(--space-4);
	}

	.carousel-btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		border: 1px solid var(--color-theme);
		background: var(--color-white);
		color: var(--color-theme);
		cursor: pointer;
	}

	.carousel-btn:disabled {
		opacity: 0.35;
		cursor: not-allowed;
	}

	.carousel-btn svg {
		width: 16px;
		height: 16px;
		fill: currentColor;
	}

	:global(.carousel-slide) {
		flex: 0 0 min(100%, 520px);
		scroll-snap-align: start;
	}
</style>
