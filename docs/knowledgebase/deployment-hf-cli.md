# Hugging Face CLI Deployment Runbook

Use `hf` where practical. Do not paste tokens into source files.

## Checks

```bash
hf auth whoami
hf env
hf cache ls
```

## Create Or Reuse A Gradio Space

```bash
hf repos create ImageEZGen3D --repo-type space --space-sdk gradio --exist-ok
```

## Dry-Run Model Downloads

```bash
hf download tencent/Hunyuan3D-2.1 --dry-run
hf cache verify tencent/Hunyuan3D-2.1
```

## Upload App

```bash
hf upload YOUR_USERNAME/ImageEZGen3D . . --repo-type=space --exclude='/outputs/*' --exclude='/.env*' --commit-message='Deploy ImageEZGen3D'
```

`requirements.txt` intentionally delegates to `-e .[app]` so Hugging Face Spaces installs dependencies from `pyproject.toml`.

## ZeroGPU Notes

- ZeroGPU requires Gradio Spaces.
- GPU work must be behind `@spaces.GPU`.
- Default GPU duration is 60 seconds; specify longer only when needed.
- `torch.compile` is not supported on ZeroGPU.
- Larger GPU size consumes more quota.
- The app default is `auto`: use ZeroGPU first, then CPU only when ZeroGPU cannot be used.
