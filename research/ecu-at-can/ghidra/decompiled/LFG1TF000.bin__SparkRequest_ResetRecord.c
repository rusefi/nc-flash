/* Ghidra analysis output; verify against original SH instructions. */

/* Set indexed915C word7FFF and9166 byteFF. Index bounds not established beyond tested0..4. */

void SparkRequest_ResetRecord(char param_1)

{
  (*(code *)PTR_FUN_0001fc1c)((int)DAT_0001fc00,(int)param_1,(int)DAT_0001fbfe);
  (*(code *)PTR_FUN_0001fc20)((int)DAT_0001fc04,(int)param_1,(int)DAT_0001fc02);
  return;
}

