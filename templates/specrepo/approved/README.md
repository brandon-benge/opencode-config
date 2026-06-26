# Approved Architecture

Human-approved architecture records live here.

Use `@architecture-approver` to create approval records after explicit human
approval. The human approval prompt should name the proposal and ask
`@architecture-approver` to create the record from
`specrepo/templates/approval-record.md`.

Use one subdirectory per approved request:

```text
specrepo/approved/YYYY-MM-DD-short-name/approval.md
```

Implementation may begin only after the approval record exists and points to the
approved proposal.
