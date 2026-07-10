# Glossary

| Term | Meaning |
| --- | --- |
| Gate | A verifiable condition that must pass for a workflow state transition. Defined in `specrepo/spec.yaml` under `required_gates` with a `check.type`, `pattern`, and optional `spec_ref`. |
| Entry gate | A gate that must pass before the workflow can enter a given state. Listed in that state's `entry_gates` in `specrepo/spec.yaml`. |
| Exit gate | A gate that must pass before the workflow can leave a given state. Listed in that state's `exit_gates` in `specrepo/spec.yaml`. |
| Request | A feature or change request placed in `specrepo/requests/`. |
| Request author | The authoring role, normally `@request-author`, that creates or refines a request before architecture work begins. |
| Proposal | A draft architecture response to a request, placed in `specrepo/proposals/`. |
| Approval record | Human approval for a proposal, placed in `specrepo/approved/`. |
| Implementation review | Coding-agent review of the approved architecture before code edits. |
| Baseline spec | Current approved product, architecture, quality, and glossary documentation in `specrepo/specs/`. |
| <Project term> | <Meaning> |
