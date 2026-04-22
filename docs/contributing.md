# Workflow

Even solo projects benefit from a disciplined workflow — future-you is a
separate developer from present-you.

## Branches

- `main` — always buildable, always passes `pytest`.
- `feat/<thing>` — new feature (one per sensor/module).
- `fix/<thing>` — bug fixes.
- `docs/<thing>` — doc-only changes.

Never commit directly to `main`. Always branch → PR → merge, even when
solo. Forces you to review your own diff and keeps the history clean.

## Commit messages

Short imperative subject line (≤ 50 chars), blank line, body if needed:

```
Accelerometer: add LIS3DH bus init

Wires up smbus2 reads to the OUT_X/Y/Z registers with the
sensitivity from the datasheet table 4. Calibration still TODO.
```

## Before pushing

```bash
ruff format .
ruff check --fix .
pytest
```

If any of those fail, fix it before pushing. Set up a pre-commit hook later
if you want this automated.

## Decision log

Non-trivial architectural decisions go in `docs/decisions/` as short
markdown files (one per decision). This is a lightweight ADR pattern.
Stops you from forgetting *why* you did something.
