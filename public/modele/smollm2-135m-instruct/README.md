# SmolLM2 135M Instruct, ONNX, 8-bit

Model used by the in-browser demo on the page „Modele de limbaj mari (LLM)” (`src/components/LlmChat.astro`).

- **Model:** SmolLM2-135M-Instruct, by Hugging Face ([HuggingFaceTB/SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)).
- **Source of these files:** the ONNX conversion [onnx-community/SmolLM2-135M-Instruct-ONNX](https://huggingface.co/onnx-community/SmolLM2-135M-Instruct-ONNX), revision `b8a5c0f183b78c55955a5364f610c36668b5e681`, variant `q8` (`model_quantized.onnx`).
- **License:** Apache License 2.0. A copy is in `LICENSE`.

## Modified files

These files were modified by inteligentartificiala.ro with `scripts/prepare-model.py`:

- `onnx/model_quantized.onnx` and `onnx/model_quantized.onnx_data*`: the weights are unchanged, but they were moved out of the original single 136 MB `model_quantized.onnx` into external data files of at most 95 MB each, because GitHub does not accept files larger than 100 MB.
- `config.json`: `transformers.js_config.use_external_data_format` was set to the number of data files.

`generation_config.json`, `tokenizer.json` and `tokenizer_config.json` are unmodified copies.
