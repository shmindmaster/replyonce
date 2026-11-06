# Security

The library holds idempotency state, not customer content, unless a caller
puts that content in the payload it asks the store to remember. Keep payloads
to the identity the effect needs (order id, message id, amount).

- Store URLs and passwords stay in the environment. The compose file uses
  the local development password `postgres` for the throwaway database only.
- Do not commit `.env` files.
- A stale fencing token must fail closed. Do not add a path that writes
  after `superseded`.
- An ambiguous timeout must not be retried as if it were a clean failure.
- The published packages have no runtime network calls of their own. Postgres
  and Redis clients connect only where the caller points them.
