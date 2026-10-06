/* Ghidra analysis output; verify against original SH instructions. */

/* u16[8814]*256/100 clamp0..32767 ->80E8;92C9bit6 substitutesROM76DDE=20480. Tailcalls50C9A.84
   valid/invalid/fault cases. */

void CAN201_UpdateWord0ApplicationValue(void)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_00020630)
                    ((uint)*(ushort *)PTR_CAN201_Word0Quarter_0002062c << 8,100);
  if ((*PTR_ApplicationFaultFlags92C9_00020634 & 0x40) != 0) {
    iVar1 = (int)*(short *)PTR_DAT_00020638;
  }
  if (DAT_00020626 < iVar1) {
    iVar1 = (int)DAT_00020626;
  }
  if (iVar1 < 0) {
    iVar1 = 0;
  }
  CAN201_Word0ApplicationValue = (undefined2)iVar1;
  (*(code *)PTR_CAN201_PublishWord0ValueAndStatus_0002063c)();
  return;
}

