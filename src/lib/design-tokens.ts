/** Design tokens extracted from the WordPress / Elementor site. */

export const colors = {
	theme: '#0DA272',
	themeHover: '#0ACD8E',
	overlay: '#1C393D',
	surface: '#EFEFEE',
	white: '#FFFFFF',
	black: '#000000',
	muted: '#747373',
	inputPlaceholder: '#A3A2A2',
	link: '#0DA272',
	footerLink: '#000000',
	footerLinkHover: '#00000091',
	dropdownHover: '#0ACD8E73',
} as const;

export const fonts = {
	body: "'Lora', Georgia, serif",
	heading: "'Open Sans', system-ui, sans-serif",
	topBar: "'Barlow Semi Condensed', system-ui, sans-serif",
} as const;

export const fontSizes = {
	xs: '0.8125rem', // 13px
	sm: '0.9375rem', // 15px
	base: '1rem', // 16px
	md: '1.125rem', // 18px
	lg: '1.25rem',
	xl: '1.5rem',
	'2xl': '2rem',
	'3xl': '3rem',
	hero: '3rem',
} as const;

export const fontWeights = {
	normal: '400',
	semibold: '600',
	bold: '700',
} as const;

export const lineHeights = {
	tight: '1.2',
	snug: '1.35',
	normal: '1.6',
	relaxed: '1.75',
} as const;

export const spacing = {
	0: '0',
	1: '0.25rem',
	2: '0.5rem',
	3: '0.75rem',
	4: '1rem',
	5: '1.25rem',
	6: '1.5rem',
	8: '2rem',
	10: '2.5rem',
	12: '3rem',
	15: '3.75rem', // 60px section padding
	16: '4rem',
	20: '5rem',
	24: '6rem',
} as const;

export const layout = {
	maxWidth: '1480px',
	contentPadding: '1.25rem',
	heroMinHeight: '980px',
	heroMinHeightMd: '600px',
	headerLogoWidth: '90px',
	headerLogoWidthSticky: '60px',
	subtitleLineWidth: '40px',
	subtitleLineOffset: '65px',
} as const;

export const radii = {
	none: '0',
	sm: '2px',
	md: '4px',
	lg: '8px',
	full: '9999px',
} as const;

export const shadows = {
	sm: '0 1px 2px rgba(0, 0, 0, 0.06)',
	md: '0 4px 12px rgba(0, 0, 0, 0.1)',
	lg: '-5px 4px 23px 41px rgba(0, 0, 0, 0.2)',
} as const;

export const breakpoints = {
	sm: '640px',
	md: '768px',
	lg: '1024px',
	xl: '1280px',
} as const;

export const transitions = {
	fast: '150ms ease',
	base: '300ms ease',
	slow: '500ms ease',
} as const;

export type ColorToken = keyof typeof colors;
export type FontToken = keyof typeof fonts;
