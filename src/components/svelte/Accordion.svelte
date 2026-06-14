<script lang="ts">
	interface Item {
		title: string;
		body: string;
	}

	interface Props {
		items: Item[];
	}

	let { items }: Props = $props();
	let openIndex = $state<number | null>(0);

	function toggle(index: number) {
		openIndex = openIndex === index ? null : index;
	}
</script>

<div class="accordion">
	{#each items as item, index (item.title)}
		<div class="accordion-item">
			<button
				type="button"
				class="accordion-trigger"
				aria-expanded={openIndex === index}
				onclick={() => toggle(index)}
			>
				<span>{item.title}</span>
				<svg class="chevron" class:open={openIndex === index} viewBox="0 0 448 512" aria-hidden="true">
					<path
						d="M207.029 381.476L12.686 187.132c-9.373-9.373-9.373-24.569 0-33.941l22.667-22.667c9.357-9.357 24.522-9.375 33.901-.04L224 284.505l154.745-154.021c9.379-9.335 24.544-9.317 33.901.04l22.667 22.667c9.373 9.373 9.373 24.569 0 33.941L240.971 381.476c-9.373 9.372-24.569 9.372-33.942 0z"
					/>
				</svg>
			</button>
			{#if openIndex === index}
				<div class="accordion-panel">
					<p>{item.body}</p>
				</div>
			{/if}
		</div>
	{/each}
</div>

<style>
	.accordion {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.accordion-item {
		border: 1px solid var(--color-surface);
		background: var(--color-white);
	}

	.accordion-trigger {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-4);
		padding: var(--space-4) var(--space-5);
		border: none;
		background: transparent;
		font-family: var(--font-heading);
		font-size: var(--font-size-base);
		font-weight: var(--font-weight-semibold);
		text-align: left;
		cursor: pointer;
		color: var(--color-black);
	}

	.chevron {
		width: 14px;
		height: 14px;
		fill: var(--color-theme);
		flex-shrink: 0;
		transition: transform var(--transition-base);
	}

	.chevron.open {
		transform: rotate(180deg);
	}

	.accordion-panel {
		padding: 0 var(--space-5) var(--space-5);
	}

	.accordion-panel p {
		margin: 0;
		color: var(--color-muted);
		line-height: var(--line-height-relaxed);
	}
</style>
