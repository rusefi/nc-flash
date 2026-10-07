/* Ghidra analysis output; verify against original SH instructions. */

/* ADCdescriptor5C578 F810 ->count ->16EFE conversion ->nonlinearretainedfilter87F8;
   raw87FA,state87FC. Supplies511CC/A518. See tcu-cycle-callback.txt. */

void OutputCycle_FilterInputB(void)

{
  ushort uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  uint uVar4;
  int iVar5;
  undefined1 local_10 [8];
  
  uVar1 = *(ushort *)PTR_DAT_00016f4c;
  uVar3 = (*(code *)PTR_OutputHandoff_ReadAdcCount_00016f5c)(PTR_DAT_00016f58);
  uVar4 = OutputCycle_ConvertInputB(uVar3,local_10);
  puVar2 = PTR_DAT_00016f50;
  iVar5 = (uint)uVar1 - (uVar4 & 0xffff);
  if ((iVar5 < -1) && (-0x10 < iVar5)) {
    iVar5 = -1;
  }
  if ((iVar5 < 0x10) && (1 < iVar5)) {
    iVar5 = 1;
  }
  if (((iVar5 < -0xf) && (-0x30 < iVar5)) || ((0xf < iVar5 && (iVar5 < 0x30)))) {
    if (iVar5 < 0) {
      iVar5 = iVar5 + 7;
    }
    iVar5 = iVar5 >> 3;
  }
  *(ushort *)PTR_DAT_00016f4c = uVar1 - (short)iVar5;
  *(short *)puVar2 = (short)uVar3;
  *PTR_DAT_00016f54 = local_10[0];
  return;
}

