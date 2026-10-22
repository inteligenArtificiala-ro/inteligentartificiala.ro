import { defineCollection } from 'astro:content';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { LEVELS, type Level } from './consts';

// Câmpuri suplimentare pentru paginile de documentație (opționale, ca paginile simple să nu aibă nevoie de ele).
const docFields = z.object({
  pubDate: z.coerce.date().optional(),
  authors: z.array(z.string()).optional(),
  tags: z.array(z.string()).optional(),
  level: z.enum(Object.keys(LEVELS) as [Level, ...Level[]]).optional(),
});

const docs = defineCollection({
  loader: docsLoader(),
  schema: docsSchema({ extend: docFields }),
});

// Textele interfeței Starlight, ajustate după WRITING-STYLE-GUIDE.md.
const i18n = defineCollection({ loader: i18nLoader(), schema: i18nSchema() });

const contributori = defineCollection({
  loader: glob({ pattern: '*.{yaml,yml}', base: './src/content/contributori' }),
  schema: z.object({
    name: z.string(),
    url: z.url(),
    role: z.string().optional(),
    bio: z.string().optional(),
  }),
});

export const collections = { docs, i18n, contributori };
