# replyonce

Library that stops an agent from replying, refunding, or ticketing twice.
Node package at the repo root. Python port in `python/` with the same state
machine. There is no application server and no `apps/` tree.

## Commands

```text
docker compose run --build --rm test
docker compose run --rm typecheck
docker compose run --build --rm python
```

`test` is Vitest against memory, Postgres, and Redis. Postgres and Redis are
compose services. Do not install Node, Python, or a virtual environment on
the host, and do not create `node_modules` or `python/.venv` in the checkout.

## Rules

- An effect is keyed by the business identity, never by the model's wording
  or a tool-call id.
- A stale run must not write. Unknown outcomes stay `ambiguous`.
- Store URLs come from the environment. Do not commit them.
- The nearest `AGENTS.md` adds local rules. The root file still applies.

## Done

The three compose commands pass. Docs in `docs/` match the change. Commit.
Publishing to npm or PyPI is a separate release workflow.
