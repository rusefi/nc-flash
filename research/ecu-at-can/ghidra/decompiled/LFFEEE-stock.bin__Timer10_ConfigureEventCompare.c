/* Ghidra analysis output; verify against original SH instructions. */

/* 256stock wholeRAM cases:ROM DC3A9=0 uses(ROM1115D+2*byte4119)&7F ->OCR10B F6D8 thenTCNT10B
   F6C4=0,shadow414B. Strictbyte noAGCK fixture;notclock/pinproof. control-initialize-timer.txt. */

void Timer10_ConfigureEventCompare(void)

{
  byte bVar1;
  
  bVar1 = 0;
  if (*PTR_DAT_000081c4 != 'Z') {
    bVar1 = PTR_DAT_000081cc[(uint)(byte)*PTR_DAT_000081c8 * 2] & 0x7f;
  }
  *(byte *)(int)DAT_000081bc = bVar1;
  *(undefined1 *)(int)DAT_000081be = 0;
  *PTR_DAT_000081d0 = bVar1;
  return;
}

