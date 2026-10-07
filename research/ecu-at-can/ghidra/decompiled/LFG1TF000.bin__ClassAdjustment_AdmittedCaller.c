/* Ghidra analysis output; verify against original SH instructions. */

/* Complete state admission precedes counter slice. Stock36BDA rejects; entry2 becomes1 or0, entry1
   stays1 or0; no36D1A.480whole calls/120retained pass. Earlier369C4 slices fixture state2 and prove
   conditional behavior only. */

void ClassAdjustment_AdmittedCaller(void)

{
  char *pcVar1;
  char *pcVar2;
  
  if (*(char *)(int)DAT_00036a4c == '\x01') {
    ClassAdjustment_State1();
  }
  else if (*(char *)(int)DAT_00036a4c == '\x02') {
    ClassAdjustment_State2();
  }
  pcVar2 = (char *)(int)DAT_00036a4e;
  pcVar1 = (char *)(int)DAT_00036a4c;
  *pcVar2 = *pcVar2 + '\x01';
  if (*pcVar1 == '\x02') {
    if (*pcVar2 != *PTR_DAT_00036a50) {
      return;
    }
    ClassAdjustment_UpdateStored();
  }
  *pcVar2 = '\0';
  return;
}

