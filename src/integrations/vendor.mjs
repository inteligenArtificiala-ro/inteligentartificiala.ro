// @ts-check

import { cp, readFile, rm } from 'node:fs/promises';
import { basename, join } from 'node:path';
import { fileURLToPath } from 'node:url';

/**
 * Fișiere din node_modules servite de pe domeniul site-ului, în public/<director>/<versiune>/. Calea include versiunea,
 * ca după o actualizare browserele să nu combine fișiere vechi și noi. Directoarele sunt ignorate de git.
 */
const PACKAGES = [
  // PyScript, pentru editoarele Python (src/components/Python.astro).
  { name: '@pyscript/core', directory: 'pyscript', include: (/** @type {string} */ file) => !file.endsWith('.map') },
  // ONNX Runtime pentru WebAssembly, folosit de Transformers.js în demo-ul cu model lingvistic (src/components/LlmChat.astro).
  {
    name: 'onnxruntime-web',
    directory: 'onnxruntime',
    include: (/** @type {string} */ file) => /^ort-wasm-simd-threaded(\.asyncify)?\.(mjs|wasm)$/.test(file),
  },
];

/** @returns {import('astro').AstroIntegration} */
export default function vendor() {
  return {
    name: 'vendor',
    hooks: {
      'astro:config:setup': async ({ config, logger }) => {
        for (const { name, directory, include } of PACKAGES) {
          const packageDir = fileURLToPath(new URL(`node_modules/${name}/`, config.root));
          const { version } = JSON.parse(await readFile(join(packageDir, 'package.json'), 'utf8'));
          const source = join(packageDir, 'dist');
          const target = fileURLToPath(new URL(`${directory}/`, config.publicDir));

          await rm(target, { recursive: true, force: true });
          await cp(source, join(target, version), {
            recursive: true,
            filter: (path) => path === source || include(basename(path)),
          });
          logger.info(`${name} ${version} copiat în public/${directory}/${version}/`);
        }
      },
    },
  };
}
