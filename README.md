# Reusable opencode Configuration For SpecRepo

This directory is a reusable opencode configuration bundle for repositories
that use the SpecRepo workflow.

Keep this directory portable. It should define opencode agents, conservative
permissions, reusable prompts, and workflow guidance. It should not contain a
specific product name, package path, source root, test root, verification
command, runtime config path, approval record, request, proposal, or
implementation review.

Repository-specific facts belong in the target repository's `specrepo/`
directory. Agents should read `specrepo/spec.yaml`, `specrepo/workflow.md`, the
baseline specs, and the active request/proposal/approval/review records before
acting.

If a repository does not have `specrepo/` yet, use `@specrepo-bootstrapper`.
It creates the complete structure from the reusable templates in
`opencode-config/templates/specrepo/` and tailors the baseline specs to the
target repository. It also creates or updates a repository-root `AGENTS.md`
that points agents at the generated SpecRepo workflow.

## Enable Markdown Profiles

Copy the agent files you want into:

```text
.opencode/agents/
```

Example:

```bash
mkdir -p .opencode/agents
cp agents/*.md .opencode/agents/
```

opencode uses the Markdown filename as the agent name. For example,
`spec-reviewer.md` becomes `@spec-reviewer`.

## Repository Fact Source

Reusable agents must discover local project facts from SpecRepo:

| Fact | Source |
| --- | --- |
| Project metadata | `specrepo/spec.yaml` |
| Source roots | `specrepo/spec.yaml` `source_roots` |
| Test roots | `specrepo/spec.yaml` `test_roots` |
| Default verification | `specrepo/spec.yaml` `commands.test` |
| Workflow gates | `specrepo/workflow.md` |
| Product, architecture, and quality expectations | `specrepo/specs/` |
| Active decisions | `specrepo/requests/`, `specrepo/proposals/`, `specrepo/approved/`, `specrepo/implementation-reviews/` |

## Configuration Files

Both root configuration files are for opencode:

| File | Role |
| --- | --- |
| `opencode.jsonc` | Root JSONC opencode configuration for the `plan` and `build` agents plus watcher behavior. |
| `opencode.yaml` | YAML opencode agent configuration for SpecRepo workflow agents. It centralizes each agent's description, mode, temperature, permissions, and tool access in one file. |

`opencode.yaml` defines the workflow agents referenced below:
`specrepo-bootstrapper`, `request-author`, `spec-reviewer`,
`architecture-approver`, `implementation-reviewer`, `spec-coder`, and
`test-reviewer`.

`opencode.jsonc` configures two opencode agents:

| Agent | Purpose |
| --- | --- |
| `plan` | Low-temperature planning agent with a 3-step limit and write/edit tools disabled. |
| `build` | Low-temperature build agent with a 10-step limit. |

It also configures the watcher to ignore generic generated or noisy paths such
as VCS internals and build outputs.

## Recommended Workflow

1. If the target repository has no `specrepo/`, ask `@specrepo-bootstrapper`
   to create it.
2. Ask `@request-author` to create or refine a request in
   `specrepo/requests/`.
3. Ask `@spec-reviewer` to create the architecture proposal.
4. Review the proposal yourself.
5. Ask `@architecture-approver` for an approval-readiness review.
6. When you approve, create or ask for an approval record in
   `specrepo/approved/`.
7. Ask `@implementation-reviewer` to create the pre-code implementation review.
8. Use `@spec-coder` to implement within the approved scope.
9. Ask `@test-reviewer` to review test coverage and verification evidence.

## Files

| File | Purpose |
| --- | --- |
| `agents/specrepo-bootstrapper.md` | Creates a complete repo-specific SpecRepo structure and root `AGENTS.md` from reusable templates. |
| `agents/request-author.md` | Creates or refines feature requests before architecture work begins. |
| `agents/spec-reviewer.md` | Turns requests into architecture proposals. |
| `agents/architecture-approver.md` | Reviews proposals before human approval. |
| `agents/implementation-reviewer.md` | Reviews approved architecture before code changes. |
| `agents/spec-coder.md` | Implements only after approval and implementation review exist. |
| `agents/test-reviewer.md` | Reviews tests and verification evidence. |
| `templates/specrepo/` | Reusable template pack for generating a repo-specific `specrepo/` directory. |
| `opencode.yaml` | YAML opencode agent configuration for the SpecRepo workflow agents. |
| `opencode.jsonc` | Root opencode config for the `plan` and `build` agents plus watcher ignores. |

## Permission Notes

The profiles use conservative write permissions. Agents that may need to write
use `edit: ask` so you can approve the actual edit.

The reusable default only allows low-risk repository inspection commands. Keep
verification commands repository-specific: read them from SpecRepo artifacts or
add local allowlists after copying the config into a target repository.

If your opencode version supports reliable path-scoped edit permissions, you can
tighten each profile further after copying it into `.opencode/agents/`.
