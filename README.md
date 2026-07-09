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

## Install From Scratch

opencode reads its user configuration from `~/.config/opencode`. To use this
repository as your reusable opencode configuration, clone it somewhere stable
and make `~/.config/opencode` a symlink to the clone.

Example macOS setup:

```bash
PWD_LOCAL=$(pwd)
git clone https://github.com/brandon-benge/opencode-config.git opencode-config

if [ -e ~/.config/opencode ] && [ ! -L ~/.config/opencode ]; then
  mv ~/.config/opencode ~/.config/opencode.backup
fi

ln -sfn ${PWD_LOCAL}/opencode-config ~/.config/opencode
```

Verify the link:

```bash
ls -l ~/.config/opencode
```

Expected shape:

```text
~/.config/opencode -> /Users/<you>/Desktop/GitProjects/opencode-config
```

After this, opencode can find the root config files in this repository:
`opencode.yaml` and `opencode.jsonc`.

If you already have an opencode configuration, review it before replacing the
directory. Move any local settings you want to keep into this repository, or
keep the backup created above at `~/.config/opencode.backup`.

## Agent Discovery

opencode automatically loads agent `.md` profiles from
`~/.config/opencode/agents/`. Since `~/.config/opencode` is a symlink to this
repository, every agent file under [`agents/`](./agents/) is immediately
available as an opencode agent (for example `agents/architecture-approver.md`
becomes `@architecture-approver`).

Agents are also registered in [`opencode.yaml`](./opencode.yaml), which defines
each agent's mode, temperature, permissions, and tool access. The YAML
configuration and the markdown profiles work together — the YAML sets the
agent's runtime properties and the markdown file provides its system prompt.

No additional setup or file copying is required after the symlink installation.

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

Primary agents chain to subagents automatically. You only need to call the
primary agents; handoffs happen in the background.

1. If the target repository has no `specrepo/`, ask `@specrepo-bootstrapper`
   to create it.
2. Ask `@request-author` to create or refine a request in
   `specrepo/requests/`. It automatically delegates to `@spec-reviewer`
   (architecture proposal) then `@architecture-approver` (review and approval
   record creation).
3. Review the proposal and architecture-approver recommendation. If satisfied,
   ask `@spec-coder` to implement. If not, stop here.
4. `@spec-coder` automatically delegates to `@implementation-reviewer` if
   needed, implements, runs verification, then chains to `@test-reviewer`
   for a test-coverage review.
5. Review the implementation summary and git diff. Merge when ready.

You never need to call `@spec-reviewer`, `@architecture-approver`,
`@implementation-reviewer`, or `@test-reviewer` directly. Call only
`@request-author` and `@spec-coder`.

📊 [Feature Development Lifecycle](feature-development-lifecycle.mmd) —
end-to-end flowchart.
📊 [Agent Responsibility Map](agent-responsibility-map.mmd) — agent roles and
auto-chain groups.
📊 [States And Gates](states-and-gates.mmd) — workflow state machine.

See [`feature-development.md`](feature-development.md) for full details and
prompt templates.

## Files

| File | Purpose |
| --- | --- |
| `agents/specrepo-bootstrapper.md` | Creates a complete repo-specific SpecRepo structure and root `AGENTS.md` from reusable templates. |
| `agents/request-author.md` | Creates or refines feature requests before architecture work begins. |
| `agents/spec-reviewer.md` | Turns requests into architecture proposals. |
| `agents/architecture-approver.md` | Reviews proposals and creates approval records automatically. |
| `agents/implementation-reviewer.md` | Reviews approved architecture before code changes. |
| `agents/spec-coder.md` | Implements only after approval and implementation review exist. |
| `agents/test-reviewer.md` | Reviews tests and verification evidence. |
| `specrepo-autocommit` | Finalization hook run by `@spec-coder` after required verification passes; blocks on `main` and chooses credentials from `OPENCODE_API_KEY` or Keychain. |
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
tighten each profile further after placing a copy in `.opencode/agents/` of a
target repository.
