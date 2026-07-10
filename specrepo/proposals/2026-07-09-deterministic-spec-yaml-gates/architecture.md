# Architecture Proposal: Deterministic SpecRepo Gates With Verifiable Conditions

Status: awaiting_approval
Date: 2026-07-09
Request: `specrepo/requests/deterministic-spec-yaml-gates.md`

## Summary

Replace the flat string-list `required_gates` and bare `states` in
`templates/specrepo/spec.yaml` with a structured schema where each gate has a
deterministic `check` block (file-glob, content-match, or command-run
condition), each state declares `entry_gates` and `exit_gates`, and the
template includes inline documentation so bootstrapped repos are self-describing
and agent-evaluable.

## Current Architecture

The template at `templates/specrepo/spec.yaml` defines gates and states as
unadorned lists:

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

states:
  - requested
  - architecture_proposed
  - awaiting_approval
  - approved
  - implementation_reviewed
  - implementing
  - verified
  - closed
```

The workflow at `templates/specrepo/workflow.md` references these gate names in
prose but provides no mechanism for an agent to evaluate them. Baseline specs
(`product.md`, `architecture.md`, `quality.md`, `glossary.md`) are
placeholders with no sections that gates can reference.

The `@specrepo-bootstrapper` agent copies these placeholders verbatim when
bootstrapping a new repo. The resulting `specrepo/spec.yaml` is equally
non-deterministic.

## Proposed Architecture

### Change 1: Structured gate schema in `templates/specrepo/spec.yaml`

Replace the flat `required_gates` mapping with a structured map keyed by gate
name. Replace the flat `states` list with a list that includes `entry_gates`,
`exit_gates`, and `artifacts_required`.

**Gate schema:**

Each gate becomes a map entry with three optional fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `description` | string | yes | Prose explaining the gate's intent |
| `check` | map | yes | A `type` + `pattern` (and optionally `section_heading`, `command_ref`, or `exception_file_pattern`) defining the deterministic evaluation |
| `spec_ref` | string | no | Pointer to the spec that elaborates on this gate (e.g. `workflow.md §Request Intake`) |

**Check types:**

| `type` value | Required extra fields | Evaluation rule |
|---|---|---|
| `file_exists` | `pattern`: single file-glob string | Pass if at least one file matching the glob exists |
| `files_exist` | `pattern`: list of file-glob strings | Pass if every file/glob in the list matches at least one existing file |
| `glob_exists` | `pattern`: single glob string | Pass if the glob expands to at least one path |
| `section_exists_in_files` | `pattern`: list of file-globs; `section_heading`: string | Pass if any file matching any glob contains a line matching the section heading (case-sensitive, exact match after optional whitespace) |
| `command_run_or_exception` | `command_ref`: field path in spec.yaml (e.g. `commands.test`); `exception_file_pattern`: file-glob | Pass if the command referenced by `command_ref` ran successfully (exit 0) OR if a file matching `exception_file_pattern` contains an explanation of why it could not run |
| `git_diff_or_spec_statement` | (none beyond `check` envelope) | Pass if `git diff --name-only` shows no changes to source/test roots, OR if the baseline spec documents that the behavior was intentionally not changed, OR if the diff shows spec updates alongside source changes |

**State schema:**

Each state becomes a map with:

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | State name |
| `entry_gates` | list of strings | yes | Gate names that must pass before entering this state |
| `exit_gates` | list of strings | yes | Gate names that must pass before leaving this state |
| `artifacts_required` | list of file-globs | no | Files that should exist when in this state |

The existing `states` list on line 23-31 of the template is replaced. The state
`awaiting_approval` is removed because approval is now modelled via
`entry_gates`/`exit_gates` on `approved`.

**Concrete diff to `templates/specrepo/spec.yaml`:**

The current `required_gates` block (lines 32-41) becomes:

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
      All four baseline specs must exist and have been read by the
      spec-reviewer agent.
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
      An approval record must exist before implementation can begin.
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
      If implementation changed user-visible behavior, the baseline specs
      must match.
    check:
      type: git_diff_or_spec_statement
    spec_ref: quality.md §Documentation Rules
```

The current `states` block (lines 23-31) becomes:

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
    entry_gates:
      [approved_architecture_exists, implementation_review_exists, test_plan_exists]
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

### Change 2: Update `templates/specrepo/workflow.md`

The workflow template currently references bare gate names in prose. After this
change, the **State Machine** table gains two columns: `Entry Gates` and
`Exit Gates`, referencing the structured gate names. The **Request Intake**,
**Architecture Proposal**, **Automatic Approval**, and **Coding-Agent
Architecture Review** sections link gates to their `spec_ref` targets.

### Change 3: Update `templates/specrepo/specs/quality.md`

Add an explicit `§Documentation Rules` anchor so the
`specs_updated_if_behavior_changed` gate's `spec_ref` resolves. The current
template already has a "Documentation Rules" section but no anchor. The section
gets a Markdown heading anchor: `## Documentation Rules {#documentation-rules}`.

### Change 4: Update `templates/specrepo/specs/glossary.md`

Add entries for `gate` (a verifiable condition that must pass for a state
transition), `entry_gate` (gate checked on state entry), and `exit_gate` (gate
checked on state exit). This keeps the glossary consistent with the new
template terminology.

### Change 5: `templates/specrepo/specs/product.md` and `architecture.md`

These two spec templates are **unchanged**. The request does not alter the
product purpose, capabilities, module boundaries, or primary flows.

## Scope

### In scope

- `templates/specrepo/spec.yaml` — replace `required_gates` and `states` with
  structured schema.
- `templates/specrepo/workflow.md` — update State Machine table and section
  references to match structured gates.
- `templates/specrepo/specs/quality.md` — add `{#documentation-rules}` anchor.
- `templates/specrepo/specs/glossary.md` — add gate-related terms.
- `specrepo/requests/deterministic-spec-yaml-gates.md` — the request (already
  created).
- `specrepo/proposals/2026-07-09-deterministic-spec-yaml-gates/architecture.md` —
  this proposal.

### Out of scope

- Any changes to runtime config, CLI, or source code in `opencode-config/`.
- Changes to `opencode.jsonc` agent definitions.
- Changes to `prompts/` — the bootstrapper, request-author, spec-coder, and
  other agent prompts are not updated in this proposal (they reference the spec
  file generically and will work with the new schema as long as field names
  match).
- Adding a runtime gate-evaluation script or binary.
- Migrating existing bootstrapped `specrepo/` directories in other repos.
- CI hooks or branch-enforcement rules.
- Changes to approval-record, implementation-review, or implementation-plan
  templates beyond what is needed for gate consistency.
- The `agent_policy` booleans — they remain advisory per the request's non-goal.

## API, CLI, Config, And Integration Changes

- Public API: none
- CLI: none
- Config: `templates/specrepo/spec.yaml` — the template used by
  `@specrepo-bootstrapper` to generate repo-specific `specrepo/spec.yaml`. The
  field names `required_gates` and `states` change structure. Any agent or
  human reading a bootstrapped spec.yaml must understand the new schema.
- External integrations: none
- Data/storage behavior: none

## Files Expected To Change

| Path | Reason |
|---|---|
| `templates/specrepo/spec.yaml` | Replace `required_gates` and `states` with structured schema |
| `templates/specrepo/workflow.md` | Update State Machine table and section references |
| `templates/specrepo/specs/quality.md` | Add `{#documentation-rules}` anchor |
| `templates/specrepo/specs/glossary.md` | Add gate, entry_gate, exit_gate terms |

## Test Plan

This is a template-only change with no runtime code. Verification focuses on
the generated output:

1. **Template renders correctly** — run `@specrepo-bootstrapper` against a test
   directory (e.g. `/tmp/test-bootstrap`) and confirm the generated
   `specrepo/spec.yaml` contains structured gates and states matching the
   proposed schema.
2. **Gates are self-documenting** — each gate in the generated spec.yaml has a
   `description`, `check.type`, and `check.pattern` (or equivalent). Confirm
   with a quick script: `yq e '.required_gates[].check.type'` on the generated
   file.
3. **State entry/exit gates resolve** — each `entry_gates` and `exit_gates`
   reference a gate name that exists in `required_gates`. Confirm with a
   script: for each state, for each gate in entry/exit, the gate name must be a
   key in `required_gates`.
4. **Existing bootstraps not broken** — the change only affects the template.
   Confirm no existing bootstrapped repo's `specrepo/spec.yaml` is touched.

## Risks And Mitigations

| Risk | Mitigation |
|---|---|
| Existing agent prompts reference flat gate names and may fail to parse the new structure | Agent prompts (`prompts/*.txt`) reference `specrepo/spec.yaml` generically — they read fields by name. As long as the `required_gates` key name is preserved (it is), agents that iterate over the structure will need updated logic. Update the agent prompts in a follow-up if gate-evaluation logic is embedded there. |
| Backward incompatibility for bootstrapped repos re-running the bootstrapper | The bootstrapper should detect an existing `specrepo/spec.yaml` and ask before overwriting. This is already the expected behavior — the bootstrapper creates new structure, not overwrite. |
| Gate check types are too loosely defined for deterministic evaluation | The `check.type` values and evaluation rules in this proposal are designed for POSIX shell commands (`test -f`, `ls`, `grep`, `git diff`). If a type proves ambiguous, the proposal can be revised to add more specific types. |

## Baseline Spec Updates

- Product spec (`templates/specrepo/specs/product.md`): **unchanged**
- Architecture spec (`templates/specrepo/specs/architecture.md`): **unchanged**
- Quality spec (`templates/specrepo/specs/quality.md`): **changed** — added
  `{#documentation-rules}` anchor
- Glossary (`templates/specrepo/specs/glossary.md`): **changed** — added
  gate-related terms
- Workflow (`templates/specrepo/workflow.md`): **changed** — updated State
  Machine table and section references

## Approval Request

Approve this proposal before implementation begins. The four template files
listed in the scope above are ready for editing once approved.
