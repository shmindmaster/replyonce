# Testing

```text
docker compose run --build --rm test
docker compose run --rm typecheck
docker compose run --build --rm python
```

Node tests live in `test/` and use Vitest. Postgres migration tests run when
`REPLYONCE_PG_URL` is set, which compose does. The CLI demo test skips until
`dist/` exists, because `tsup` output is a release artifact, not a source file.

Python tests live in `python/tests/` and use pytest. They cover the same
once, race, run, adapter, key, and migration behaviour.

CI (`.github/workflows/ci.yml`) runs those compose commands on Ubuntu.
The image is the runtime under test. A change to store behaviour needs both
suites.
