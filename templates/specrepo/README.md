# SpecRepo Template Pack

These templates are reusable inputs for `@specrepo-bootstrapper`.

The bootstrapper copies the structure into a target repository as `specrepo/`
and replaces placeholders with facts discovered from that repository. Do not
copy the placeholders verbatim when enough project context is available.

Generated `specrepo/` directories should not include agent profiles. Reusable
agent behavior belongs in `$HOME/.config/opencode/agents/`.

`root-README.md` is the template for the generated `specrepo/README.md`.
`root-AGENTS.md` is the template for a generated or updated repository-root
`AGENTS.md`. The other files map directly to their generated paths.

## Template Structure

```text
specrepo/
  README.md
  spec.yaml
  workflow.md
  specs/
    product.md
    architecture.md
    quality.md
    glossary.md
  requests/
    README.md
  proposals/
    README.md
  approved/
    README.md
  implementation-reviews/
    README.md
  templates/
    feature-request.md
    architecture-proposal.md
    approval-record.md
    implementation-review.md
    implementation-plan.md
```

Root-level companion file:

```text
AGENTS.md
```
