# Development

Git, Docker, and an editor are enough.

```text
docker compose run --build --rm test
docker compose run --rm typecheck
docker compose run --build --rm python
```

`test` runs Vitest. `typecheck` is `tsc --noEmit`. `python` is
`uv run pytest -q` in the Python image. Rebuild when `package.json`,
`package-lock.json`, `python/pyproject.toml`, or `python/uv.lock` changes.
Source and tests are mounted read-only, so an ordinary edit does not reinstall
dependencies.

Postgres 16 and Redis 7 start with the test services. The URLs are set in
`compose.yaml`. They are local to the compose project.

Do not create `node_modules`, `dist`, or `python/.venv` in the checkout.
`npm run build` (tsup) stays inside the image when a release needs `dist/`.
