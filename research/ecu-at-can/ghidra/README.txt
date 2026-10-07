Persistent paired-ROM Ghidra project
===================================

Open live/nc-at-can.gpr in Ghidra. Its companion nc-at-can.rep directory is
essential: the .gpr file alone does not contain the analysis.

Programs: LFFEEE-stock.bin (engine ECU), LFG1TF000.bin (TCU).
Imported from the unchanged examples/ binaries with SHA256 checks in the
annotation script. Both received auto-analysis and 2012 evidence annotations
(865 ECU, 1147 TCU). Known CAN tables have explicit data types to remove
speculative functions created by auto-analysis inside table bytes.

Ghidra version: 12.1.3 PUBLIC, Java 21.
Language: SuperH:BE:32:SH-2A, default compiler specification.
This installed language provides the floating-point instruction support
needed for analysis; it is a superset choice, not identification of either
chip as an SH-2A. The firmware uses SH-2E-family code. Verify decompilation
against original instructions, especially delay slots and floating point.
Analysis_RAM covers observed references; it is not a full hardware map.
TCU Analysis_Low_RAM6000..7FFF covers newly traced diagnostic-list accesses
near6188; this is neither physical-chip RAM identification nor an EEPROM claim.
TCU GBR context is FFFF8000 over application ROM 10000..7FFFF.

What is saved for Git:
  nc-at-can.tar.gz       full closed project (.gpr plus .rep)
  snapshot.json          archive SHA256 and per-file SHA256 inventory
  restore-verification.json  successful independent restoration check
  annotations.tsv       reproducible names, comments and addresses
  scripts/              import annotation and read-back/export scripts
  decompiled/           annotated function exports and read-back reports
  snapshot.py           archive creation with byte-for-byte read-back
  verify_restore.py     complete export/readback and archive/project hash checks

The current archive was extracted into restore-check/basic-startup-20261007.
All 11 project-file hashes matched before and after both programs reopened
read-only. All 2012 annotations and 1046 complete export/report files matched.
This refresh adds six original UBC/BSC/DMA-operation startup functions, with
whole-RAM/register/MMIO component checks. Complete15574 now stops at ITVRR1
F424 before recovery-enable flags; no full startup/physical recovery claim.
See ../tcu-basic-hardware-startup.txt for sources, assumptions and next action.
The programs, archive and exports are saved locally. No staging/commit/push.
../CHECKPOINT.txt owns all three broader scopes and next actions. Current
archive identity and independent restoration results are in snapshot.json and
restore-verification.json. Dated older reports retain historical identities.

The live/ database, restore-check/ scratch and logs remain ignored. After
editing in Ghidra, save both programs, CLOSE the project, then refresh:

  python research/ecu-at-can/ghidra/snapshot.py

Refresh annotations.tsv when changing evidence labels/comments. GUI-only
edits persist in the archive but are not automatically copied into the TSV.
Re-run VerifyCanEvidence.java to refresh exports when analysis changes.
Check git status and review the archive/manifest together before committing.
Saving locally and creating an archive do not commit or push anything.

Restore into a new empty directory (do not overwrite an open project):

  mkdir /path/to/restored-project
  tar -xzf research/ecu-at-can/ghidra/nc-at-can.tar.gz -C /path/to/restored-project

Open /path/to/restored-project/nc-at-can.gpr. Both database and marker file
are included. snapshot.json permits independent archive/file hash checks.

Rebuild instead of restoring (run from repository root; requires Ghidra):

  mkdir -p research/ecu-at-can/ghidra/live
  analyzeHeadless research/ecu-at-can/ghidra/live nc-at-can \
    -import examples/LFFEEE-stock.bin examples/LFG1TF000.bin \
    -loader BinaryLoader -processor SuperH:BE:32:SH-2A -cspec default \
    -scriptPath research/ecu-at-can/ghidra/scripts \
    -preScript ApplyCanEvidence.java "$PWD/research/ecu-at-can/ghidra/annotations.tsv" \
    -analysisTimeoutPerFile 180 -max-cpu 2

Then reapply the evidence after auto-analysis, save, and independently reopen:

  analyzeHeadless research/ecu-at-can/ghidra/live nc-at-can \
    -process '*' -noanalysis -scriptPath research/ecu-at-can/ghidra/scripts \
    -postScript ApplyCanEvidence.java "$PWD/research/ecu-at-can/ghidra/annotations.tsv"
  analyzeHeadless research/ecu-at-can/ghidra/live nc-at-can \
    -process '*' -noanalysis -readOnly -scriptPath research/ecu-at-can/ghidra/scripts \
    -postScript VerifyCanEvidence.java "$PWD/research/ecu-at-can/ghidra/annotations.tsv" \
    "$PWD/research/ecu-at-can/ghidra/decompiled" 300

Expect READBACK_OK for both programs (865 ECU / 1147 TCU). Check logs for errors;
headless exit status alone does not prove a script completed successfully.

The older LF9VEB project in /home/snow/miata-nc-ghidra remains separate and
unchanged. This new project holds the AT ECU and TCU work in nc-flash.

After read-only VerifyCanEvidence.java runs on both the live project and an
independently extracted project (using restored/exports as its output folder),
close both and compare all expected artifacts:

  python research/ecu-at-can/ghidra/verify_restore.py /path/to/restored-project --write-report

The script validates archive/live/restored file hashes, expected export names,
complete readbacks, annotation rows and identical contents. It writes the
restore report only after every check passes. VerifyCanEvidence.java allows
60 seconds per function and fails if any decompilation is incomplete; it also
removes stale exports on a failed decompilation. The previous15-second timeout
left an old startup export in place; tcu-cmt0-delivery.txt records that failure
and the required rerun. Headless process exit status alone is insufficient.

For the large ECU1619A startup function, the optional third argument to
VerifyCanEvidence.java can increase the per-function allowance to300 seconds.
The CMT0 refresh required retrying the ECU program after15/60-second timeouts;
the TCU verification remained complete. Every export is still required.
