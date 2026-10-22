"""Pregătește modelul SmolLM2 135M pentru demo-ul din documentație (src/components/LlmChat.astro).

Descarcă de pe Hugging Face fișierele ONNX cuantizate pe 8 biți, la o revizie fixă, și mută ponderile modelului în
fișiere de date externe de cel mult 95 MB, pentru că GitHub nu acceptă fișiere mai mari de 100 MB. Transformers.js le
încarcă pe toate, în ordine: model_quantized.onnx_data, model_quantized.onnx_data_1 etc.

Rulare (o singură dată, rezultatul se versionează în public/modele/):

    python3 -m venv .venv && .venv/bin/pip install onnx
    .venv/bin/python scripts/prepare-model.py
"""

from __future__ import annotations

import argparse
import json
import shutil
import urllib.request
from pathlib import Path

import onnx
from onnx.external_data_helper import ExternalDataInfo, uses_external_data

REPO = 'onnx-community/SmolLM2-135M-Instruct-ONNX'
REVISION = 'b8a5c0f183b78c55955a5364f610c36668b5e681'
MODEL_FILE = 'onnx/model_quantized.onnx'
COPIED_FILES = ['generation_config.json', 'tokenizer.json', 'tokenizer_config.json']
ALIGNMENT = 4096
# Tensorii mai mici rămân în fișierul .onnx.
MIN_EXTERNAL_BYTES = 1024


def download(cache: Path) -> None:
    for name in ['config.json', MODEL_FILE, *COPIED_FILES]:
        target = cache / name
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        url = f'https://huggingface.co/{REPO}/resolve/{REVISION}/{name}'
        print(f'Descărcare {url}')
        urllib.request.urlretrieve(url, target)


def tensor_bytes(tensor: onnx.TensorProto, source_dir: Path) -> bytes | None:
    """Datele unui tensor, din fișierul extern sau din .onnx. None dacă tensorul rămâne în .onnx."""
    if uses_external_data(tensor):
        info = ExternalDataInfo(tensor)
        with open(source_dir / info.location, 'rb') as data_file:
            data_file.seek(info.offset or 0)
            return data_file.read(info.length)
    if len(tensor.raw_data) >= MIN_EXTERNAL_BYTES:
        return tensor.raw_data
    return None


def split_external_data(source: Path, target: Path, max_bytes: int) -> int:
    """Rescrie modelul cu ponderile în mai multe fișiere externe. Un tensor nu este împărțit între două fișiere."""
    model = onnx.load(source, load_external_data=False)
    chunk_names: list[str] = []
    chunk = None
    size = 0

    for tensor in model.graph.initializer:
        data = tensor_bytes(tensor, source.parent)
        if data is None:
            continue
        if len(data) > max_bytes:
            raise ValueError(f'Tensorul {tensor.name} ({len(data)} octeți) depășește limita unui fișier.')

        offset = -(-size // ALIGNMENT) * ALIGNMENT
        if chunk is None or offset + len(data) > max_bytes:
            if chunk:
                chunk.close()
            name = f'{target.name}_data' + (f'_{len(chunk_names)}' if chunk_names else '')
            chunk_names.append(name)
            chunk = open(target.parent / name, 'wb')
            size = offset = 0

        chunk.write(b'\0' * (offset - size))
        chunk.write(data)
        size = offset + len(data)

        tensor.ClearField('raw_data')
        tensor.data_location = onnx.TensorProto.EXTERNAL
        del tensor.external_data[:]
        for key, value in [('location', chunk_names[-1]), ('offset', offset), ('length', len(data))]:
            entry = tensor.external_data.add()
            entry.key, entry.value = key, str(value)

    if chunk:
        chunk.close()
    onnx.save_model(model, target)
    return len(chunk_names)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--cache', type=Path, default=Path('.cache/smollm2-135m-instruct'))
    parser.add_argument('--out', type=Path, default=Path('public/modele/smollm2-135m-instruct'))
    parser.add_argument('--max-mb', type=int, default=95)
    args = parser.parse_args()

    download(args.cache)
    shutil.rmtree(args.out / 'onnx', ignore_errors=True)
    (args.out / 'onnx').mkdir(parents=True)

    for name in COPIED_FILES:
        shutil.copyfile(args.cache / name, args.out / name)

    model_name = Path(MODEL_FILE).name
    chunks = split_external_data(args.cache / MODEL_FILE, args.out / 'onnx' / model_name, args.max_mb * 1_000_000)

    # Transformers.js află din config.json câte fișiere de date are modelul.
    config = json.loads((args.cache / 'config.json').read_text())
    config.setdefault('transformers.js_config', {})['use_external_data_format'] = {model_name: chunks}
    (args.out / 'config.json').write_text(json.dumps(config, indent=2) + '\n')

    for path in sorted((args.out / 'onnx').iterdir()):
        print(f'{path}: {path.stat().st_size / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
