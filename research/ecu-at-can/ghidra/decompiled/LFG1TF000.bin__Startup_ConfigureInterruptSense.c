/* Ghidra analysis output; verify against original SH instructions. */

/* 1024 original wholeRAM/register cases:RTSdelay-slot14428 writes00FF toICR ED18. 2048 ownercases
   preserve externally sampledNMILbit15; controls8..0 writable/reserved14..9 reject. No IRQ/NMI
   arrival. tcu-icr-startup.txt. */

void Startup_ConfigureInterruptSense(void)

{
  *(undefined2 *)(int)DAT_0001450e = DAT_0001450c;
  return;
}

