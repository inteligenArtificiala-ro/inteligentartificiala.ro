# Third-party notices

## Starlight and the Exquisitus theme

- [Starlight](https://github.com/withastro/starlight) (`@astrojs/starlight`), MIT, © Astro contributors. Installed as a dependency.
- [starlight-theme-exquisitus](https://github.com/anaxite/starlight-theme-exquisitus), MIT, © Anaxite. Installed as a dependency. It provides the site's base visual style, adjusted in `src/styles/custom.css`.

The full license texts are included in the packages (`node_modules/@astrojs/starlight/LICENSE`, `node_modules/starlight-theme-exquisitus/LICENSE`).

## Fonts

All fonts are distributed under the [SIL Open Font License 1.1](https://openfontlicense.org):

- **Source Sans 3** and **Source Serif 4**, © Adobe, installed via `@fontsource-variable` and served from the site's own domain. They are the site's interface and reading typefaces. Static copies in `assets/fonts/` (licenses in `OFL-SourceSans3.txt` and `OFL-SourceSerif4.txt`) are used only to generate the Open Graph image.
- **JetBrains Mono**, bundled by the Exquisitus theme via `@fontsource` and served from the site's own domain, for code. The theme also bundles **Literata** and **Alegreya Sans**, which the site no longer uses.
- **Archivo Black** (`assets/fonts/`), © 2017 The Archivo Black Project Authors. The license is in `assets/fonts/OFL-ArchivoBlack.txt`. No longer used.

## Runnable Python examples

- [PyScript](https://github.com/pyscript/pyscript) (`@pyscript/core`), Apache-2.0, © Anaconda, Inc. and PyScript contributors. Installed as a dependency and served from the site's domain (copied to `public/pyscript/` at build time). The license is in `node_modules/@pyscript/core/LICENSE`.
- [Pyodide](https://github.com/pyodide/pyodide), MPL-2.0. Not distributed by this site: PyScript loads it from cdn.jsdelivr.net when a reader runs an example.

## In-browser language model demo

- [Transformers.js](https://github.com/huggingface/transformers.js) (`@huggingface/transformers`), Apache-2.0, © Hugging Face. Installed as a dependency and bundled into the demo's Web Worker. The license is in `node_modules/@huggingface/transformers/LICENSE`.
- [ONNX Runtime Web](https://github.com/microsoft/onnxruntime) (`onnxruntime-web`), MIT, © Microsoft Corporation. Installed as a dependency of Transformers.js. Its WebAssembly files are served from the site's domain (copied to `public/onnxruntime/` at build time).
- **SmolLM2-135M-Instruct**, Apache-2.0, © Hugging Face, in the ONNX conversion by [onnx-community](https://huggingface.co/onnx-community/SmolLM2-135M-Instruct-ONNX), stored in `public/modele/smollm2-135m-instruct/`. The folder contains a copy of the license (`LICENSE`) and a `README.md` listing the files modified by this project.

## Google Colab button

- The **Google Colab** logo in `src/components/Colab.astro` is a trademark of Google LLC, drawn from the official "Open in Colab" badge and used only to link the lab notebooks to Colab. The page loads nothing from Google; a reader reaches Colab only by clicking the link. The README uses the official badge image.

## Lab: Imagini și sunete cu modele de difuzie

The models are not distributed by this site. Readers download them from Hugging Face Hub when they run the code.

- [google/ddpm-cat-256](https://huggingface.co/google/ddpm-cat-256), Apache-2.0.
- [Stable Diffusion 1.5](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5), CreativeML OpenRAIL-M.
- [AudioLDM 2](https://huggingface.co/cvssp/audioldm2), CC BY-NC-SA 4.0.

## Lab: Un model lingvistic de la zero

- **mvGPT** code (`public/laboratoare/model-lingvistic-de-la-zero/cod/`), MIT, © 2026 mvGPT maintainers, from [github.com/nenuadrian/mvGPT](https://github.com/nenuadrian/mvGPT). Copied with comments and printed messages translated into Romanian.
- **TinyStories** and **TinyStories-Instruct** samples (`public/laboratoare/model-lingvistic-de-la-zero/date/`), by Ronen Eldan and Yuanzhi Li ([roneneldan/TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories), [roneneldan/TinyStoriesInstruct](https://huggingface.co/datasets/roneneldan/TinyStoriesInstruct)). TinyStories is licensed [CDLA-Sharing-1.0](https://cdla.dev/sharing-1-0/). TinyStories-Instruct declares no license on its dataset card. It is the same authors' instruction version of TinyStories' stories, and the site serves only 60 of its documents. `povesti.txt` holds the first 300 stories of `TinyStoriesV2-GPT4-train.txt` and `instructiuni.txt` 60 documents from the start of `TinyStories-Instruct-valid.txt`, unchanged. The full sets are downloaded by readers from Hugging Face, not served by this site.
