/* Ghidra analysis output; verify against original SH instructions. */

/* Two91728 bytes AND indexed AC148 pair;return1 onlyno match. B4 stockpair8000
   meansinhibitwhen99D8bit15clear. Executedfullgatepath. */

undefined4 Diagnostic_CheckModeMaskMismatch(uint param_1)

{
  undefined *puVar1;
  byte bVar2;
  undefined4 uVar3;
  uint uVar4;
  
  puVar1 = PTR_DAT_0009a4a4;
  uVar3 = 1;
  for (uVar4 = 0; (int)uVar4 < 2; uVar4 = uVar4 + 1) {
    bVar2 = (*(code *)PTR_Diagnostic_ReadModeByte_0009a4a8)(uVar4 & 0xff);
    if ((bVar2 & puVar1[uVar4 + (param_1 & 0xffff) * 2]) != 0) {
      uVar3 = 0;
    }
  }
  return uVar3;
}

