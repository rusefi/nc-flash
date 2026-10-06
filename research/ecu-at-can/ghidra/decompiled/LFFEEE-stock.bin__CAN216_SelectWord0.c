/* Ghidra analysis output; verify against original SH instructions. */

/* Selects6A34 into6E04 under local gates; now executed fromTCU18F10 through3B5C6/5295C to
   per-cylinder spark. MT/local substitutions remain distinct; spark-interaction.txt. */

undefined4 * CAN216_SelectWord0(void)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  
  puVar1 = (undefined4 *)-(((*PTR_TransmissionModeFlags_0003b65c & 0x40) == 0) - 1);
  if (puVar1 == (undefined4 *)0x1) {
    *(undefined4 *)PTR_CAN216_SelectedNumericRequest_0003b6bc = 0;
  }
  else {
    if ((*PTR_DAT_0003b6c0 == '\0') && (*PTR_DAT_0003b6c4 == '\0')) {
      uVar2 = *DAT_0003b6cc;
    }
    else {
      puVar1 = &DAT_0003b6c8;
      uVar2 = DAT_0003b6c8;
    }
    *(undefined4 *)PTR_CAN216_SelectedNumericRequest_0003b6bc = uVar2;
  }
  return puVar1;
}

