/* Ghidra analysis output; verify against original SH instructions. */

/* Executes14128 for four ADC words; channel ordering0/1/3/2 into8A2C and adds counts into
   wrapping8A64 words. All10bit counts tested; conversion/completion timing unmodeled. */

void OutputHandoff_AcquireSamples(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined2 uVar4;
  int iVar3;
  byte bVar5;
  int iVar6;
  undefined2 *puVar7;
  
  puVar1 = PTR_OutputHandoff_ReadAdcCount_000189c4;
  puVar7 = (undefined2 *)(int)DAT_000189b0;
  uVar4 = (*(code *)PTR_OutputHandoff_ReadAdcCount_000189c4)(PTR_OutputHandoff_AdcPointers_000189c8)
  ;
  puVar2 = PTR_DAT_000189cc;
  *puVar7 = uVar4;
  uVar4 = (*(code *)puVar1)(puVar2);
  puVar2 = PTR_DAT_000189d0;
  puVar7[1] = uVar4;
  uVar4 = (*(code *)puVar1)(puVar2);
  puVar2 = PTR_DAT_000189d4;
  puVar7[3] = uVar4;
  uVar4 = (*(code *)puVar1)(puVar2);
  bVar5 = 0;
  iVar6 = (int)DAT_000189b2;
  puVar7[2] = uVar4;
  iVar3 = 0;
  do {
    *(short *)(iVar6 + iVar3) = *(short *)(iVar6 + iVar3) + *(short *)((int)puVar7 + iVar3);
    bVar5 = bVar5 + 1;
    iVar3 = iVar3 + 2;
  } while (bVar5 < 4);
  return;
}

