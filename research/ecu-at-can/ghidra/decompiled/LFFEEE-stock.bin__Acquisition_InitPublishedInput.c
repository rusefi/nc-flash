/* Ghidra analysis output; verify against original SH instructions. */

/* Copies40E8float to6CB4/6CB8/6CB0. Originalbodyexecuted afterchannel1producer; notfullboot. */

void Acquisition_InitPublishedInput(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined4 uVar3;
  
  puVar2 = PTR_Acquisition_FilteredChannel1_0001df78;
  puVar1 = PTR_Control_LocalFilterInput_0001df70;
  uVar3 = *(undefined4 *)PTR_Acquisition_ScaledChannel1_0001df74;
  *(undefined4 *)PTR_Control_LocalFilterInput_0001df70 = uVar3;
  *(undefined4 *)puVar2 = uVar3;
  *(undefined4 *)PTR_Acquisition_FilteredInputCopy_0001df7c = *(undefined4 *)puVar1;
  return;
}

