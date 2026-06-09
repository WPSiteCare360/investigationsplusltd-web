<script lang="ts">
	let count = $state(0);
</script>

<section>
	<h2>Welcome to Astro + Svelte</h2>
	<p>Your site is ready for Netlify deployment.</p>
	<button type="button" onclick={() => count++}>
		Clicked {count} {count === 1 ? 'time' : 'times'}
	</button>
</section>

<style>
	section {
		font-family: system-ui, sans-serif;
		max-width: 40rem;
		margin: 2rem auto;
		padding: 0 1rem;
	}

	h2 {
		margin-bottom: 0.5rem;
	}

	button {
		margin-top: 1rem;
		padding: 0.5rem 1rem;
		cursor: pointer;
	}
</style>
