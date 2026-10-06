/* Ghidra analysis output; verify against original SH instructions. */

/* Executed in local-input-faults.txt: snapshot7244/723E as Booleans, initialize8EB4=10/8EB5=8. No
   stored-DTC claim. */

void LocalInputDiag_InitializeCounters(void)

{
  undefined1 *puVar1;
  
  LocalInputDiag_SnapshotStates();
  puVar1 = DAT_0006c020;
  *PTR_LocalInputDiag_NeutralEventCounter_0006c018 = *PTR_DAT_0006c014;
  *puVar1 = *PTR_DAT_0006c01c;
  return;
}

