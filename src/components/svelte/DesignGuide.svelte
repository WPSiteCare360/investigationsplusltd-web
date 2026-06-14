<script lang="ts">
	import {
		colors,
		fonts,
		fontSizes,
		fontWeights,
		lineHeights,
		spacing,
		layout,
		radii,
		shadows,
		breakpoints,
		transitions,
	} from '../../lib/design-tokens';

	const colorEntries = Object.entries(colors) as [string, string][];
	const fontEntries = Object.entries(fonts) as [string, string][];
	const fontSizeEntries = Object.entries(fontSizes) as [string, string][];
	const spacingEntries = Object.entries(spacing) as [string, string][];
</script>

<div class="design-guide">
	<header class="guide-hero theme-bg">
		<div class="container">
			<h6 class="subtitle-white">Design system</h6>
			<h1 class="heading-mixed">
				Investigations <b>Plus</b> <i>tokens</i>
			</h1>
			<p class="guide-lead">
				Design tokens and patterns converted from the WordPress Elementor site. Use CSS
				variables from <code>src/styles/tokens.css</code> or import from
				<code>src/lib/design-tokens.ts</code>.
			</p>
		</div>
	</header>

	<div class="container guide-body">
		<section class="guide-section" id="colors">
			<h2>Colors</h2>
			<div class="swatch-grid">
				{#each colorEntries as [name, value] (name)}
					<div class="swatch">
						<div class="swatch-color" style:background-color={value}></div>
						<div class="swatch-meta">
							<strong>{name}</strong>
							<code>{value}</code>
							<span>var(--color-{name.replace(/([A-Z])/g, '-$1').toLowerCase()})</span>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<section class="guide-section" id="typography">
			<h2>Typography</h2>

			<h3>Font families</h3>
			<div class="type-samples">
				{#each fontEntries as [name, value] (name)}
					<div class="type-row">
						<span class="type-label">{name}</span>
						<p style:font-family={value}>
							The quick brown fox jumps over the lazy dog.
						</p>
						<code>{value}</code>
					</div>
				{/each}
			</div>

			<h3>Font sizes</h3>
			<div class="size-list">
				{#each fontSizeEntries as [name, value] (name)}
					<div class="size-row">
						<span class="size-label">{name}</span>
						<span style:font-size={value}>Sample text at {value}</span>
					</div>
				{/each}
			</div>

			<h3>Heading hierarchy</h3>
			<div class="heading-stack">
				<h1>Heading 1 - Toronto Private Investigators</h1>
				<h2>Heading 2 - About Investigations Plus</h2>
				<h3>Heading 3 - Key Services</h3>
				<h4>Heading 4 - Who we are</h4>
				<h5>Heading 5 - Section label</h5>
				<h6>Heading 6 - Subtitle style (also uses .subtitle-green)</h6>
			</div>

			<h3>Body text</h3>
			<p>
				We are Toronto private investigators with a flair for solving complex cases that has
				been recognized by the insurance industry, law firms, large corporations, and small
				businesses.
			</p>

			<h3>Mixed heading pattern</h3>
			<div class="subtitle-wrap">
				<h6 class="subtitle-green">Some information</h6>
			</div>
			<h2 class="heading-mixed">Want us <i>to</i><br /><b>investigate</b> Something?</h2>
		</section>

		<section class="guide-section" id="buttons">
			<h2>Buttons</h2>
			<div class="button-row">
				<a class="btn btn-theme" href="#">Consult Now</a>
				<a class="btn btn-theme-light" href="#">Learn More</a>
				<a class="btn btn-outline" href="#">Get in Touch</a>
			</div>
		</section>

		<section class="guide-section" id="spacing">
			<h2>Spacing scale</h2>
			<div class="spacing-list">
				{#each spacingEntries as [name, value] (name)}
					<div class="spacing-row">
						<span class="spacing-label">{name}</span>
						<div class="spacing-bar" style:width={value}></div>
						<code>{value}</code>
					</div>
				{/each}
			</div>
		</section>

		<section class="guide-section" id="layout">
			<h2>Layout</h2>
			<dl class="token-dl">
				{#each Object.entries(layout) as [key, value] (key)}
					<div>
						<dt>{key}</dt>
						<dd><code>{value}</code></dd>
					</div>
				{/each}
			</dl>
			<div class="layout-demo">
				<div class="layout-box">
					<span>.container max-width: {layout.maxWidth}</span>
				</div>
			</div>
		</section>

		<section class="guide-section" id="misc">
			<h2>Radii, shadows, breakpoints, transitions</h2>

			<h3>Border radii</h3>
			<div class="radii-row">
				{#each Object.entries(radii) as [name, value] (name)}
					<div class="radii-box" style:border-radius={value}>
						{name}
					</div>
				{/each}
			</div>

			<h3>Shadows</h3>
			<div class="shadow-row">
				{#each Object.entries(shadows) as [name, value] (name)}
					<div class="shadow-box" style:box-shadow={value}>{name}</div>
				{/each}
			</div>

			<h3>Breakpoints</h3>
			<dl class="token-dl">
				{#each Object.entries(breakpoints) as [key, value] (key)}
					<div>
						<dt>{key}</dt>
						<dd><code>{value}</code></dd>
					</div>
				{/each}
			</dl>

			<h3>Line heights & weights</h3>
			<dl class="token-dl">
				{#each Object.entries(lineHeights) as [key, value] (key)}
					<div>
						<dt>lineHeight.{key}</dt>
						<dd><code>{value}</code></dd>
					</div>
				{/each}
				{#each Object.entries(fontWeights) as [key, value] (key)}
					<div>
						<dt>fontWeight.{key}</dt>
						<dd><code>{value}</code></dd>
					</div>
				{/each}
				{#each Object.entries(transitions) as [key, value] (key)}
					<div>
						<dt>transition.{key}</dt>
						<dd><code>{value}</code></dd>
					</div>
				{/each}
			</dl>
		</section>

		<section class="guide-section theme-bg section-on-green" id="on-green">
			<h6 class="subtitle-white">On green background</h6>
			<h2>Section on theme background</h2>
			<p>White text and subtitle line variants used in hero and CTA bands.</p>
			<a class="btn btn-theme-light" href="#">Example CTA</a>
		</section>
	</div>
</div>

<style>
	.design-guide {
		padding-bottom: var(--space-16);
	}

	.guide-hero {
		padding: var(--space-16) 0 var(--space-12);
		margin-bottom: var(--space-10);
	}

	.guide-hero .container {
		padding-left: calc(var(--layout-content-padding) + var(--layout-subtitle-line-offset));
	}

	.guide-lead {
		max-width: 42rem;
		font-size: var(--font-size-lg);
		opacity: 0.95;
	}

	.guide-body {
		display: flex;
		flex-direction: column;
		gap: var(--space-12);
	}

	.guide-section h2 {
		font-size: var(--font-size-2xl);
		margin-bottom: var(--space-6);
		padding-bottom: var(--space-3);
		border-bottom: 2px solid var(--color-surface);
	}

	.guide-section h3 {
		font-size: var(--font-size-lg);
		margin: var(--space-6) 0 var(--space-4);
	}

	.swatch-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: var(--space-4);
	}

	.swatch {
		border: 1px solid var(--color-surface);
		overflow: hidden;
	}

	.swatch-color {
		height: 80px;
		border-bottom: 1px solid var(--color-surface);
	}

	.swatch-meta {
		padding: var(--space-3);
		font-size: var(--font-size-sm);
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
	}

	.swatch-meta code {
		font-size: var(--font-size-xs);
	}

	.swatch-meta span {
		color: var(--color-muted);
		font-size: var(--font-size-xs);
	}

	.type-samples,
	.size-list,
	.spacing-list {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.type-row,
	.size-row,
	.spacing-row {
		display: grid;
		grid-template-columns: 100px 1fr auto;
		gap: var(--space-4);
		align-items: center;
		padding: var(--space-3);
		background: var(--color-surface);
	}

	.type-label,
	.size-label,
	.spacing-label {
		font-family: var(--font-heading);
		font-weight: var(--font-weight-semibold);
		font-size: var(--font-size-sm);
		text-transform: uppercase;
	}

	.spacing-bar {
		height: 12px;
		background: var(--color-theme);
		max-width: 100%;
	}

	.heading-stack {
		padding: var(--space-6);
		background: var(--color-surface);
	}

	.subtitle-wrap {
		padding-left: var(--layout-subtitle-line-offset);
	}

	.button-row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-4);
	}

	.token-dl {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
		gap: var(--space-3);
		margin: 0;
	}

	.token-dl > div {
		padding: var(--space-3);
		background: var(--color-surface);
	}

	.token-dl dt {
		font-family: var(--font-heading);
		font-weight: var(--font-weight-semibold);
		font-size: var(--font-size-sm);
		margin-bottom: var(--space-1);
	}

	.token-dl dd {
		margin: 0;
	}

	.layout-demo {
		margin-top: var(--space-6);
		background: repeating-linear-gradient(
			-45deg,
			var(--color-surface),
			var(--color-surface) 10px,
			#e5e5e4 10px,
			#e5e5e4 20px
		);
		padding: var(--space-6);
	}

	.layout-box {
		max-width: var(--layout-max-width);
		margin-inline: auto;
		padding: var(--space-8);
		background: var(--color-white);
		border: 2px dashed var(--color-theme);
		text-align: center;
		font-family: var(--font-heading);
	}

	.radii-row,
	.shadow-row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-4);
	}

	.radii-box,
	.shadow-box {
		width: 100px;
		height: 80px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--color-white);
		border: 1px solid var(--color-surface);
		font-size: var(--font-size-xs);
		font-family: var(--font-heading);
	}

	.section-on-green {
		padding: var(--space-10);
		margin-top: var(--space-4);
	}

	.section-on-green .container,
	.section-on-green {
		padding-left: calc(var(--space-10) + var(--layout-subtitle-line-offset));
	}

	code {
		font-size: 0.9em;
		background: rgba(0, 0, 0, 0.06);
		padding: 0.1em 0.35em;
	}
</style>
