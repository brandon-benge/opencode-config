# Feature Development With opencode Agents

This guide describes a reusable feature-development workflow for any
SpecRepo-managed repository using the opencode agents in this bundle.

## Directory Boundary

Keep responsibilities separate:

| Directory | Responsibility |
| --- | --- |
| `opencode-config/` | Reusable opencode agent profiles, permissions, prompts, and workflow guidance. |
| `specrepo/` | Repo-specific project facts, workflow gates, baseline specs, templates, requests, proposals, approvals, implementation reviews, and verification commands. |

Agents should treat `specrepo/spec.yaml` as the manifest for local facts such
as `source_roots`, `test_roots`, workflow directories, and `commands.test`.

## Purpose And Prerequisites

Use this workflow when a change should move through request, architecture,
human approval, implementation review, implementation, verification, and merge
without losing the decision trail.

The target repository should have:

- opencode configured with the agents from this bundle.
- `specrepo/spec.yaml`.
- `specrepo/workflow.md`.
- Baseline specs under `specrepo/specs/`.
- Templates under `specrepo/templates/`.
- A clean enough working tree that feature changes can be reviewed.
- A feature request file under the request directory named in
  `specrepo/spec.yaml`.

If the request does not exist yet, create one before asking any agent to begin.
Keep the request small enough that behavior, non-goals, constraints, and
acceptance criteria are clear.

If the target repository does not have `specrepo/`, ask
`@specrepo-bootstrapper` to create it from the reusable template pack before
starting feature work.

## Role Split

| Role | Responsibility |
| --- | --- |
| `@specrepo-bootstrapper` | Creates a complete repo-specific SpecRepo structure when a repository does not have one yet. |
| Request author | Describes the desired repository-specific behavior and acceptance criteria. |
| `@spec-reviewer` | Turns one request into an architecture proposal and any justified baseline spec updates. |
| `@architecture-approver` | Reviews proposal readiness and writes an approval record only after explicit human approval. |
| Human approver | Owns the final architecture approval decision. |
| `@implementation-reviewer` | Creates the pre-code implementation review and decides `Proceed` or `Stop for revised architecture`. |
| `@spec-coder` | Implements only the approved scope after approval and implementation review exist. |
| `@test-reviewer` | Reviews tests, verification evidence, and scope compliance without editing files. |
| Human merger | Reviews the final diff and decides whether to merge. |

## End-To-End Lifecycle

1. Create `specrepo/` with `@specrepo-bootstrapper` if it does not exist.
2. Create the feature request.
3. Ask `@spec-reviewer` to create the architecture proposal.
4. Review the proposal yourself.
5. Ask `@architecture-approver` for an approval-readiness review.
6. Give human approval only when the proposal is ready.
7. Create the approval record, or explicitly ask `@architecture-approver` to
   create it after you approve.
8. Ask `@implementation-reviewer` to create the implementation review gate.
9. Ask `@spec-coder` to implement the approved scope.
10. Ask `@test-reviewer` to review coverage and verification evidence.
11. Fix any blocking findings within the approved scope.
12. Run or confirm final verification.
13. Review the final diff and merge.

## Prompt Templates

Replace bracketed placeholders with paths and names from the target
repository's SpecRepo manifest.

### 0. Bootstrap SpecRepo With `@specrepo-bootstrapper`

Use this only when `specrepo/` does not exist yet.

```text
@specrepo-bootstrapper Create a complete SpecRepo structure for this
repository.

Inspect the repository to infer product name, language, source roots, test
roots, package metadata, default config, and default verification command. Use
the reusable templates under opencode-config/templates/specrepo/. Tailor the
baseline specs to this repository. Do not create requests, proposals, approval
records, or implementation reviews for unrelated work.
```

Expected output:

- `specrepo/spec.yaml`
- `specrepo/workflow.md`
- Baseline specs under `specrepo/specs/`
- Inboxes under `specrepo/requests/`, `specrepo/proposals/`,
  `specrepo/approved/`, and `specrepo/implementation-reviews/`
- Artifact templates under `specrepo/templates/`

Human gate:

- Confirm the inferred project facts before using the generated SpecRepo for
  feature work.

### 1. Create Or Refine The Request

```text
Create or refine this SpecRepo request at specrepo/requests/[request-name].md.

Feature:
[describe the user-visible behavior]

Acceptance criteria:
- [criterion 1]
- [criterion 2]
- [criterion 3]

Constraints:
- [important compatibility, safety, performance, or workflow constraint]

Non-goals:
- [explicitly out of scope]

Do not create an architecture proposal yet.
```

Expected output:

- `specrepo/requests/[request-name].md`
- Clear acceptance criteria.
- Explicit constraints and non-goals.

Human gate:

- Confirm the request describes the intended change before architecture work
  starts.

### 2. Architecture Proposal With `@spec-reviewer`

```text
@spec-reviewer Read specrepo/requests/[request-name].md and create the
architecture proposal for it.

Follow the SpecRepo workflow and templates. Read specrepo/spec.yaml first to
discover source roots, test roots, workflow directories, and default commands.
Inspect source and tests only as needed to ground the proposal. Do not edit
implementation code. End by listing any baseline spec changes and asking for
human approval.
```

Expected output:

- `specrepo/proposals/YYYY-MM-DD-[short-name]/architecture.md`
- Optional updates to baseline specs under `specrepo/specs/`.
- A clear list of expected source, test, config, docs, and behavior changes.
- A test or verification plan and explicit approval conditions.

Human gate:

- Read the proposal and decide whether it matches the request.
- Do not approve if scope, risks, API, CLI, config, provider, prompt, external
  side effects, docs, or verification expectations are unclear.

### 3. Approval-Readiness Review With `@architecture-approver`

```text
@architecture-approver Review
specrepo/proposals/YYYY-MM-DD-[short-name]/architecture.md for approval
readiness.

Compare it with the original request and current baseline specs. Do not create
an approval record yet. Return a decision recommendation of approve, revise, or
reject with blocking issues, non-blocking suggestions, and approval conditions.
```

Expected output:

- Chat review with decision recommendation: `approve`, `revise`, or `reject`.
- Blocking issues, if any.
- Non-blocking suggestions.
- Approval conditions.

Human gate:

- If the recommendation is `revise` or `reject`, send the proposal back through
  `@spec-reviewer`.
- If the recommendation is `approve`, make the final human approval decision.

### 4. Human Approval Record

Only create an approval record after a human approves the proposal.

```text
@architecture-approver I approve
specrepo/proposals/YYYY-MM-DD-[short-name]/architecture.md.

Create the approval record using the repository's approval-record template.
Name me as the human approver for this opencode session.
```

Expected output:

- `specrepo/approved/YYYY-MM-DD-[short-name]/approval.md`
- The approval record references the approved proposal.
- The approval record names the human approver or states that the user approved
  it in the current opencode session.

Human gate:

- Verify the approval record points to the intended proposal.
- Implementation must not start until this record exists.

### 5. Implementation Review Gate With `@implementation-reviewer`

```text
@implementation-reviewer Read
specrepo/approved/YYYY-MM-DD-[short-name]/approval.md and create the required
implementation review.

Confirm the approved architecture is internally consistent, maps to concrete
source, test, config, documentation, and verification files where applicable,
and has an executable verification plan. Do not edit implementation code.
```

Expected output:

- `specrepo/implementation-reviews/YYYY-MM-DD-[short-name].md`
- Decision: `Proceed` or `Stop for revised architecture`.
- Concrete implementation map.
- Verification plan.

Human gate:

- Continue only if the decision is `Proceed`.
- If the decision is `Stop for revised architecture`, return to architecture
  proposal revision and repeat approval.

### 6. Implementation With `@spec-coder`

```text
@spec-coder Implement the approved change described by
specrepo/approved/YYYY-MM-DD-[short-name]/approval.md and
specrepo/implementation-reviews/YYYY-MM-DD-[short-name].md.

Stay within the approved scope. Add or update the tests or checks required by
the approved verification plan. If implementation reveals a material
architecture change, stop and ask for a revised proposal. Run the approved
verification commands and summarize the results.
```

Expected output:

- Source, config, docs, or spec changes within the approved scope.
- Test or verification changes required by the approved test plan.
- Verification commands and results, or a recorded reason they could not run.

Human gate:

- Review the implementation summary and git diff.
- Do not merge until verification evidence exists and test review passes or
  any residual risk is explicitly accepted.

### 7. Test And Verification Review With `@test-reviewer`

```text
@test-reviewer Review the current git diff against
specrepo/approved/YYYY-MM-DD-[short-name]/approval.md,
specrepo/proposals/YYYY-MM-DD-[short-name]/architecture.md, and
specrepo/implementation-reviews/YYYY-MM-DD-[short-name].md.

Check whether tests or verification evidence cover every acceptance criterion,
whether verification commands actually ran, and whether the implementation
stayed within approved scope. Do not edit files. Return findings first and end
with a verification recommendation of pass, needs more tests, or blocked.
```

Expected output:

- Findings first, ordered by severity.
- File and line references where possible.
- Missing tests or residual risks.
- Verification recommendation: `pass`, `needs more tests`, or `blocked`.

Human gate:

- `pass`: proceed to final review and merge.
- `needs more tests`: ask `@spec-coder` to add the missing tests, then rerun
  `@test-reviewer`.
- `blocked`: resolve the blocker before continuing. If the blocker changes the
  approved architecture, go back to the architecture proposal stage.

### 8. Final Diff And Merge

Use the normal primary opencode session or your own shell for final commands.

```text
Review the final git diff for the approved feature. Confirm it matches
specrepo/approved/YYYY-MM-DD-[short-name]/approval.md, includes the expected
tests or verification evidence, and has no unrelated changes. Then summarize
the merge readiness.
```

Expected output:

- Final diff review.
- Verification results.
- Explicit merge-readiness summary.

Human gate:

- A human decides whether to merge.
- Do not merge unrelated changes with the approved feature.

## Best Practices

- Keep each request focused on one user-visible change.
- Put ambiguity in the request before architecture starts.
- Treat approval as a human decision, not an agent decision.
- Do not let implementation start before both approval and implementation
  review exist.
- Keep proposal names, approval names, and implementation review names aligned.
- Prefer small, focused tests or checks that map directly to acceptance
  criteria.
- Record exact verification commands and results.
- Stop for revised architecture when implementation discovers a material design
  change.
- Keep unrelated cleanup out of the feature branch.
- Rerun `@test-reviewer` after any meaningful implementation or test change.

## Troubleshooting

### The Request Is Ambiguous

Stop before architecture. Refine `specrepo/requests/[request-name].md` until the
desired behavior, acceptance criteria, constraints, and non-goals are concrete.

### The Proposal Does Not Match The Request

Ask `@spec-reviewer` to revise the proposal. Do not approve a proposal with
missing behavior, vague tests, or hidden scope expansion.

### Approval Review Says `revise` Or `reject`

Do not create an approval record. Fix the proposal first, then rerun
`@architecture-approver`.

### Implementation Review Says `Stop for revised architecture`

Return to `@spec-reviewer` with the blocker. The feature needs revised
architecture and another human approval before implementation.

### `@spec-coder` Finds A Material Architecture Change

Stop coding. Ask for a revised proposal instead of expanding scope in the
implementation.

### Verification Fails

Ask `@spec-coder` to fix failures within the approved scope and rerun the
approved verification plan.

### Test Review Says `needs more tests`

Ask `@spec-coder` to add the missing tests, then run `@test-reviewer` again.

### The Diff Contains Unrelated Changes

Separate unrelated work before merge. The approved feature branch should contain
only the request, proposal, approval, implementation review, implementation,
tests, docs, and spec updates required for the approved feature.

### Verification Cannot Run

Record the exact command, the exact failure, and why it could not be completed.
Do not treat missing verification as a pass. A human must decide whether the
risk is acceptable before merge.
