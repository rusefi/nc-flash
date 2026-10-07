/* Ghidra analysis output; verify against original SH instructions. */

/* ReadsADCSR1 F838 andwritesold&7F then tailcalls4DFE. All256softwarestatusbytesverified. VBRFFC50
   offset308 via2FA8 mapsADI1 perRenesas; wrapper/interruptdelivery unexecuted. */

void Acquisition_AcknowledgeAdi1(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_Acquisition_FollowCompletion_0000f354;
  *(byte *)(int)DAT_0000f330 = *(byte *)(int)DAT_0000f330 & 0x7f;
  (*(code *)puVar1)();
  return;
}

