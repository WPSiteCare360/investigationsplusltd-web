<script lang="ts">
	import type { NavItem } from '../../data/navigation';
	import { mainNav, siteConfig } from '../../data/navigation';

	interface Props {
		currentPath?: string;
	}

	let { currentPath = '' }: Props = $props();

	let mobileOpen = $state(false);
	let openDropdown = $state<string | null>(null);

	function isActive(href: string): boolean {
		if (href === '/') return currentPath === '/' || currentPath === '';
		return currentPath.startsWith(href.replace(/\/$/, ''));
	}

	function toggleMobile() {
		mobileOpen = !mobileOpen;
		if (!mobileOpen) openDropdown = null;
	}

	function toggleDropdown(label: string) {
		openDropdown = openDropdown === label ? null : label;
	}

	function closeMobile() {
		mobileOpen = false;
		openDropdown = null;
	}

	function navLinkClass(href: string, isChild = false): string {
		const base = isChild ? 'nav-subitem' : 'nav-item';
		return isActive(href) ? `${base} is-active` : base;
	}
</script>

<header class="site-header">
	<div class="top-bar">
		<div class="container top-bar-inner">
			<a class="top-bar-link" href={siteConfig.phoneHref}>{siteConfig.phone}</a>
			<a class="top-bar-link" href={`mailto:${siteConfig.email}`}>{siteConfig.email}</a>
			<img
				class="top-bar-flag"
				src="/images/brand/Canadian-flag-40x20-1.png"
				alt="Canadian flag"
				width="40"
				height="20"
			/>
		</div>
	</div>

	<div class="main-bar">
		<div class="container main-bar-inner">
			<a class="logo-link" href="/" aria-label={siteConfig.name}>
				<img
					class="logo"
					src="/images/brand/invertigationplus-text-logo-white.svg"
					alt={siteConfig.name}
					width="200"
					height="40"
				/>
			</a>

			<button
				type="button"
				class="menu-toggle"
				aria-expanded={mobileOpen}
				aria-controls="site-nav"
				onclick={toggleMobile}
			>
				<span class="sr-only">Menu</span>
				{#if mobileOpen}
					<svg viewBox="0 0 1000 1000" aria-hidden="true" width="24" height="24">
						<path
							d="M742 167L500 408 258 167C246 154 233 150 217 150 196 150 179 158 167 167 154 179 150 196 150 212 150 229 154 242 171 254L408 500 167 742C138 771 138 800 167 829 196 858 225 858 254 829L496 587 738 829C750 842 767 846 783 846 800 846 817 842 829 829 842 817 846 804 846 783 846 767 842 750 829 737L588 500 833 258C863 229 863 200 833 171 804 137 775 137 742 167Z"
						/>
					</svg>
				{:else}
					<svg viewBox="0 0 1000 1000" aria-hidden="true" width="24" height="24">
						<path
							d="M104 333H896C929 333 958 304 958 271S929 208 896 208H104C71 208 42 237 42 271S71 333 104 333ZM104 583H896C929 583 958 554 958 521S929 458 896 458H104C71 458 42 487 42 521S71 583 104 583ZM104 833H896C929 833 958 804 958 771S929 708 896 708H104C71 708 42 737 42 771S71 833 104 833Z"
						/>
					</svg>
				{/if}
			</button>

			<nav id="site-nav" class="site-nav" class:is-open={mobileOpen} aria-label="Main">
				<ul class="nav-list">
					{#each mainNav as item (item.label)}
						<li class="nav-list-item" class:has-children={!!item.children}>
							{#if item.children}
								<button
									type="button"
									class={navLinkClass(item.href)}
									class:dropdown-open={openDropdown === item.label}
									aria-expanded={openDropdown === item.label}
									onclick={() => toggleDropdown(item.label)}
								>
									{item.label}
									<svg class="chevron" viewBox="0 0 320 512" aria-hidden="true" width="10" height="10">
										<path
											d="M143 352.3L7 216.3c-9.4-9.4-9.4-24.6 0-33.9l22.6-22.6c9.4-9.4 24.6-9.4 33.9 0l96.4 96.4 96.4-96.4c9.4-9.4 24.6-9.4 33.9 0l22.6 22.6c9.4 9.4 9.4 24.6 0 33.9l-136 136c-9.2 9.4-24.4 9.4-33.8 0z"
										/>
									</svg>
								</button>
								<ul class="submenu" class:is-open={openDropdown === item.label}>
									{#each item.children as child (child.href)}
										<li>
											<a
												class={navLinkClass(child.href, true)}
												href={child.href}
												onclick={closeMobile}
											>
												{child.label}
											</a>
										</li>
									{/each}
								</ul>
							{:else}
								<a class={navLinkClass(item.href)} href={item.href} onclick={closeMobile}>
									{item.label}
								</a>
							{/if}
						</li>
					{/each}
				</ul>
			</nav>
		</div>
	</div>
</header>

<style>
	.site-header {
		position: sticky;
		top: 0;
		z-index: 100;
	}

	.top-bar {
		background-color: var(--color-theme);
		color: var(--color-white);
	}

	.top-bar-inner {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-6);
		padding-block: var(--space-2);
		flex-wrap: wrap;
	}

	.top-bar-link {
		font-family: var(--font-topbar);
		font-size: var(--font-size-md);
		font-weight: var(--font-weight-semibold);
		text-transform: lowercase;
		text-decoration: underline;
		color: var(--color-white);
	}

	.top-bar-link:hover {
		text-decoration: underline;
		opacity: 0.9;
	}

	.top-bar-flag {
		flex-shrink: 0;
	}

	.main-bar {
		background-color: var(--color-theme);
		color: var(--color-white);
		border-top: 1px solid rgba(255, 255, 255, 0.12);
	}

	.main-bar-inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-6);
		padding-block: var(--space-3);
	}

	.logo-link {
		flex-shrink: 0;
		line-height: 0;
	}

	.logo {
		width: auto;
		height: 36px;
	}

	.menu-toggle {
		display: none;
		align-items: center;
		justify-content: center;
		padding: var(--space-2);
		border: none;
		background: transparent;
		color: var(--color-white);
		cursor: pointer;
	}

	.menu-toggle svg {
		fill: currentColor;
	}

	.site-nav {
		flex: 1;
	}

	.nav-list {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0;
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.nav-list-item {
		position: relative;
	}

	.nav-item,
	:global(.nav-subitem) {
		display: inline-flex;
		align-items: center;
		gap: var(--space-1);
		padding: 13px 7px;
		font-family: var(--font-heading);
		font-size: var(--font-size-sm);
		font-weight: var(--font-weight-normal);
		text-transform: uppercase;
		text-decoration: none;
		color: var(--color-white);
		background: none;
		border: none;
		cursor: pointer;
		white-space: nowrap;
	}

	.nav-item:hover,
	:global(.nav-subitem:hover),
	.nav-item.is-active,
	:global(.nav-subitem.is-active) {
		text-decoration: none;
	}

	.nav-item::after,
	:global(.nav-subitem)::after {
		content: '';
		position: absolute;
		left: 7px;
		right: 7px;
		bottom: 8px;
		height: 3px;
		background-color: transparent;
		transition: background-color var(--transition-base);
	}

	.nav-list-item > .nav-item {
		position: relative;
	}

	.nav-item:hover::after,
	.nav-item.is-active::after {
		background-color: var(--color-white);
	}

	.chevron {
		fill: currentColor;
		transition: transform var(--transition-base);
	}

	.dropdown-open .chevron {
		transform: rotate(180deg);
	}

	.submenu {
		display: none;
		position: absolute;
		top: 100%;
		left: 0;
		min-width: 260px;
		margin: 0;
		padding: var(--space-2) 0;
		list-style: none;
		background-color: var(--color-theme);
		box-shadow: var(--shadow-md);
		z-index: 10;
	}

	.submenu.is-open {
		display: block;
	}

	.submenu li {
		margin: 0;
	}

	:global(.nav-subitem) {
		display: block;
		width: 100%;
		padding: var(--space-3) var(--space-4);
		position: relative;
	}

	:global(.nav-subitem:hover) {
		background-color: var(--color-dropdown-hover);
	}

	:global(.nav-subitem::after) {
		display: none;
	}

	@media (max-width: 1024px) {
		.menu-toggle {
			display: inline-flex;
		}

		.site-nav {
			display: none;
			position: absolute;
			top: 100%;
			left: 0;
			right: 0;
			background-color: var(--color-theme);
			border-top: 1px solid rgba(255, 255, 255, 0.12);
			padding: var(--space-4);
		}

		.site-nav.is-open {
			display: block;
		}

		.main-bar {
			position: relative;
		}

		.nav-list {
			flex-direction: column;
			align-items: stretch;
		}

		.nav-list-item {
			width: 100%;
		}

		.nav-item,
		:global(.nav-subitem) {
			width: 100%;
			justify-content: space-between;
			padding: var(--space-3) var(--space-2);
		}

		.submenu {
			position: static;
			box-shadow: none;
			padding-left: var(--space-4);
			background-color: rgba(0, 0, 0, 0.1);
		}
	}
</style>
