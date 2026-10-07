/* Ghidra analysis output; verify against original SH instructions. */

/* 6CD4 divided by0.5, adds0.5, truncates/clamps0..255 through20B8, caps200. A3A4 exact1
   forcesFF.36A28 packsbyte6.288 encoder cases including hold mode; tcu-paired-input.txt. */

char CAN215_EncodeSelectedControlByte(void)

{
  undefined *puVar1;
  byte bVar2;
  char cVar3;
  undefined4 uVar4;
  
  uVar4 = (*(code *)PTR_FUN_00036c54)(PTR_DAT_00036c5c);
  bVar2 = (*(code *)PTR_FUN_00036c64)(uVar4,DAT_00036c60,0);
  puVar1 = PTR_CAN215_SelectedControlByte_00036c68;
  cVar3 = (*(code *)PTR_FUN_00036c70)(PTR_DAT_00036c6c);
  if (cVar3 == '\x01') {
    *puVar1 = (char)DAT_00036c30;
  }
  else if (DAT_00036c32 < (short)(ushort)bVar2) {
    *puVar1 = (char)DAT_00036c32;
  }
  else {
    *puVar1 = bVar2;
  }
  return cVar3;
}

