# Repository working guidance

Read `CLAUDE.md` and `.claude/notes.md` before working. Follow the repository's
architecture, verification and no-auto-commit rules.

## Durable memory

The user requires all relevant project memory to be saved in this repository.
Do not depend on chat history, automatic conversation summaries, a private
agent memory store, `/tmp`, ignored scratch directories, or a sibling checkout
as the only record needed to continue work.

- Keep `.claude/notes.md` as the short repository-wide continuation index.
- Keep substantive task findings and evidence beside the task's files. The
  ECU/AT investigation uses `research/ecu-at-can/README.txt` for findings and
  `research/ecu-at-can/CHECKPOINT.txt` for current state and next steps.
- Save meaningful discoveries and corrections incrementally, and update the
  checkpoint before ending a turn or handing off. Include the full objective,
  user constraints, decisions and reasons, exact artifact identities, evidence
  addresses/sources, commands and results, unresolved questions, failed leads
  that matter, and the next concrete action. Clearly distinguish verified
  facts, static interpretations, hypotheses, and incomplete tests.
- Preserve scripts and inputs needed to reproduce results. Record tool versions
  and setup commands when tools are temporary or machine-specific. Copy the
  relevant conclusions from outside this repository into repository files,
  with provenance; an external path alone is not durable project memory.
- Save Ghidra programs after meaningful analysis changes. Preserve `.gpr` and
  `.rep` together in a restorable archive, alongside annotation scripts and
  useful text exports. Refresh and verify that archive after changes; keeping
  only the project marker, or an outdated archive, is insufficient.
- Use Git-eligible files for durable records. Confirm ignore status when adding
  artifacts. Keep reproducible caches, transient locks and logs ignored unless
  a specific result requires retaining them. Never put credentials or unrelated
  private data into the memory bank.
- Report whether work is saved locally, staged, committed or pushed accurately.
  Saving memory does not authorize a commit or push.

Avoid duplicating large narratives across indexes: link to the authoritative
task record, and keep its status current. A continuation should be possible
from repository files even when no earlier conversation is available.

## Active research scope

Preserve all three ECU research requirements when updating memory or planning
continuation: ECU/automatic-transmission CAN integration, deep traction-control
logic/integration, and NC folding/unfolding roof CAN integration. Their current
evidence, completion criteria and open questions live in
`research/ecu-at-can/CHECKPOINT.txt` and `research/ecu-at-can/traction-roof.txt`.
Carry unresolved requirements forward explicitly; a narrower successful trace
does not complete the broader investigation.

Keep a distinct evidence status and next concrete action for traction control
and roof integration in the task checkpoint. ECU/TCU progress must not silently
replace either added goal. For each, distinguish executed firmware evidence,
factory documentation, candidate signal mappings and missing remote-controller
evidence. Preserve both folding and unfolding, including interruption and
recovery, in the roof scope.
