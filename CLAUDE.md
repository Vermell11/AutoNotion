# Claude Code instructions

Read and follow `AGENTS.md`, then `PROJECT_CONTEXT.md`.

Before changing code:

1. Treat `PROJECT_CONTEXT.md` only as a minimal index.
2. Read the global rules, project rules, project summary, current state, and last
   closed session referenced there, plus `Sesiones/En curso.md` when present.
3. Query the existing Graphify graph for architecture and relationships.
4. Inspect the repository and preserve local work.
5. For coding work, activate Ponytail when available. After tracing the real flow,
   prefer no new code, existing project code, the standard library, native platform
   features, installed dependencies, and finally the smallest working change.

Before closing a meaningful code change, run a Ponytail complexity review when the
skill is available. Never simplify away security, trust-boundary validation,
data-loss prevention, accessibility, explicit requirements, or the smallest useful
check.

Do not query Notion for routine context. Notion is the structured session ledger and
metrics/API layer.

Completing a task does not close the session. Before executing the closing workflow,
wait until the user explicitly says they want to close or load the session into
Notion. Then show the proposed closing summary and explicitly ask whether the user
confirms closing and registering it. Without an unambiguous affirmative response, keep
the session open and do not create or update a Notion session row.

After confirmation, finish Obsidian, `PROJECT_CONTEXT.md`, Graphify and tests, then
create the final commit. Build the JSON payload outside the repository with the full
commit SHA and run `scripts/notion.py close-session --payload <path> --dry-run`.
Do not tag or publish when preflight fails. When it passes, create the local annotated
tag, run the connector without `--dry-run`, require `status=completed`, and only then
publish main and the tag.

Keep the Obsidian in-progress session note updated after material agreements or
changes. At confirmed close, convert it into the dated version note instead of keeping
two divergent copies.
