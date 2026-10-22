import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import { CITARE } from './consts';

// Paginile de documentație (cele cu nivel) se încheie cu secțiunea „Cum citați această pagină”, afișată de
// src/components/starlight/Footer.astro. Secțiunea nu face parte din Markdown, așa că o adăugăm aici în cuprins.
export const onRequest = defineRouteMiddleware(({ locals }) => {
  const { entry, toc } = locals.starlightRoute;
  if (entry.data.level && toc) {
    toc.items.push({ depth: 2, slug: CITARE.id, text: CITARE.titlu, children: [] });
  }
});
