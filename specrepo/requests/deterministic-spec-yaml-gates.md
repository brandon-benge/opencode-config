# Feature Request: Deterministic SpecRepo Gates With Verifiable Conditions

Status: requested
Date: 2026-07-09
Requester: brandonbenge

## Summary

The `templates/specrepo/spec.yaml` template defines `required_gates` as bare
strings (e.g. `request_file_exists`, `current_specs_read`) and `states` as
unadorned names. Neither section links to file-system evidence, spec sections,
or verifiable conditions. This request adds a deterministic gate schema so that
agents can check, enforce, and report gate status without guesswork.

## Problem

When a repository is bootstrapped with the current template, the generated
`specrepo/spec.yaml` contains gates like these:

```yaml
required_gates:
  before_architecture_update:
    - request_file_exists
    - current_specs_read
  before_implementation:
    - approved_architecture_exists
    - implementation_review_exists
    - test_plan_exists
  before_close:
    - tests_run_or_exception_recorded
    - specs_updated_if_behavior_changed
```

An agent reading this file has no way to determine:

- **What constitutes "passing"** for `request_file_exists` — which file at which
  path should exist? What if multiple request files exist?
- **What threshold satisfies** `current_specs_read` — does it mean all four
  baseline specs were read, or just that the directory was listed?
- **What maps** `test_plan_exists` to — is it a section in the proposal, a
  standalone file, or a field in the implementation review?

Similarly, the `states` list has no entry criteria, exit criteria, or
artifact requirements. An agent cannot answer "is this state valid given the
current files on disk?"

Without deterministic gate definitions, agents must rely on human judgment or
convention, which defeats the purpose of an automated SpecRepo workflow.

## Desired Behavior

After this change, the generated `specrepo/spec.yaml` defines each gate with:

1. **A unique gate name** (as today).
2. **A path condition** — a file-glob or directory-existence check that
   determines pass/fail deterministically (e.g. `specrepo/requests/*.md`).
3. **An optional spec reference** — a pointer to the baseline spec section that
   elaborates on the gate's intent (e.g. `quality.md §Required Coverage Areas`).
4. **An optional description** clarifying what the gate requires in prose.

Each state transition can also declare which gates must pass before entering or
exiting that state.

The concrete template change should look something like this (illustrative):

```yaml
required_gates:
  request_file_exists:
    description: >
      At least one feature-request file must exist in the request inbox before
      architecture work begins.
    check:
      type: file_exists
      pattern: "specrepo/requests/*.md"
    spec_ref: workflow.md §Request Intake
  current_specs_read:
    description: >
      All four baseline specs (product, architecture, quality, glossary) must
      exist and have been read by the spec-reviewer agent.
    check:
      type: files_exist
      pattern:
        - specrepo/specs/product.md
        - specrepo/specs/architecture.md
        - specrepo/specs/quality.md
        - specrepo/specs/glossary.md
    spec_ref: workflow.md §Architecture Proposal
  approved_architecture_exists:
    description: >
      An approval record must exist under specrepo/approved/ before
      implementation can begin.
    check:
      type: glob_exists
      pattern: "specrepo/approved/*/approval.md"
    spec_ref: workflow.md §Automatic Approval
  implementation_review_exists:
    description: >
      An implementation review must exist confirming the approved architecture
      is implementable.
    check:
      type: glob_exists
      pattern: "specrepo/implementation-reviews/*.md"
    spec_ref: workflow.md §Coding-Agent Architecture Review
  test_plan_exists:
    description: >
      The approved architecture proposal or implementation review must contain
      a test plan section.
    check:
      type: section_exists_in_files
      pattern:
        - "specrepo/proposals/*/architecture.md"
        - "specrepo/implementation-reviews/*.md"
      section_heading: "## Test Plan"
    spec_ref: quality.md §Test Strategy
  tests_run_or_exception_recorded:
    description: >
      Either the default verification command has been run and passed, or a
      recorded exception explains why it could not run.
    check:
      type: command_run_or_exception
      command_ref: commands.test
      exception_file_pattern: "specrepo/implementation-reviews/*.md"
    spec_ref: quality.md §Test Strategy
  specs_updated_if_behavior_changed:
    description: >
      If the implementation changed user-visible behavior, the baseline specs
      must have been updated to match.
    check:
      type: git_diff_or_spec_statement
      spec_ref: quality.md §Documentation Rules
```

States should declare entry and exit gates:

```yaml
states:
  - name: requested
    entry_gates: []
    exit_gates: [request_file_exists]
    artifacts_required: []
  - name: architecture_proposed
    entry_gates: [request_file_exists, current_specs_read]
    exit_gates: [approved_architecture_exists]
    artifacts_required:
      - "specrepo/proposals/*/architecture.md"
  - name: approved
    entry_gates: [approved_architecture_exists]
    exit_gates: [implementation_review_exists]
    artifacts_required:
      - "specrepo/approved/*/approval.md"
  - name: implementation_reviewed
    entry_gates: [approved_architecture_exists, implementation_review_exists, test_plan_exists]
    exit_gates: []
    artifacts_required:
      - "specrepo/implementation-reviews/*.md"
  - name: implementing
    entry_gates: [approved_architecture_exists, implementation_review_exists]
    exit_gates: []
    artifacts_required: []
  - name: verified
    entry_gates: [tests_run_or_exception_recorded]
    exit_gates: [specs_updated_if_behavior_changed]
    artifacts_required: []
  - name: closed
    entry_gates: [specs_updated_if_behavior_changed]
    exit_gates: []
    artifacts_required: []
```

The existing flat `required_gates` list would be replaced by the above
structured schema, making the template backward-incompatible for existing
`specrepo/spec.yaml` files — but the change is scoped to the template, so only
newly bootstrapped repos are affected. Existing repos can migrate at their own
pace.

## Acceptance Criteria

1. The `templates/specrepo/spec.yaml` template defines each gate with a unique
   name, a `check` block specifying a `type` and deterministically evaluable
   condition, and an optional `spec_ref`.
2. Each state in `states` declares `entry_gates` (gates that must pass to enter)
   and `exit_gates` (gates that must pass to leave), plus optional
   `artifacts_required` file patterns.
3. The `required_gates` section has an explicit `$schema` or inline documentation
   so that agents know how to evaluate each `check.type`.
4. File-glob-based check types (`file_exists`, `files_exist`, `glob_exists`) are
   simple to evaluate — an agent can run `test -f <path>` or `ls <glob>` to
   determine pass/fail.
5. Content-based check types (`section_exists_in_files`, `command_run_or_exception`,
   `git_diff_or_spec_statement`) are documented with clear evaluation rules so
   an agent can determine pass/fail deterministically.
6. The `workflow.md` template is updated to reference the structured gate
   definitions rather than the flat gate names.
7. The `templates/specrepo/specs/product.md`, `architecture.md`, `quality.md`,
   and `glossary.md` are updated where needed to include sections referenced
   by `spec_ref` in the gate definitions (e.g. `quality.md` gets the
   `§Documentation Rules` anchor).
8. The `@specrepo-bootstrapper` agent produces `specrepo/spec.yaml` with the
   structured gate schema when bootstrapping a new repository.

## Constraints

- **Backward-compatible template only** — the change is to `templates/specrepo/`
  files. Existing `specrepo/` directories in other repos are not migrated
  automatically. A future separate request could introduce a migration command.
- **Check types must be evaluable by an agent without external tooling** beyond
  `test`, `ls`, `git diff`, and grep-like content matching.
- **The `$schema` or inline documentation must live inside the template**
  itself, not in an external file, so bootstrapped repos are self-contained.
- **No new programming language runtime** — the gate checks must be evaluable
  via shell commands and file-system operations available in any POSIX-like
  environment.
- **The `agent_policy` section** may also need structured enforcement rules, but
  that is explicitly deferred to a separate request (non-goal below).

## Non-Goals

- Adding a runtime validator binary or script for gate evaluation.
- Migrating existing bootstrapped `specrepo/` directories to the new schema.
- Enforcement hooks or CI actions that reject branches based on gate status.
- Changes to the approval-record, implementation-review, or implementation-plan
  templates beyond what is needed to link back to gate definitions.
- Adding machine-readable `agent_policy` enforcement — the booleans remain
  advisory.

## Impacted Areas

- Public API: unknown
- CLI: no
- Config: yes — `templates/specrepo/spec.yaml` gate schema changes
- External integrations: no
- Data/storage behavior: unknown
- Tests/docs: yes — `templates/specrepo/workflow.md`, baseline spec templates

## Notes

The `feature-development.md`, `feature-development-lifecycle.mmd`, and
`states-and-gates.mmd` files in this repo document the intended workflow and
may need to be updated to reflect the new structured gates. Those changes are
within scope of the architecture proposal but are not part of this request's
acceptance criteria.

The existing `required_gates` field in the template is a flat list of strings:
```yaml
required_gates:
  before_architecture_update:
    - request_file_exists
    - current_specs_read
```

The new schema replaces this with a structured map keyed by gate name and a
`states` list with `entry_gates`/`exit_gates`. The illustrative YAML above is
the intended shape; the `@spec-reviewer` may adjust field names and nesting
during the architecture proposal.
