/* Ghidra analysis output; verify against original SH instructions. */

/* 960wholeRAM cases PASS:if414C0, TSR10F6E8 read/write0B/read,80D4compare/counterconfig,
   E744ORmask4intoTIER10F6EA,414C1. Nonzero414Cpreserves.544Timer10latchcases/5rejects. Mask4CME10B,
   notbitindex4/IREG. Noevents/physicalinterrupts. control-timer-event2.txt. */

void Control_EnableCaptureCompare10B(void)

{
  if (*PTR_DAT_00007dd0 == '\0') {
    *(undefined2 *)(int)DAT_00007dc6 = 0xb;
    Timer10_ConfigureEventCompare();
    (*DAT_00007dd4)((int)DAT_00007dc8,4,1);
    *PTR_DAT_00007dd0 = 1;
  }
  return;
}

