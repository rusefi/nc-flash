/* Ghidra analysis output; verify against original SH instructions. */

/* 20DF8->91A2; full209B4 selects80EC and return->80EA, shiftedcap800B;
   historydelta91A0,207DE(60)->919C,20EAA->91A4,tail50EA4.450 full-caller branch fixtures and3
   both-capture shift lifecycles. Other outputs not all independently asserted. See
   tcu-reference-source.txt. */

void Reference_UpdateSourceAndDerivedValues(void)

{
  short sVar1;
  short sVar2;
  short sVar3;
  undefined *puVar4;
  undefined2 uVar6;
  short sVar7;
  undefined4 uVar5;
  short *psVar8;
  int iVar9;
  
  uVar6 = Motion_CalculateRawPeriodValue();
  *(undefined2 *)PTR_Motion_PeriodDerivedValue_0002097c = uVar6;
  sVar7 = Reference_SelectMeasuredOrHistorySource();
  iVar9 = (int)sVar7 >> 6;
  if (DAT_00020970 < iVar9) {
    iVar9 = (int)DAT_00020970;
  }
  uVar5 = Reference_SumCaptureHistory(0x3c);
  psVar8 = (short *)(int)DAT_00020972;
  sVar1 = *psVar8;
  sVar2 = psVar8[1];
  sVar3 = psVar8[2];
  psVar8[2] = sVar2;
  psVar8[1] = *psVar8;
  puVar4 = PTR_FUN_00020980;
  *psVar8 = sVar7;
  (*(code *)puVar4)();
  DAT_ffff80ea = sVar7;
  *(undefined4 *)PTR_DAT_00020984 = uVar5;
  DAT_ffff800b = (undefined1)iVar9;
  *(short *)PTR_DAT_00020988 = (short)((((int)sVar1 - (int)sVar2) - (int)sVar3) + (int)sVar7 >> 2);
  uVar6 = Reference_SelectAlternateCachedValue();
  *(undefined2 *)PTR_Reference_AlternatePublishedValue_0002098c = uVar6;
  (*(code *)PTR_FUN_00020990)();
  return;
}

