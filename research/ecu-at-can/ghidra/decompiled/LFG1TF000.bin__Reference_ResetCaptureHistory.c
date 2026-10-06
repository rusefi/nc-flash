/* Ghidra analysis output; verify against original SH instructions. */

/* SR critical section fills18 words91CC with20DE8()=57344, resets91B4=0. See
   tcu-reference-source.txt. */

void Reference_ResetCaptureHistory(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  int iVar4;
  
  uVar1 = Reference_ReadResetPeriod();
  uVar2 = (*(code *)PTR_FUN_00020e30)();
  puVar3 = (undefined4 *)PTR_Reference_CaptureHistory_00020e34;
  for (iVar4 = 0; iVar4 < (int)(uint)(byte)*PTR_DAT_00020e38; iVar4 = iVar4 + 1) {
    *puVar3 = uVar1;
    puVar3 = puVar3 + 1;
  }
  *(undefined1 *)(int)DAT_00020e18 = 0;
  (*(code *)PTR_FUN_00020e3c)(uVar2);
  return;
}

