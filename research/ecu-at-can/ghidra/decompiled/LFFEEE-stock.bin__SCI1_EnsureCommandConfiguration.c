/* Ghidra analysis output; verify against original SH instructions. */

/* 256 bytepatterns verify SMR80,BRR4,SCR low2clear,SDCR F2 onlywhenbit3set. Registermap
   corroborated SH7058manual;control-serial.txt. */

undefined4 SCI1_EnsureCommandConfiguration(void)

{
  byte bVar1;
  undefined4 uVar2;
  undefined4 uStack_c;
  undefined4 auStack_8 [2];
  
  (*(code *)PTR_FUN_0000bf18)(auStack_8,(int)DAT_0000bf06);
  (*(code *)PTR_FUN_0000bf18)(&uStack_c,(int)DAT_0000bf06);
  if (*(byte *)(int)DAT_0000bf0c != DAT_0000bf0a) {
    *(byte *)(int)DAT_0000bf0c = (byte)DAT_0000bf0a;
  }
  bVar1 = *(byte *)(int)DAT_0000bf0e;
  if ((bVar1 & 3) != 0) {
    *(byte *)(int)DAT_0000bf0e = bVar1 & (byte)DAT_0000bf14;
  }
  if ((*(byte *)(int)DAT_0000bf10 & 8) != 0) {
    *(byte *)(int)DAT_0000bf10 = (byte)DAT_0000bf16;
  }
  if (*(char *)(int)DAT_0000bf12 != '\x04') {
    *(char *)(int)DAT_0000bf12 = '\x04';
  }
  (*(code *)PTR_FUN_0000bf20)(uStack_c);
  uVar2 = (*(code *)PTR_FUN_0000bf20)(auStack_8[0]);
  return uVar2;
}

