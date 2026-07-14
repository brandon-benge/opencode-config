# Reusable opencode Configuration For SpecRepo

This directory is a reusable opencode configuration bundle for repositories
that use the SpecRepo workflow.

Keep this directory portable. It should define opencode agents, conservative
permissions, reusable prompts, and workflow guidance. It should not contain a
specific product name, package path, source root, test root, verification
command, runtime config path, approval record, request, proposal, or
implementation review.

Repository-specific facts belong in the target repository's `AGENTS.md` and
`specrepo/` directory. Agents should read `AGENTS.md`, the baseline specs, and
the active request/proposal/approval/review records before acting.

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

After this, opencode can find `opencode.jsonc`, prompts, and skills in this
repository.

If you already have an opencode configuration, review it before replacing the
directory. Move any local settings you want to keep into this repository, or
keep the backup created above at `~/.config/opencode.backup`.

## Agent Configuration

Agents are defined in [`opencode.jsonc`](./opencode.jsonc), which is the single
source of truth for each agent's description, mode, temperature, permissions,
skill access, and tool access. Their system prompts live in
[`prompts/`](./prompts/) as standalone `.txt` files referenced via the
`prompt: "{file:...}"` field.

For example, `opencode.jsonc` defines `@architecture-approver` and loads its
prompt from `prompts/architecture-approver.txt`. No additional setup or file
copying is required after the symlink installation.

Reusable procedures live in [`skills/`](./skills/). OpenCode loads them on
demand through the native skill tool, and `opencode.jsonc` grants each agent
only the skills it needs.

## Repository Fact Source

Reusable agents must discover local project facts from SpecRepo:

| Fact | Source |
| --- | --- |
| Project metadata | Repository-root `AGENTS.md` |
| Source roots | Repository-root `AGENTS.md` |
| Test roots | Repository-root `AGENTS.md` |
| Default verification | Repository-root `AGENTS.md` and `specrepo/specs/quality.md` |
| Workflow gates | `AGENTS.md`, prompts, and SpecRepo skills |
| Product, architecture, quality, and glossary expectations | `specrepo/specs/` |
| Active decisions | `specrepo/requests/`, `specrepo/proposals/`, `specrepo/approved/`, `specrepo/implementation-reviews/` |

## Configuration Files

Both root configuration files are for opencode:

| File | Role |
| --- | --- |
| `opencode.jsonc` | Root JSONC opencode configuration for built-in agents, SpecRepo workflow agents, permissions, skill access, and watcher behavior. |

`opencode.jsonc` defines the workflow agents referenced below:
`specrepo-bootstrapper`, `request-author`, `spec-reviewer`,
`architecture-approver`, `implementation-reviewer`, `spec-coder`, and
`test-reviewer`.

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
📊 [States And Gates](states-and-gates.mmd) — simplified state machine
(see [Feature Development Lifecycle](feature-development-lifecycle.mmd) for
full branching flow with decision gates).

See [`feature-development.md`](feature-development.md) for full details and
prompt templates.

## Files

| File | Purpose |
| --- | --- |
| `opencode.jsonc` | Root opencode config for agents, permissions, skill access, and watcher ignores. |
| `prompts/` | System prompt `.txt` files loaded by each agent via the `prompt: "{file:...}"` field in `opencode.jsonc`. |
| `skills/` | Reusable opencode skills loaded on demand by specific agents. |
| `specrepo-autocommit` | Finalization hook run by `@spec-coder` after required verification passes; blocks on `main` and chooses credentials from `OPENCODE_API_KEY` or Keychain. |
| `templates/specrepo/` | Reusable template pack for generating a repo-specific `specrepo/` directory. |

## Permission Notes

The profiles use conservative write permissions. Agents that may need to write
use `edit: ask` so you can approve the actual edit.

The reusable default only allows low-risk repository inspection commands. Keep
verification commands repository-specific: read them from SpecRepo artifacts or
add local allowlists after copying the config into a target repository.

If your opencode version supports reliable path-scoped edit permissions, you can
tighten each profile further in `opencode.jsonc`.

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `AUTOCOMMIT_PARAMS` | Optional path to a YAML parameters file passed as `--config-file` to the `autocommit` CLI. If unset, only `-c <summary>` is used. See [example params.yaml](https://github.com/brandon-benge/langchain_autocommit/blob/main/params.yaml). |
