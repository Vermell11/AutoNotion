# Claude Code instructions

Read and follow `AGENTS.md`, then `PROJECT_CONTEXT.md`.

Before changing code:

1. Read the Obsidian project summary, current state, and last closed session referenced
   by `PROJECT_CONTEXT.md`.
2. Query the existing Graphify graph for architecture and relationships.
3. Inspect the repository and preserve local work.

Do not query Notion for routine context. Notion is the structured session ledger and
metrics/API layer; write its closing row only after Obsidian, Graphify, tests, commit
and version tag are ready.

At session close, update Obsidian, `PROJECT_CONTEXT.md`, Graphify and the Git version,
then create a new Notion session row with timestamps, duration, hours, challenge,
result, summary, tag and commit.
