/* Ghidra analysis output; verify against original SH instructions. */

/* History/class/operation5 retention of9BF1bit0/9BEE; acceptedfall captures9BEC
   whileactive/release0/op5. Othercases reset usingoriginaldouble0.5->0conversion;288directcases. */

void Selection_UpdateOverlayMeasurementLatch(char param_1,uint param_2)

{
  byte bVar1;
  char cVar2;
  uint uVar3;
  undefined2 uVar4;
  undefined2 *puVar5;
  uint uVar6;
  
  uVar3 = (uint)(char)CAN231_SixStateSource;
  bVar1 = *(byte *)(int)DAT_000460cc;
  uVar6 = (uint)(char)bVar1;
  cVar2 = *PTR_DAT_000460d4;
  if ((((param_1 == '\0') || (*(char *)(int)DAT_000460ca < (char)TransmissionStateClass)) ||
      (bVar1 < CAN231_SixStateSource)) ||
     ((CAN231_SixStateSource < bVar1 && (((param_2 & 0xff) == 1 || (cVar2 != '\x05')))))) {
    *(byte *)(int)DAT_000460ce = *(byte *)(int)DAT_000460ce & 0xfe;
    uVar4 = (*(code *)PTR_FUN_000460dc)();
    *(undefined2 *)(int)DAT_000460d0 = uVar4;
  }
  if (((param_1 == '\x01') && ((uVar3 & 0xff) < (uVar6 & 0xff))) &&
     (((param_2 & 0xff) == 0 && (cVar2 == '\x05')))) {
    puVar5 = (undefined2 *)(int)DAT_000460d2;
    *(byte *)(int)DAT_000460ce = *(byte *)(int)DAT_000460ce | 1;
    *(undefined2 *)(int)DAT_000460d0 = *puVar5;
  }
  return;
}

