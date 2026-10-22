# inteligentartificiala.ro

Documentation in Romanian about artificial intelligence, from basic concepts to the implementation of large language models. Built with [Astro](https://astro.build), [Starlight](https://starlight.astro.build) and the [Exquisitus](https://github.com/anaxite/starlight-theme-exquisitus) theme.

```bash
npm install
npm run dev          # http://localhost:4321
npm run dev:search   # build + preview, with search working
npm run build        # dist/ + search index
npm run check        # types and lint
```

## Labs and Colab notebooks

Every lab has Jupyter notebooks in `public/laboratoare/<lab>/notebooks/`. Google Colab opens them straight from this repository's `main` branch, and the site links to them from each lab page.

| Lab | Notebook | Colab |
| --- | --- | --- |
| [Un model de limbaj local cu Transformers](https://inteligentartificiala.ro/laboratoare/model-local-transformers/prezentare/) | Introducere | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/model-local-transformers/notebooks/01-prezentare.ipynb) |
|  | Tokenizatorul, modelul și generarea | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/model-local-transformers/notebooks/02-tokenizator-si-generare.ipynb) |
|  | Memorie, dispozitive și cuantizare | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/model-local-transformers/notebooks/03-memorie-si-dispozitive.ipynb) |
|  | Un model de raționament local | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/model-local-transformers/notebooks/04-model-de-rationament.ipynb) |
| [Imagini și sunete cu modele de difuzie](https://inteligentartificiala.ro/laboratoare/difuzie-imagini-si-sunete/prezentare/) | Introducere | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/difuzie-imagini-si-sunete/notebooks/01-prezentare.ipynb) |
|  | Procesul de difuzie, pas cu pas | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/difuzie-imagini-si-sunete/notebooks/02-procesul-de-difuzie.ipynb) |
|  | De la text la imagine | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/difuzie-imagini-si-sunete/notebooks/03-imagini-din-text.ipynb) |
|  | Sunete din text | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/difuzie-imagini-si-sunete/notebooks/04-sunete-din-text.ipynb) |
| [Un model de limbaj de la zero (mvGPT)](https://inteligentartificiala.ro/laboratoare/model-lingvistic-de-la-zero/prezentare/) | Tot laboratorul | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/model-lingvistic-de-la-zero/notebooks/mvgpt.ipynb) |
| [Control continuu cu PPO în MuJoCo](https://inteligentartificiala.ro/laboratoare/control-continuu-ppo-halfcheetah/prezentare/) | Tot laboratorul | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inteligentArtificiala-ro/inteligentartificiala.ro/blob/main/public/laboratoare/control-continuu-ppo-halfcheetah/notebooks/ppo-halfcheetah.ipynb) |

The notebooks of the first two labs are generated from the code blocks of the lab pages, so changes go into the pages, not into the notebooks. The mvGPT and PPO notebooks run those labs' scripts.

- Licenses: [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md)

Every push to `main` is published automatically to GitHub Pages (`.github/workflows/deploy.yml`).
