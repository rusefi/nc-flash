/* Ghidra analysis output; verify against original SH instructions. */

/* 64completeleaf/64actual15574..1558C caller cases verify12orderedwordwrites
   andwholeapplicationRAM. ED12=0980 viaED0C+6; compatibleSH7055S CMT0priority9/CMT1priority8.
   Hardwareacceptance/nesting unproved. tcu-interrupt-setup.txt. */

void INTC_InitializePriorities(void)

{
  undefined2 *puVar1;
  undefined2 *puVar2;
  
  *(undefined2 *)(int)DAT_000144ec = 0;
  *(undefined2 *)(int)DAT_000144ee = 0;
  *(undefined2 *)(int)DAT_000144f0 = 0xd;
  *(undefined2 *)(int)DAT_000144f2 = 0x30;
  *(undefined2 *)(int)DAT_000144f6 = DAT_000144f4;
  puVar2 = (undefined2 *)(int)DAT_000144fa;
  *puVar2 = DAT_000144f8;
  puVar1 = (undefined2 *)(int)DAT_000144fe;
  *puVar1 = DAT_000144fc;
  *(undefined2 *)(int)DAT_00014502 = DAT_00014500;
  puVar2[3] = 0;
  puVar1[3] = DAT_00014504;
  *(undefined2 *)(int)DAT_00014506 = 6;
  *(undefined2 *)(int)DAT_0001450a = DAT_00014508;
  return;
}

