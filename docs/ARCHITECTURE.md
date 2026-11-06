# Architecture

Two libraries, one state machine.

| Path | Owns |
| --- | --- |
| `src/logic.ts` | Fencing, once-only effects, ambiguous outcomes |
| `src/replyonce.ts` | `createReplyOnce` and conversation runs |
| `src/stores/` | Memory, Postgres, Redis |
| `src/adapters/` | Tool-call loops, webhooks, BullMQ |
| `src/cli.ts` | `replyonce demo` |
| `python/src/replyonce/` | The same machine for asyncio workers |
| `examples/` | Quickstart, agent loop, webhook, Postgres, BullMQ |
| `infra/docker/` | The Node 22 and Python 3.12 images |

A run holds a fencing token for one conversation. A newer run or a redelivery
takes the token, and the old run's writes are refused. An effect is stored
under the business identity (the order, the message), not under a tool-call
id. A timeout after the provider may have acted is `ambiguous` until a
reconciler or a person resolves it.

Node and Python persist the same state format so they can share one Postgres
or Redis store.
