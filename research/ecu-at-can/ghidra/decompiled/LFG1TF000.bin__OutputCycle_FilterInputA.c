/* Ghidra analysis output; verify against original SH instructions. */

/* ADCdescriptor5C57C F812 ->count ->16FF6 conversion ->nonlinearretainedfilter8800;
   raw8802,state8804. Boundaryandrandom fullRAMchecks. See tcu-cycle-callback.txt. */

void OutputCycle_FilterInputA(void)

{
  ushort uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  uint uVar4;
  int iVar5;
  undefined1 local_10 [8];
  
  uVar1 = *(ushort *)PTR_DAT_00017044;
  uVar3 = (*(code *)PTR_OutputHandoff_ReadAdcCount_00017054)(PTR_DAT_00017050);
  uVar4 = OutputCycle_ConvertInputA(uVar3,local_10);
  puVar2 = PTR_DAT_00017048;
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
  *(ushort *)PTR_DAT_00017044 = uVar1 - (short)iVar5;
  *(short *)puVar2 = (short)uVar3;
  *PTR_DAT_0001704c = local_10[0];
  return;
}

