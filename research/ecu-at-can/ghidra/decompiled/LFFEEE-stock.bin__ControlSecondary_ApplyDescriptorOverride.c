/* Ghidra analysis output; verify against original SH instructions. */

/* 966Cbit6clear clears960E. Mode0 encodes963C andreturns originalinput;5/7
   decode963C*.0030517578125;othernonzero passthrough.1408cases. Operationaldiagnosticmeaning/access
   unproved. */

uint ControlSecondary_ApplyDescriptorOverride(undefined4 param_1)

{
  undefined *puVar1;
  uint uVar2;
  int iVar3;
  
  puVar1 = PTR_DAT_0008b9b8;
  iVar3 = (int)DAT_0008b9b6;
  if ((*PTR_DAT_0008b9bc & PTR_DAT_0008b9b8[iVar3 + 8]) == 0) {
    **(undefined1 **)(PTR_DAT_0008b9b8 + iVar3 + 0xc) = 0;
  }
  uVar2 = (uint)**(byte **)(puVar1 + iVar3 + 0xc);
  if (uVar2 == 0) {
    uVar2 = (*(code *)PTR_FUN_0008b9cc)(param_1,DAT_0008b9c8,0);
    puVar1 = PTR_ControlSecondary_EncodedValue_0008b9d0;
    *PTR_ControlSecondary_EncodedValue_0008b9d0 = (char)(uVar2 >> 8);
    puVar1[1] = (char)uVar2;
  }
  else if ((uVar2 == 5) || (uVar2 == 7)) {
    uVar2 = (*(code *)PTR_FUN_0008bacc)
                      (DAT_0008b9c8,0,*(undefined2 *)PTR_ControlSecondary_EncodedValue_0008bac8);
  }
  return uVar2;
}

