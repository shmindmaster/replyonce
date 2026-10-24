# Changelog

All notable changes to this project are documented here. This project follows
[Semantic Versioning](https://semver.org/).

## Unreleased

## 0.1.0 - 2026-10-23

First release.

- `once(key, effect)` with an effect ledger: `pending`, `committed`, `failed`, `ambiguous`.
- Keys from scope, intent and a canonical hash of the business identity; a stable provider
  idempotency key per effect.
- Runs with fencing tokens. `supersede` mode lets the newest context own the scope;
  `exclusive` mode allows one lease holder at a time, with takeover after expiry.
- Redelivery handling: the same `runId` resumes the run, fences earlier deliveries, and
  replays completed effects.
- Conversation fence: `conversation_changed` refusals with conflict details and an ack, with
  ordering by a logical clock, plus `contextAt` for snapshot-time context.
- Ambiguous outcomes are not retried; supports an optional reconciler and `resolve()`.
- Stores: memory, Postgres (row lock per scope) and Redis (Lua compare-and-set).
- Adapters: guarded tools with OpenAI and Anthropic tool shapes, a read-only
  `check_already_done` tool, a webhook handler with HTTP status mapping, and a BullMQ processor wrapper.
- `npx replyonce demo` chaos simulation.
