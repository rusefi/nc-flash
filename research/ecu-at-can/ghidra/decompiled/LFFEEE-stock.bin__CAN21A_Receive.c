/* Ghidra analysis output; verify against original SH instructions. */

/* Static: mode734A bit40 OR80 polls descriptor3792C then348E2/unpack/reload; peripheral wrapper not
   executed. */

uint CAN21A_Receive(void)

{
  uint uVar1;
  
  if (((*PTR_TransmissionModeFlags_000356a4 & 0x40) != 0) ||
     (uVar1 = -((((int)(char)*PTR_TransmissionModeFlags_000356a4 & 0x80U) == 0) - 1), uVar1 == 1)) {
    uVar1 = (*(code *)PTR_FUN_000356ac)(PTR_CAN21A_RxDescriptor_000356a8);
    uVar1 = uVar1 & 0xff;
    if (uVar1 == 0) {
      (*DAT_000356b0)();
      CAN21A_Unpack();
      uVar1 = CAN21A_ReloadReceiptCounter();
      return uVar1;
    }
  }
  return uVar1;
}

