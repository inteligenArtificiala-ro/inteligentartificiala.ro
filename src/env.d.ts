interface Window {
  dataLayer: unknown[];
  gtag: (...args: unknown[]) => void;
  gaLoaded?: boolean;
}
