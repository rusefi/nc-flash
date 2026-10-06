/* Ghidra analysis output; verify against original SH instructions. */

/* Descriptor378EC; admitted if734A bit40 or80. Calls unpack34B8C and counter reload34BB2 on
   receipt. Sender unproven. */

uint CAN211_Receive(void)

{
  uint uVar1;
  
  if (((*PTR_TransmissionModeFlags_00034a10 & 0x40) != 0) ||
     (uVar1 = -((((int)(char)*PTR_TransmissionModeFlags_00034a10 & 0x80U) == 0) - 1), uVar1 == 1)) {
    uVar1 = (*(code *)PTR_FUN_00034a18)(PTR_CAN_Descriptor_ARRAY_000378cc_2__can_id_00034a14);
    uVar1 = uVar1 & 0xff;
    if (uVar1 == 0) {
      (*DAT_00034a1c)();
      CAN211_Unpack();
      uVar1 = CAN211_ReloadReceiptCounter();
      return uVar1;
    }
  }
  return uVar1;
}

