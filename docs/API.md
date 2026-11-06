# API

Node import: `createReplyOnce` and `MemoryStore` from `replyonce`.
Postgres and Redis stores are exported from `replyonce/postgres` and
`replyonce/redis`. Adapters are `replyonce/adapters`.

`once({ scope, intent, payload }, fn)` runs `fn` at most once for that
scope and intent. A race returns `executed` for the winner and `in_flight`
or `replayed` for the rest.

A conversational run is one inbound message or one queue job. Customer-visible
writes go through that run. The run refuses the write when its fencing token
is stale or when another reply landed after it read the conversation.

Python: `replyonce` on PyPI (package name `replyonce`, import `replyonce`).
The console script is `replyonce demo`.

CLI, after a build inside the image: `replyonce demo --conversations 100
--seed 7`. `FORCE_COLOR=1` keeps the demo colours when output is piped.

The effect status values callers branch on are `executed`, `replayed`,
`in_flight`, and the refusal reasons surfaced by the adapters (`ended`,
`redelivered_after_write`, `superseded`).
