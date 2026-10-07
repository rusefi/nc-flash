/* Ghidra analysis output; verify against original SH instructions. */

/* 128wholeRAM cases
   PASS:19stockdescriptors,allmodemasks1;mode0writesbyte0=0/byte2=FF/byte3=ROMdefault;
   modes1..3preserve. Task4availability2. Suppliedmode,notfull3DD8bootproof.
   control-queued-event2.txt. */

void Control_InitializeTaskAvailability(void)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  undefined1 *puVar4;
  undefined *puVar5;
  int iVar6;
  
  puVar2 = PTR_DAT_00003ff8;
  puVar1 = PTR_FUN_00003ff4;
  iVar6 = 0;
  puVar5 = PTR_DAT_00003ff0;
  if (0 < *(short *)PTR_DAT_00003ff8) {
    do {
      iVar3 = (*(code *)puVar1)(iVar6);
      if (iVar3 == 0) {
        puVar4 = *(undefined1 **)(puVar5 + 4);
        puVar4[2] = 0xff;
        *puVar4 = 0;
        puVar4[3] = puVar5[0xc];
      }
      iVar6 = iVar6 + 1;
      puVar5 = puVar5 + 0x10;
    } while ((short)iVar6 < *(short *)puVar2);
  }
  return;
}

