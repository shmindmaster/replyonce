# Integrations

| Integration | Role |
| --- | --- |
| Postgres | Shared store. Node uses `pg`. Python uses `psycopg` 3. |
| Redis | Shared store. Node uses `ioredis`. Python uses `redis`. |
| BullMQ | Queue adapter. A redelivered job is skipped or refused when the effect already landed. |
| Webhooks | Adapter treats a second delivery of the same business event as the same effect. |
| Tool calls | Adapters accept OpenAI and Anthropic tool-call shapes. The idempotency key is not the tool-call id. |

Environment variables read by the suite and the examples:

- `REPLYONCE_PG_URL`
- `REPLYONCE_REDIS_URL`
- `DATABASE_URL`
- `REDIS_URL`

Compose sets them to the `postgres` and `redis` services. A host shell does
not need them.
