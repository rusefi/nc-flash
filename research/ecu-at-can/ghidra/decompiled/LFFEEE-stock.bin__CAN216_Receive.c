/* Ghidra analysis output; verify against original SH instructions. */

/* Poll descriptor 3790C only if mode bit 40 clear and FFFF734C == 1. */

uint CAN216_Receive(void)

{
  uint uVar1;
  
  uVar1 = (uint)(char)*PTR_TransmissionModeFlags_00034cbc;
  if ((uVar1 & 0x40) == 0) {
    uVar1 = (*(code *)PTR_FUN_00034cc4)(PTR_ATReceiveConfigurationGate_00034cc0);
    uVar1 = uVar1 & 0xff;
    if (uVar1 == 1) {
      uVar1 = (*(code *)PTR_FUN_00034ccc)(PTR_CAN216_RxDescriptor_00034cc8);
      uVar1 = uVar1 & 0xff;
      if (uVar1 == 0) {
        (*(code *)PTR_FUN_00034cd0)();
        CAN216_Unpack();
        uVar1 = FUN_00035078();
        return uVar1;
      }
    }
  }
  return uVar1;
}

