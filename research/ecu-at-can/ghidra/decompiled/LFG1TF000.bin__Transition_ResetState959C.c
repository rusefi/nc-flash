/* Ghidra analysis output; verify against original SH instructions. */

/* Set959C=1, clear95A0bit0 and tailcall2D354(index4). Explicit reset lifecycle fixture, not
   scheduler proof. */

void Transition_ResetState959C(void)

{
  byte *pbVar1;
  
  pbVar1 = (byte *)(int)DAT_0002f4c2;
  *(undefined1 *)(int)DAT_0002f4c6 = 1;
  *pbVar1 = *pbVar1 & 0xfe;
                    /* WARNING: Could not recover jumptable at 0x0002f4b8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_0002f4f0)(4);
  return;
}

