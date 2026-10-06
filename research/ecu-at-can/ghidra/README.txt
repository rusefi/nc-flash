Persistent paired-ROM Ghidra project
===================================

Open live/nc-at-can.gpr in Ghidra. Its companion nc-at-can.rep directory is
essential: the .gpr file alone does not contain the analysis.

Programs: LFFEEE-stock.bin (engine ECU), LFG1TF000.bin (TCU).
Imported from the unchanged examples/ binaries with SHA256 checks in the
annotation script. Both received auto-analysis and 1247 evidence annotations
(570 ECU, 677 TCU). Known CAN tables have explicit data types to remove
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

The current archive was extracted into a separate directory, all 11 project
file hashes checked, and both programs reopened read-only in Ghidra. All 1247
annotations and all 643 export/report files matched the live project.

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
    "$PWD/research/ecu-at-can/ghidra/decompiled"

Expect READBACK_OK for both programs (570 ECU / 677 TCU). Check logs for errors;
headless exit status alone does not prove a script completed successfully.

The older LF9VEB project in /home/snow/miata-nc-ghidra remains separate and
unchanged. This new project holds the AT ECU and TCU work in nc-flash.
