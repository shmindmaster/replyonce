# Operations

## Demo

Inside the Node image, after `npm run build`:

```text
node dist/cli.js demo --conversations 100 --seed 7
```

A duplicate reply fails the demo. That is the production signal the library
exists to prevent.

## Local databases

`docker compose down` stops Postgres and Redis. Their data is not a named
volume in this project, so it does not accumulate. Do not point compose at
a database that holds real customer effects.

## Image cleanup

Tags are `replyonce-node:local` and `replyonce-python:local`. Remove them
with `docker image rm` when you want the disk back. Do not prune volumes
that belong to another compose project.

## When a write is refused

`superseded` means a newer run owns the conversation. `redelivered_after_write`
means the effect already happened. `ended` means the run is closed. Treat
those as success-shaped skips, not as a reason to call the provider again.
