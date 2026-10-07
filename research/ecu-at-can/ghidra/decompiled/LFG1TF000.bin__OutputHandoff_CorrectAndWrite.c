/* Ghidra analysis output; verify against original SH instructions. */

/* Executed error/proportional/integral correction, exact fallback flags and retained reset on first
   recovery call; final signedword clamp then14280. Explicit ADC inputs/write sink only, no physical
   actuation model. */

void OutputHandoff_CorrectAndWrite(int param_1)

{
  int iVar1;
  short sVar4;
  undefined4 uVar2;
  int iVar3;
  char cVar5;
  int iVar6;
  short *psVar7;
  char *pcVar8;
  bool bVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  
  iVar12 = param_1 * 2;
  iVar1 = (*(code *)PTR_FUN_00018b8c)();
  psVar7 = (short *)(DAT_00018b6c + iVar12);
  (*(code *)PTR_FUN_00018b90)();
  sVar4 = (*(code *)PTR_FUN_00018b90)();
  iVar11 = (int)DAT_00018b78;
  *psVar7 = sVar4 + *(short *)(iVar12 + DAT_00018b76);
  *(short *)(iVar11 + iVar12) =
       *(short *)(PTR_OutputDriver_PreviousWords_00018b94 + iVar12) - *psVar7;
  uVar2 = (*(code *)PTR_FUN_00018b8c)();
  iVar3 = (*(code *)PTR_FUN_00018b98)(uVar2);
  iVar6 = (int)DAT_00018b7c;
  iVar10 = param_1 * 4;
  uVar2 = OutputHandoff_AccumulateError
                    ((int)*(short *)(iVar11 + iVar12),(int)*(short *)(iVar12 + DAT_00018b7e),
                     *(undefined4 *)(iVar6 + iVar10),iVar1);
  *(undefined4 *)(iVar6 + iVar10) = uVar2;
  iVar6 = (*(code *)PTR_FUN_00018b8c)();
  cVar5 = (*(code *)PTR_OutputHandoff_ReadInhibit_00018b9c)();
  if (*(char *)(param_1 + DAT_00018b80) == '\x01') {
    bVar9 = false;
    pcVar8 = (char *)(DAT_00018b82 + param_1);
    if ((((*(ushort *)(iVar12 + DAT_00018b84) < 0x44) ||
         ((int)DAT_00018b68 < (int)(uint)*(ushort *)(iVar12 + DAT_00018b84))) ||
        (((int)(uint)*(ushort *)PTR_DAT_00018ba4 < (int)DAT_00018b86 &&
         ((0 < *(short *)(iVar12 + DAT_00018b78) &&
          ((int)(uint)*(ushort *)PTR_DAT_00018ba4 <=
           (int)(short)(((short)iVar1 - *(short *)PTR_DAT_00018ba0) + (short)iVar6))))))) ||
       (cVar5 == '\x01')) {
      bVar9 = true;
      *pcVar8 = '\x01';
    }
    else {
      cVar5 = *pcVar8;
      *pcVar8 = '\0';
      if (cVar5 != '\0') {
        bVar9 = true;
      }
    }
    if (bVar9) {
      iVar3 = 0;
      iVar6 = (*(code *)PTR_FUN_00018c28)();
      *(int *)(iVar10 + DAT_00018c22) = (int)(short)iVar6 * (int)DAT_00018c24;
    }
  }
  else if (cVar5 == '\x01') {
    iVar3 = 0;
    iVar6 = 0;
    *(undefined4 *)(iVar10 + DAT_00018c22) = 0;
  }
  iVar10 = (int)DAT_00018c26;
  sVar4 = (*(code *)PTR_FUN_00018c30)(iVar1 + iVar3 + iVar6,0,(int)*(short *)PTR_DAT_00018c2c);
  *(short *)(iVar10 + iVar12) = sVar4;
                    /* WARNING: Could not recover jumptable at 0x00018c1e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_OutputHandoff_WritePwmBuffer_00018c34)(param_1,(int)*(short *)(iVar10 + iVar12));
  return;
}

