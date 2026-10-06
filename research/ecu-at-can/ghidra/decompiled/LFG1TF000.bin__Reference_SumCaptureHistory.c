/* Ghidra analysis output; verify against original SH instructions. */

/* Count=int16-clamp(param*18/360); signed32-wrapped sum backwards from current91B4 modulo18.162
   angle/head cases; MACL preserved. See tcu-reference-source.txt. */

int Reference_SumCaptureHistory(short param_1)

{
  short sVar2;
  undefined4 uVar1;
  byte bVar3;
  int iVar4;
  int iVar5;
  
  sVar2 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00020868)
                    ((int)(short)(ushort)(byte)*PTR_DAT_00020848 * (int)param_1,(int)DAT_00020846);
  iVar5 = 0;
  uVar1 = (*(code *)PTR_FUN_00020858)();
  bVar3 = *(byte *)(int)DAT_00020840;
  iVar4 = 0;
  if (0 < sVar2) {
    do {
      iVar5 = iVar5 + *(int *)(PTR_Reference_CaptureHistory_0002084c + (uint)bVar3 * 4);
      if (bVar3 == 0) {
        bVar3 = *PTR_DAT_00020848;
      }
      iVar4 = iVar4 + 1;
      bVar3 = bVar3 - 1;
    } while (iVar4 < sVar2);
  }
  (*(code *)PTR_FUN_0002085c)(uVar1);
  return iVar5;
}

