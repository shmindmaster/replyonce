# Deployment

This is a library, not a hosted service.

- Node package `replyonce` on npm. `prepublishOnly` runs typecheck, build,
  test, and smoke. The release workflow is `.github/workflows/release.yml`.
- Python package `replyonce` from `python/`. The release workflow is
  `.github/workflows/release-python.yml`.
- CI on every push and pull request builds the images and runs the suites.
  There is no staging server and no production container to promote.

Rollback of a published version is a new release. Rollback of `main` is
`git revert`.
