/* Ghidra analysis output; verify against original SH instructions. */

/* 64 original wholeRAM/register cases writeDMAOR ECB0=0; unread AE/NMIF flags remain.32
   read-one/write-zero sequences PASS. NoDMA transfers; full15574 now stops14602 bytewriteF424=0.
   tcu-basic-hardware-startup.txt. */

void Startup_DisableDMAOperation(void)

{
  *(undefined2 *)(int)DAT_00014526 = 0;
  return;
}

