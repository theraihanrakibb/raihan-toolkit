# AI-Inference Repo Cheat-Sheet

Reference for the `ai-infra-helper` skill.

## SGLang (sgl-project/sglang)

### Layout
```
python/sglang/
├── srt/                  # SGLang runtime (server + scheduler)
│   ├── managers/
│   ├── model_executor/
│   └── models/           # per-model architecture files (add a new model here)
├── lang/                 # frontend language (SGLang DSL)
└── ...
test/srt/                 # runtime tests
.github/workflows/        # CI: pr-gate, pr-test-*, lint
.dockerignore  .gitignore  README.md  pyproject.toml
```

### Where common changes go
| Change | Likely file |
|---|---|
| Add a new model architecture | `python/sglang/srt/models/<arch>.py` |
| Tweak scheduler | `python/sglang/srt/managers/scheduler.py` |
| Server endpoint | `python/sglang/srt/entrypoints/` |
| Frontend DSL | `python/sglang/lang/` |

### Test / lint commands (minimal — run these before pushing)
```bash
# Lint — this is what actually gates your fork PR
pre-commit install
pre-commit run --all-files

# Targeted runtime test (much faster than the full suite)
pytest test/srt/test_<area>.py -k <test_name> -x
```

### Fork-PR CI behavior (IMPORTANT)
- **Fork PRs fail `pr-gate` / `pr-test-*` by design.** Those workflows need repo secrets the fork doesn't have. Do NOT spend cycles trying to make `pr-test-*` green — they will be neutral / skipped on merge.
- **Only `lint` actually gates your code.** Make `lint` green; that's the bar.
- Don't run the full `pytest test/srt/` locally just to satisfy fork-only CI — it's slow and most failures are infra, not your code.

## vLLM (vllm-project/vllm)

### Layout
```
vllm/
├── attention/
├── model_executor/models/    # per-model files (add a new model here)
├── engine/
├── entrypoints/
└── ...
tests/                        # tests
.format.sh  pyproject.toml
```

### Test / lint
```bash
./.format.sh                  # ruff + black + mypy (this is the gate)
pytest tests/<area>/test_x.py -k <name> -x
```

### Fork-PR CI behavior
- Similar to SGLang: fork PRs can't access GPU CI. Make `lint` + `ruff` green; that's the local bar.

## TensorRT-LLM
- C++ + Python hybrid. Lint via `bash docker/develop/docker-entrypoint.sh --lint`.
- Fork PRs to NVIDIA repos often need a CLA — check `CONTRIBUTING.md` before opening.

## General fork-PR checklist
1. `pre-commit run --all-files` (or `.format.sh` for vLLM) is green.
2. Targeted `pytest -k <name> -x` passes locally.
3. Commit message is Conventional Commit format.
4. PR description from `templates/pr-description.md`.
5. Push to your fork, not upstream.
