export const contactSeo = {
	title: 'Contact Investigations Plus | Private Investigators GTA',
	description:
		'Contact Investigations Plus for a free, confidential consultation. Licensed private investigators serving Toronto, Brampton, Vaughan, Markham, Mississauga, Richmond Hill, and all of Ontario. Available 24/7.',
};

export const contactHero = {
	subtitle: 'Get in touch',
	titleHtml: '<b>Contact</b> Investigations Plus',
	image: '/images/uploads/2022/07/hire-us-for-work1.jpg',
};

export const contactIntro =
	'Investigations Plus Ltd. is a licensed private investigation agency incorporated, bonded, and insured under Ontario law. We provide discreet, professional investigative services across the GTA and beyond -- locally, Canada-wide, and internationally. Time matters in investigations; contact us today for immediate assistance.';

export const contactDetails = {
	hours: '24/7',
	email: 'info@investigationsplusltd.com',
	tollFree: '1-888-703-2912',
	tollFreeHref: 'tel:18887032912',
	gtaPhone: '(647) 703-2912',
	gtaPhoneHref: 'tel:16477032912',
	googleBusiness: 'https://maps.app.goo.gl/Nt2WMdKYpbJtSsJP6',
	coverage: 'Greater Toronto Area, Ontario, Canada-wide, and international assignments',
} as const;

export type Office = {
	id: string;
	name: string;
	address: string;
	phone: string;
	phoneHref: string;
	image: string;
	imageAlt: string;
};

export const offices: Office[] = [
	{
		id: 'brampton',
		name: 'Brampton Office',
		address: '10 George St North, Suite 137, Brampton, ON, L6X 1R2',
		phone: '1 (888) 703-2912, (647) 703-2912 (GTA)',
		phoneHref: 'tel:18887032912',
		image:
			'/images/uploads/2024/05/Contact-Investigation-Plus-Private-Investigator-Brampton_Dominion_Building.jpg',
		imageAlt: 'Investigations Plus Brampton office at Dominion Building',
	},
	{
		id: 'toronto',
		name: 'Toronto Office',
		address: '1682 Eglinton Ave W, Toronto, ON, M6E 2H5',
		phone: '(647) 703-2912 (GTA)',
		phoneHref: 'tel:16477032912',
		image:
			'/images/uploads/2024/05/Contact-Toronto-Location-Featured-Investigation-Plus-Private-Investigator-Toronto-Brampton.jpg',
		imageAlt: 'Financial District at Downtown Toronto, Ontario',
	},
];

export type ServiceArea = {
	id: string;
	city: string;
	summary: string;
	image: string;
	imageAlt: string;
};

export const serviceAreas: ServiceArea[] = [
	{
		id: 'toronto',
		city: 'Toronto',
		summary:
			'Discreet investigative services in Toronto and across the GTA, Ontario, and Canada. We respond effectively to urgent matters including missing persons, fraud, surveillance, and electronic surveillance threats.',
		image:
			'/images/uploads/2024/05/Contact-Toronto-Location-Featured-Investigation-Plus-Private-Investigator-Toronto-Brampton.jpg',
		imageAlt: 'Toronto skyline and Financial District',
	},
	{
		id: 'brampton',
		city: 'Brampton',
		summary:
			'The private investigation company Brampton residents and businesses trust for answers, proof, and peace of mind. Corporate fraud, insurance fraud, background checks, and personal matters handled with strict confidentiality.',
		image:
			'/images/uploads/2024/05/Contact-Investigation-Plus-Private-Investigator-Brampton_Dominion_Building.jpg',
		imageAlt: 'Investigations Plus Brampton office',
	},
	{
		id: 'vaughan',
		city: 'Vaughan',
		summary:
			'Professional, discreet, and results-oriented services for individuals, businesses, insurance companies, and legal professionals throughout Vaughan.',
		image: '/images/uploads/2025/10/Vaughans.webp',
		imageAlt: 'Vaughan, Ontario',
	},
	{
		id: 'markham',
		city: 'Markham',
		summary:
			'Investigative services tailored for individuals and businesses in Markham, covering surveillance, background checks, fraud investigation, missing persons, and corporate inquiries.',
		image: '/images/uploads/2025/10/Markham.webp',
		imageAlt: 'Markham, Ontario',
	},
	{
		id: 'mississauga',
		city: 'Mississauga',
		summary:
			'Investigators serving private individuals, companies, and solicitors in Mississauga with cutting-edge technology, precision, and utmost discretion.',
		image: '/images/uploads/2025/10/Mississauga.webp',
		imageAlt: 'Mississauga, Ontario',
	},
	{
		id: 'richmond-hill',
		city: 'Richmond Hill',
		summary:
			'Professional and discreet investigative services in Richmond Hill for individuals, corporate clients, and legal matters including surveillance and missing-person locates.',
		image: '/images/uploads/2025/10/Richmond-Hill.webp',
		imageAlt: 'Richmond Hill, Ontario',
	},
];

export const formLocations = [
	{ value: '', label: 'Select a location' },
	{ value: 'toronto', label: 'Toronto' },
	{ value: 'brampton', label: 'Brampton' },
	{ value: 'vaughan', label: 'Vaughan' },
	{ value: 'markham', label: 'Markham' },
	{ value: 'mississauga', label: 'Mississauga' },
	{ value: 'richmond-hill', label: 'Richmond Hill' },
	{ value: 'other', label: 'Other / General inquiry' },
] as const;

export const investigationServices = [
	{
		label: 'Bug Sweeping Services / TSCM',
		href: '/private-investigators-services/bug-sweeping-services-tscm',
	},
	{
		label: 'Infidelity Investigations',
		href: '/private-investigators-services/infidelity-investigation',
	},
	{ label: 'Surveillance and Monitoring', href: '/private-investigators-services' },
	{ label: 'Background Checks and Due Diligence', href: '/private-investigators-services' },
	{ label: 'Insurance and Fraud Investigations', href: '/private-investigators-services' },
	{ label: 'Corporate and Workplace Investigations', href: '/private-investigators-services' },
	{
		label: 'Legal Support',
		href: '/private-investigators-services/legal-services',
	},
	{ label: 'Missing Persons and Locates', href: '/private-investigators-services' },
	{ label: 'Electronic Counter-Surveillance', href: '/private-investigators-services' },
];

export const whyChooseUs = [
	'Licensed and insured -- incorporated, bonded, and compliant with Ontario regulations.',
	'Experienced team with backgrounds in military, legal, forensic, IT, cyber, radio, and psychological fields.',
	'Technology-driven -- advanced surveillance tools, GPS, and specialized TSCM expertise.',
	'Confidential -- every case treated with strict privacy.',
	'Available 24/7 for time-sensitive matters.',
	'Trusted by insurance companies, law firms, corporations, and private clients across Ontario.',
];

/** Legacy location URLs redirect to anchors on this page. */
export const legacyLocationRedirects: Record<string, string> = {
	'/private-investigator-toronto-ontario': '/contact#toronto',
	'/private-investigator-brampton-ontario': '/contact#brampton',
	'/private-investigator-vaughan-ontario': '/contact#vaughan',
	'/private-investigator-markham-ontario': '/contact#markham',
	'/private-investigator-mississauga-ontario': '/contact#mississauga',
	'/private-investigator-richmond-hill-ontario': '/contact#richmond-hill',
};
