# Contributing

Thanks for helping. replyonce is small on purpose. The bar for a change is whether it keeps
a duplicate effect from reaching a customer, or makes an honest limit clearer.

## Setup

```sh
git clone https://github.com/shmindmaster/replyonce
cd replyonce
npm install
npm run typecheck && npm run build && npm test
```

Node 22 or newer is needed to develop (the build tools require it). The published package
supports Node 18+, and CI checks the built output on 18 and 20.

### Postgres and Redis tests

The suites run against every store whose URL is set:

```sh
docker run -d --rm --name ro-pg -e POSTGRES_PASSWORD=postgres -p 55432:5432 postgres:17-alpine
docker run -d --rm --name ro-redis -p 56379:6379 redis:7-alpine
REPLYONCE_PG_URL=postgres://postgres:postgres@localhost:55432/postgres \
REPLYONCE_REDIS_URL=redis://localhost:56379 npm test
```

Without those variables, only the memory store is tested. CI always runs all three.

## Ground rules

- **The state machine stays pure.** All decisions live in `src/logic.ts` as functions from
  state to state. Stores only make `transact` atomic. Do not put decision logic in a store.
- **Every bug fix comes with a test that fails without it.** For a race, add it to
  `test/race.test.ts` or as a fault in the chaos demo (`src/demo.ts`). It must pass against
  all three stores.
- **No runtime dependencies.** Stores take structural clients (`pg.Pool`-like, `eval`-capable).
- **The public API is small and stable.** New options need a clear failure they prevent.
  Breaking changes wait for a major version.
- **Claims match tests.** If a change affects a guarantee or a limit, update the README in
  the same pull request.
- **Generic examples only.** No real customer, company or personal data in code, tests or docs.

## Pull requests

1. Open an issue first for anything larger than a fix.
2. Keep commits focused. CI must be green: typecheck, build, tests on three stores, the chaos
   demo, the examples, and smoke tests on Node 18 and 20.
3. Add a line to `CHANGELOG.md` under "Unreleased".

By contributing, you agree that your contributions are licensed under the Apache License 2.0.
