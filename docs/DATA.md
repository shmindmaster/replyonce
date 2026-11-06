# Data

No database ships inside the library. Callers choose a store.

| Store | Where state lives |
| --- | --- |
| `MemoryStore` | Process memory. Tests and the demo default. |
| Postgres | Tables created by `PostgresStore.migrate`. URL `REPLYONCE_PG_URL` or `DATABASE_URL`. |
| Redis | Keys at `REPLYONCE_REDIS_URL` or `REDIS_URL`. |

The stored record is the effect ledger: scope, intent, payload identity,
fencing token, status, and the ambiguous-outcome mark. Node and Python write
the same shape. Do not change a field without a migration test in both trees.

The demo does not persist. Postgres and Redis in `compose.yaml` are empty
local databases for the suite, and they are discarded with the compose
project. There is no customer dataset in this repository.
