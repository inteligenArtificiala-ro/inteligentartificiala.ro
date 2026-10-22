// Rulează modelul lingvistic din demo (src/components/LlmChat.astro) într-un Web Worker, ca pagina să rămână fluidă.
// Modelul și ONNX Runtime sunt servite de pe domeniul site-ului, deci nu se trimit date către terți.
import {
  env,
  InterruptableStoppingCriteria,
  type Message,
  type ProgressInfo,
  pipeline,
  type TextGenerationPipeline,
  TextStreamer,
} from '@huggingface/transformers';

export type WorkerRequest =
  | { type: 'load'; bytes: number }
  | { type: 'generate'; messages: Message[] }
  | { type: 'stop' };

export type WorkerResponse =
  | { type: 'progress'; loaded: number }
  | { type: 'ready'; device: 'webgpu' | 'wasm' }
  | { type: 'token'; text: string }
  | { type: 'done' }
  | { type: 'error'; message: string };

const MODEL = 'smollm2-135m-instruct';

// Fișierele modelului sunt în public/modele/ (pregătite cu scripts/prepare-model.py).
env.allowRemoteModels = false;
env.allowLocalModels = true;
env.localModelPath = '/modele/';

// Fișierele trec pe lângă cache-ul HTTP al browserului: în ferestrele private, acesta e păstrat în memorie și refuză
// fișierele de zeci de MB, iar refuzul oprește descărcarea. Pentru vizitele următoare, Transformers.js le păstrează
// în Cache Storage.
env.fetch = (input, init) => fetch(input, { ...init, cache: 'no-store' });

// ONNX Runtime este copiat în public/onnxruntime/<versiune>/ de src/integrations/vendor.mjs. Ca Transformers.js,
// se folosește varianta „asyncify”, cu excepția Safari mai vechi de 26 fără WebGPU.
const onnx = env.backends.onnx;
if (onnx.wasm) {
  const base = `/onnxruntime/${onnx.versions?.web}/ort-wasm-simd-threaded`;
  const safari = /Version\/(\d+)[\d.]* (Mobile\/\S+ )?Safari/.exec(navigator.userAgent);
  const suffix = safari && Number(safari[1]) < 26 && !('gpu' in navigator) ? '' : '.asyncify';
  onnx.wasm.wasmPaths = { mjs: `${base}${suffix}.mjs`, wasm: `${base}${suffix}.wasm` };
}

let generator: TextGenerationPipeline | undefined;
const stopping = new InterruptableStoppingCriteria();

const post = (message: WorkerResponse) => self.postMessage(message);

async function load(bytes: number) {
  // Fișierele rămân în Cache Storage doar dacă browserul are loc pentru ele (o fereastră privată are o cotă mică).
  // Altfel, o scriere eșuată în cache ar opri chiar descărcarea.
  const { quota = 0, usage = 0 } = (await navigator.storage?.estimate?.().catch(() => undefined)) ?? {};
  env.useBrowserCache = quota - usage > bytes * 1.5;
  env.useWasmCache = env.useBrowserCache;

  // Progresul se însumează pe fișiere. Totalul vine de la pagină, pentru că nu toate răspunsurile au Content-Length.
  const loaded = new Map<string, number>();

  const gpu = (navigator as Navigator & { gpu?: { requestAdapter(): Promise<unknown> } }).gpu;
  const device = (await gpu?.requestAdapter().catch(() => null)) ? 'webgpu' : 'wasm';

  generator = (await pipeline('text-generation', MODEL, {
    dtype: 'q8',
    device,
    progress_callback: (info: ProgressInfo) => {
      if (info.status !== 'progress') return;
      loaded.set(info.file, info.loaded);
      post({ type: 'progress', loaded: [...loaded.values()].reduce((sum, value) => sum + value, 0) });
    },
  })) as TextGenerationPipeline;

  post({ type: 'ready', device });
}

async function generate(messages: Message[]) {
  if (!generator) throw new Error('Modelul nu este încărcat.');
  stopping.reset();
  const streamer = new TextStreamer(generator.tokenizer, {
    skip_prompt: true,
    skip_special_tokens: true,
    callback_function: (text: string) => post({ type: 'token', text }),
  });
  // Valorile recomandate în descrierea modelului SmolLM2 (temperature 0.2, top_p 0.9).
  await generator(messages, {
    max_new_tokens: 256,
    do_sample: true,
    temperature: 0.2,
    top_p: 0.9,
    repetition_penalty: 1.1,
    streamer,
    stopping_criteria: stopping,
  });
  post({ type: 'done' });
}

self.addEventListener('message', async (event: MessageEvent<WorkerRequest>) => {
  const request = event.data;
  try {
    if (request.type === 'load') await load(request.bytes);
    else if (request.type === 'generate') await generate(request.messages);
    else stopping.interrupt();
  } catch (error) {
    post({ type: 'error', message: error instanceof Error ? error.message : String(error) });
  }
});
