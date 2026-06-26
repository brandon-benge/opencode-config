# OpenCode Agent Profiles

These are inactive OpenCode-ready agent profiles for this repository's
SpecRepo workflow. They are kept outside `.opencode/agents/` so you can review
them before enabling them.

## Enable

Copy the agent files you want into:

```text
.opencode/agents/
```

Example:

```bash
mkdir -p .opencode/agents
cp opencode-agent-profiles/agents/*.md .opencode/agents/
```

OpenCode uses the Markdown filename as the agent name. For example,
`spec-reviewer.md` becomes `@spec-reviewer`.

## Recommended Workflow

1. Put a request in `specrepo/requests/`.
2. Ask `@spec-reviewer` to create the architecture proposal.
3. Review the proposal yourself.
4. Ask `@architecture-approver` for an approval-readiness review.
5. When you approve, create or ask for an approval record in
   `specrepo/approved/`.
6. Ask `@implementation-reviewer` to create the pre-code implementation review.
7. Use `spec-coder` to implement within the approved scope.
8. Ask `@test-reviewer` to review test coverage and verification evidence.

## Files

| File | Purpose |
| --- | --- |
| `agents/spec-reviewer.md` | Turns requests into architecture proposals. |
| `agents/architecture-approver.md` | Reviews proposals before human approval. |
| `agents/implementation-reviewer.md` | Reviews approved architecture before code changes. |
| `agents/spec-coder.md` | Implements only after approval and implementation review exist. |
| `agents/test-reviewer.md` | Reviews tests and verification evidence. |
| `agents.yaml` | Consolidated YAML reference for the agent frontmatter. |

## Permission Notes

The profiles use conservative write permissions. Agents that may need to write
use `edit: ask` so you can approve the actual edit. The prompt body still
contains the repository-specific path restrictions.

If your OpenCode version supports reliable path-scoped edit permissions, you can
tighten each profile further after copying it into `.opencode/agents/`.
