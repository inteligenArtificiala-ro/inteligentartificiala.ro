export const SITE = {
  name: 'InteligentArtificiala.ro',
  description:
    'Documentație în limba română despre inteligența artificială, de la conceptele de bază până la implementarea modelelor de limbaj mari (LLM).',
  url: 'https://inteligentartificiala.ro',
  email: 'contact@inteligentartificiala.ro',
  // Autorul implicit al paginilor (date structurate și citare), dacă pagina nu are câmpul `authors`.
  author: { name: 'Adrian Mircea Nenu', url: 'https://nenuadrian.com' },
  locale: 'ro-RO',
  lang: 'ro',
  repo: 'https://github.com/inteligentArtificiala-ro/inteligentartificiala.ro',
  googleAnalyticsId: 'G-C5RGL9RXDT',
} as const;

export const LEVELS = {
  incepator: 'Începător',
  intermediar: 'Intermediar',
  avansat: 'Avansat',
} as const;

export type Level = keyof typeof LEVELS;

// Secțiunea de la sfârșitul paginilor de documentație (src/components/Citare.astro), cu intrarea ei din cuprins
// (src/route-data.ts).
export const CITARE = { id: 'citare', titlu: 'Cum citați această pagină' } as const;
