/* Ghidra analysis output; verify against original SH instructions. */

/* Sets status01 at61D3+2*group, updates next byte and setsA99B for record flags04. Group36C7
   reaches CAN216 byte7 bit1. */

byte Diagnostic_LatchReportFlag(byte param_1)

{
  byte bVar1;
  int iVar2;
  undefined *puVar3;
  byte *pbVar4;
  int iVar5;
  
  puVar3 = PTR_DAT_00057a1c;
  iVar2 = DAT_00057a18;
  iVar5 = (uint)param_1 * 2;
  pbVar4 = (byte *)(DAT_00057a18 + 0x4b + iVar5);
  *pbVar4 = *pbVar4 | 1;
  pbVar4 = (byte *)(iVar2 + iVar5 + 0x4c);
  *pbVar4 = *pbVar4 & 0x3f | 0xc0;
  pbVar4 = (byte *)(iVar2 + iVar5 + 0x4c);
  *pbVar4 = *pbVar4 & 0xc0 | 0x28;
  bVar1 = puVar3[(uint)param_1 * 0x10];
  if ((bVar1 & 4) != 0) {
    *(undefined1 *)(int)DAT_00057a16 = 1;
  }
  return bVar1;
}

