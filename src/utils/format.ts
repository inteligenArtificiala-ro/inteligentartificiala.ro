// Regula lui „de” (WRITING-STYLE-GUIDE.md §2): 1 pagină, 2 pagini, 19 pagini, 20 de pagini, 101 pagini, 120 de pagini.
export const pluralize = (n: number, singular: string, plural: string): string => {
  if (n === 1) return `1 ${singular}`;
  const de = n !== 0 && (n % 100 >= 20 || n % 100 === 0);
  return de ? `${n} de ${plural}` : `${n} ${plural}`;
};
