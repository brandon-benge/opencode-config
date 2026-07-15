# Feature Development With opencode Agents

This guide describes a reusable feature-development workflow for any
SpecRepo-managed repository using the opencode agents in this bundle.

## Directory Boundary

Keep responsibilities separate:

| Directory | Responsibility |
| --- | --- |
| `opencode-config/` | Reusable opencode agent config, permissions, prompts, skills, and workflow guidance. |
| `specrepo/` | Repo-specific baseline specs, templates, requests, proposals, approvals, implementation reviews, and verification evidence. |

Agents should treat repository-root `AGENTS.md` and `specrepo/specs/` as the
source for local project facts such as source roots, test roots, runtime config,
and default verification commands. Reusable procedures live in opencode skills.

## Purpose And Prerequisites

Use this workflow when a change should move through request, architecture,
automatic approval, implementation review, implementation, verification, and
merge without losing the decision trail.

The target repository should have:

- opencode configured with the agents from this bundle.
- A repository-root `AGENTS.md` with current project shape.
- Baseline specs under `specrepo/specs/`.
- Templates under `specrepo/templates/`.
- A clean enough working tree that feature changes can be reviewed.
- A feature request file under `specrepo/requests/`.

If the request does not exist yet, ask `@request-author` to create one before
architecture work begins. Keep the request small enough that behavior,
non-goals, constraints, and acceptance criteria are clear.

If the target repository does not have `specrepo/`, ask
`@specrepo-bootstrapper` to create it from the reusable template pack before
starting feature work.

## Role Split

Primary agents automatically chain to subagents. You only need to call the
primary agents; the handoffs happen in the background.

| Role | Mode | Responsibility | Handles |
| --- | --- | --- | --- |
| `@specrepo-bootstrapper` | primary | Creates a complete repo-specific SpecRepo structure when a repository does not have one yet. | One-time setup |
| `@request-author` | primary | Creates or refines one request, then **auto-chains** to `@spec-reviewer` then `@architecture-approver`. | Request → Proposal → Auto-approval → Summary |
| `@spec-reviewer` | subagent | Turns one request into an architecture proposal and any justified baseline spec updates. | Called by `@request-author` |
| `@architecture-approver` | subagent | Reviews proposal readiness. Creates the approval record automatically when the proposal meets the criteria. | Called by `@request-author` |
| `@spec-coder` | primary | Implements the approved scope, **auto-chains** to `@implementation-reviewer` if needed, then to `@test-reviewer`. | Impl. review → Code → Test review |
| `@implementation-reviewer` | subagent | Creates the pre-code implementation review and decides `Proceed` or `Stop for revised architecture`. | Called by `@spec-coder` |
| `@test-reviewer` | subagent | Reviews tests, verification evidence, and scope compliance without editing files. | Called by `@spec-coder` |

Only call the primary agents: `@specrepo-bootstrapper`, `@request-author`, and
`@spec-coder`. The subagents (`@spec-reviewer`, `@architecture-approver`,
`@implementation-reviewer`, `@test-reviewer`) are invoked automatically by the
chain and should never be called directly.

📊 [Agent Responsibility Map](agent-responsibility-map.mmd) — visual reference
for the agent roles, relationships, and auto-chain groups.

## End-To-End Lifecycle

Primary agents chain to subagents automatically. You only need to call the
primary agents at the right time.

1. **Bootstrap** — Create `specrepo/` with `@specrepo-bootstrapper` if it does
   not exist.
2. **Request + Proposal + Approval** — Ask `@request-author` to create or
   refine the feature request. It automatically delegates to `@spec-reviewer`
   (architecture proposal) then `@architecture-approver` (review and automatic
   approval record creation if criteria are met).
3. **Review and decide** — Read the proposal and architecture-approver
   recommendation. If the recommendation is `approve` and you are satisfied,
   proceed. If `revise` or `reject`, or if you simply do not like the result,
   stop here — do not call `@spec-coder`.
4. **Implement** — Ask `@spec-coder` to implement the approved scope. It
   automatically delegates to `@implementation-reviewer` (review gate) if
   needed, then `@test-reviewer` (verification review) after coding.
5. **Final review** — Review the implementation summary, git diff, and
   `@test-reviewer` recommendation (`pass` / `needs more tests` / `blocked`).
6. **Merge** — Merge when verification evidence exists and you are satisfied.

📊 [Feature Development Lifecycle](feature-development-lifecycle.mmd) —
end-to-end flowchart of the entire lifecycle.

📊 [States And Gates](states-and-gates.mmd) — simplified state machine
(see [Feature Development Lifecycle](feature-development-lifecycle.mmd) for
full branching flow with decision gates).

## Prompt Templates

Replace bracketed placeholders with paths and names from the target repository's
SpecRepo directory and `AGENTS.md`. Subagents are called automatically — you
only need to call the primary agents.

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

- Baseline specs under `specrepo/specs/`
- Inboxes under `specrepo/requests/`, `specrepo/proposals/`,
  `specrepo/approved/`, and `specrepo/implementation-reviews/`
- Artifact templates under `specrepo/templates/`
- Repository-root `AGENTS.md` updated with project shape and SpecRepo guidance

Human gate:

- Confirm the inferred project facts before using the generated SpecRepo for
  feature work.

### 1. Request → Proposal → Approval (One Prompt)

Call `@request-author` once. It creates the request, then automatically chains
to `@spec-reviewer` (architecture proposal) and `@architecture-approver`
(review and automatic approval record creation).

```text
@request-author Create or refine this SpecRepo request at
specrepo/requests/[request-name].md.

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
```

**Automatic chain (no human action needed):**

| Step | Agent | Produces |
| --- | --- | --- |
| 1 | `@request-author` | `specrepo/requests/[request-name].md` |
| 2 | → `@spec-reviewer` (auto) | `specrepo/proposals/YYYY-MM-DD-[name]/architecture.md` |
| 3 | → `@architecture-approver` (auto) | Readiness recommendation and auto-created approval record at `specrepo/approved/YYYY-MM-DD-[name]/approval.md` |

Expected output:

- Request file with acceptance criteria, constraints, and non-goals.
- Architecture proposal with scope, test plan, and approval conditions.
- Approval record (if the proposal was approved).

Human gate:

- Read the proposal and architecture-approver recommendation.
- If satisfied, call `@spec-coder` to implement.
- If `revise` or `reject`, ask `@request-author` to re-run with a clearer
  request.
- If you simply do not like the proposed approach, do not call `@spec-coder`.

### 2. Implementation → Test Review (One Prompt)

Call `@spec-coder` once. It checks that the approval record and implementation
review exist, implements, then chains to `@test-reviewer`.

```text
@spec-coder Implement the approved change described by
specrepo/approved/YYYY-MM-DD-[short-name]/approval.md.
```

**Automatic chain (no human action needed):**

| Step | Agent | Produces |
| --- | --- | --- |
| 1 | → `@implementation-reviewer` (auto, if missing) | `specrepo/implementation-reviews/YYYY-MM-DD-[name].md` / `Proceed` or `Stop` |
| 2 | `@spec-coder` implements | Source, config, test, doc changes |
| 3 | `@spec-coder` runs verification | Verification results |
| 4 | → `@test-reviewer` (auto) | Recommendation: `pass` / `needs more tests` / `blocked` |
| 5 | `@spec-coder` acts on result | Autocommit (git commit, no checks) if `pass`; or retry loop (fix → verify → test review) if `needs more tests` |

Expected output:

- Implementation review gate (if one did not already exist).
- Source, config, docs, or spec changes within the approved scope.
- Tests or checks required by the approved test plan.
- Verification commands and results, or a recorded reason they could not run.
- `@test-reviewer` recommendation.
- Autocommit (git commit, no checks — only runs when verification passed and
  test review passed).

Human gate:

- Review the implementation summary and git diff.
- Do not merge until verification evidence exists and test review passes or
  any residual risk is explicitly accepted.

### 3. Final Diff And Merge

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
- The architecture-approver approves automatically; you stay in control by
  choosing whether to call `@spec-coder`.
- Do not let implementation start before both approval and implementation
  review exist (handled automatically by `@spec-coder`).
- Keep proposal names, approval names, and implementation review names aligned.
- Prefer small, focused tests or checks that map directly to acceptance
  criteria.
- Record exact verification commands and results.
- Stop for revised architecture when implementation discovers a material design
  change.
- Keep unrelated cleanup out of the feature branch.
- After `@spec-coder` finishes, read its summary — it includes the
  `@test-reviewer` recommendation. If the result was `needs more tests`,
  re-run `@spec-coder` to fix; the chain re-invokes `@test-reviewer`
  automatically in a retry loop (fix → verify → review).
- The autocommit tool runs the `autocommit` CLI with the YAML file named by
  `AUTOCOMMIT_PARAMS`. It runs only after tests pass and `@test-reviewer`
  returns `pass`; it performs no verification of its own.
- You never need to call `@spec-reviewer`, `@architecture-approver`,
  `@implementation-reviewer`, or `@test-reviewer` directly. Call only the
  primary agents (`@request-author`, `@spec-coder`) and let the chain handle
  the rest.

## Troubleshooting

### The Request Is Ambiguous

Stop before architecture. Refine `specrepo/requests/[request-name].md` until the
desired behavior, acceptance criteria, constraints, and non-goals are concrete.

### The Proposal Does Not Match The Request

The proposal was created by `@spec-reviewer` as part of the `@request-author`
chain. Ask `@request-author` to re-run with a clearer request, or directly
prompt `@spec-reviewer` to revise. Do not proceed to implementation when the
proposal has missing behavior, vague tests, or hidden scope expansion.

### Architecture-Approver Says `revise` Or `reject`

No approval record was created. Ask `@request-author` to re-run the chain with
a refined request, or directly prompt `@spec-reviewer` to revise the proposal,
then `@architecture-approver` to re-review.

### Implementation Review Says `Stop for revised architecture`

`@spec-coder` will report this automatically and stop. Ask
`@request-author` to start a new chain with the blocker information, or
directly ask `@spec-reviewer` for revised architecture. A revised proposal
needs a new approval from `@architecture-approver` before resuming.

### `@spec-coder` Finds A Material Architecture Change

`@spec-coder` will report this automatically and stop. Ask
`@request-author` to start a new chain, or directly ask `@spec-reviewer`
for revised architecture.

### Verification Fails

Ask `@spec-coder` to fix failures within the approved scope and rerun. The
`@test-reviewer` chain will re-run automatically after verification.

### Test Review Says `needs more tests`

Re-run `@spec-coder`. It fixes the missing tests, re-runs verification, and
re-invokes `@test-reviewer` automatically. You do not need to call
`@test-reviewer` separately.

### The Diff Contains Unrelated Changes

Separate unrelated work before merge. The approved feature branch should contain
only the request, proposal, approval, implementation review, implementation,
tests, docs, and spec updates required for the approved feature.

### Verification Cannot Run

Record the exact command, the exact failure, and why it could not be completed.
Do not treat missing verification as a pass. A human must decide whether the
risk is acceptable before merge.
