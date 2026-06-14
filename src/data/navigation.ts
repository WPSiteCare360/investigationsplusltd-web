export type NavItem = {
	label: string;
	href: string;
	children?: NavItem[];
};

export const siteConfig = {
	name: 'Investigation Plus',
	legalName: 'Investigations Plus LTD',
	tagline: 'Constantly challenging ourselves to deliver more to our clients',
	phone: '1-888-703-2912',
	phoneHref: 'tel:18887032912',
	email: 'info@investigationsplusltd.com',
	copyright: `Copyright ${new Date().getFullYear()} All Rights Reserved`,
} as const;

export const mainNav: NavItem[] = [
	{ label: 'Home', href: '/' },
	{ label: 'About', href: '/private-investigation-about' },
	{
		label: 'Services',
		href: '/private-investigators-services',
		children: [
			{ label: 'All Services', href: '/private-investigators-services' },
			{
				label: 'Infidelity Investigation',
				href: '/private-investigators-services/infidelity-investigation',
			},
			{
				label: 'Bug Sweeping Services & TSCM Toronto',
				href: '/private-investigators-services/bug-sweeping-services-tscm',
			},
			{
				label: 'Legal Services',
				href: '/private-investigators-services/legal-services',
			},
		],
	},
	{ label: 'Blog', href: '/blog' },
	{
		label: 'Collaboration',
		href: '/private-investigation-experts-collaboration',
	},
	{
		label: 'Contact',
		href: '/contact',
		children: [
			{ label: 'Toronto', href: '/contact#toronto' },
			{ label: 'Brampton', href: '/contact#brampton' },
			{ label: 'Vaughan', href: '/contact#vaughan' },
			{ label: 'Richmond Hill', href: '/contact#richmond-hill' },
			{ label: 'Mississauga', href: '/contact#mississauga' },
			{ label: 'Markham', href: '/contact#markham' },
		],
	},
];

export const socialLinks = [
	{
		label: 'Facebook',
		href: 'https://www.facebook.com/Investigations-Plus-Ltd-437465893286965/',
	},
	{
		label: 'YouTube',
		href: 'https://www.youtube.com/channel/UCdRNZ4VPvY2nDj6sXzseCPg',
	},
	{
		label: 'X (Twitter)',
		href: 'https://twitter.com/piplus3?s=03',
	},
	{
		label: 'Instagram',
		href: 'https://www.instagram.com/investigationsplusltd/',
	},
	{
		label: 'LinkedIn',
		href: 'https://www.linkedin.com/in/investigations-plus-ltd-99759b140/',
	},
] as const;
