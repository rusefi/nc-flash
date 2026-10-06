/* Ghidra analysis output; verify against original SH instructions. */

/* SR critical section increments91AC saturatingFFFF;16 value/SR cases. Accepted20678 capture clears
   it.1E506 tailcalls here; physical period open. See tcu-reference-policy.txt. */

void Reference_IncrementElapsedCaptureCounter(void)

{
  undefined4 uVar1;
  ushort *puVar2;
  
  uVar1 = (*(code *)PTR_FUN_000209a8)();
  puVar2 = (ushort *)(int)DAT_0002097a;
  if ((int)(uint)*puVar2 < (int)PTR_DAT_000209ac) {
    *puVar2 = *puVar2 + 1;
  }
  (*(code *)PTR_FUN_000209b0)(uVar1);
  return;
}

