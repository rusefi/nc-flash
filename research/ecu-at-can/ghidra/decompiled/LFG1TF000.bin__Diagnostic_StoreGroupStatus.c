/* Ghidra analysis output; verify against original SH instructions. */

/* Stores R5 byte atA736+group R4; updatesA6EC+group bit80 according to status06/80. Software status
   only; final DTC mapping unresolved. */

uint Diagnostic_StoreGroupStatus(uint param_1,byte param_2)

{
  undefined *puVar1;
  uint uVar2;
  char *pcVar3;
  byte *pbVar4;
  
  puVar1 = PTR_DAT_000566d4;
  param_1 = param_1 & 0xff;
  uVar2 = (uint)DAT_000566c0;
  *(byte *)(param_1 + uVar2) = param_2;
  if ((param_2 & 6) != 0) {
    pcVar3 = puVar1 + param_1;
    uVar2 = (int)*pcVar3 & 0x7f;
    *pcVar3 = (char)uVar2;
    return uVar2;
  }
  if ((DAT_000566c6 & param_2) != 0) {
    pbVar4 = puVar1 + param_1;
    *pbVar4 = *pbVar4 | (byte)DAT_000566c6;
  }
  return uVar2;
}

