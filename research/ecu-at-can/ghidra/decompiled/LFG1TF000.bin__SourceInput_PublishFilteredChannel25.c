/* Ghidra analysis output; verify against original SH instructions. */

/* Calls173CE(25),copies filtered8895 to89A4,always sets89A5=2. Does not forward filter status8897=3
   on ADC invalidity; retained eleven-call probe. Physical switch identity open;
   tcu-source-selection.txt. */

void SourceInput_PublishFilteredChannel25(void)

{
  undefined1 uVar1;
  undefined1 *puVar2;
  
  uVar1 = (*(code *)PTR_Input_GetFilteredState_00017d7c)(0x19);
  puVar2 = (undefined1 *)(int)DAT_00017d78;
  *(undefined1 *)(int)DAT_00017d76 = uVar1;
  *puVar2 = 2;
  return;
}

