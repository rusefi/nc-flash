/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00023490) */
/* 92D5bit7 rising resets82C4;938Cbit0 mirrorsfault. Healthy880C*256/10 capped25600; fault branches
   both stock25600 across timer31.15360 input/fault/timer cases. */

int Primary_ConvertCANInput(void)

{
  bool bVar1;
  undefined *puVar2;
  byte bVar5;
  int iVar3;
  short sVar4;
  int extraout_r3;
  byte *pbVar6;
  
  puVar2 = PTR_Primary_FaultElapsedTimer_00023488;
  bVar1 = ((int)(char)*PTR_ApplicationFaultFlags92D5_00023484 & 0x80U) != 0;
  pbVar6 = (byte *)(int)DAT_00023466;
  if (((*pbVar6 & 1) == 0) && (bVar1)) {
    *PTR_Primary_FaultElapsedTimer_00023488 = 0;
  }
  if (bVar1) {
    bVar5 = *pbVar6 | 1;
  }
  else {
    bVar5 = *pbVar6 & 0xfe;
  }
  *pbVar6 = bVar5;
  if (bVar1) {
    iVar3 = (int)*(short *)PTR_DAT_000234ec;
    if ((byte)*puVar2 < (byte)*PTR_DAT_000234f0) {
      iVar3 = (int)*(short *)PTR_DAT_000234f4;
    }
  }
  else {
    iVar3 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00023474)
                      ((uint)*(ushort *)PTR_CAN215_PrimaryDecodedValue_0002348c << 8,10);
    sVar4 = (*(code *)PTR_FUN_000234e4)(iVar3);
    if (sVar4 < extraout_r3) {
      sVar4 = (*(code *)PTR_FUN_000234e4)();
      iVar3 = (int)sVar4;
    }
  }
  return iVar3;
}

