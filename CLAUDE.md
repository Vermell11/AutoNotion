# Claude Code instructions

Read and follow `AGENTS.md`, then `PROJECT_CONTEXT.md`.

Before changing code:

1. Treat `PROJECT_CONTEXT.md` only as a minimal index.
2. Read the global rules, project rules, project summary, current state, and last
   closed session referenced there, plus `Sesiones/En curso.md` when present.
3. Query the existing Graphify graph for architecture and relationships.
4. Inspect the repository and preserve local work.

Do not query Notion for routine context. Notion is the structured session ledger and
metrics/API layer; write its closing row only after Obsidian, Graphify, tests, commit
and version tag are ready.

Completing a task does not close the session. Before executing the closing workflow,
wait until the user explicitly says they want to close or load the session into
Notion. Then show the proposed closing summary and explicitly ask whether the user
confirms closing and registering it. Without an unambiguous affirmative response, keep
the session open and do not create or update a Notion session row.

After confirmation, update Obsidian, `PROJECT_CONTEXT.md`, Graphify and the Git version,
then create one new Notion session row with timestamps, duration, hours, challenge,
result, summary, tag and commit.

Keep the Obsidian in-progress session note updated after material agreements or
changes. At confirmed close, convert it into the dated version note instead of keeping
two divergent copies.
