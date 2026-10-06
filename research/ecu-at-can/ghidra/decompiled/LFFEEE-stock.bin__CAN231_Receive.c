/* Ghidra analysis output; verify against original SH instructions. */

/* Active AT receives frame 231; see mutually gated ECU transmitter. */

uint CAN231_Receive(void)

{
  uint uVar1;
  
  uVar1 = (uint)(char)*PTR_TransmissionModeFlags_0003582c;
  if ((uVar1 & 0x40) == 0) {
    uVar1 = (*(code *)PTR_FUN_00035834)(PTR_ATReceiveConfigurationGate_00035830);
    uVar1 = uVar1 & 0xff;
    if (uVar1 == 1) {
      uVar1 = (*(code *)PTR_FUN_0003583c)(PTR_CAN231_RxDescriptor_00035838);
      uVar1 = uVar1 & 0xff;
      if (uVar1 == 0) {
        (*(code *)PTR_FUN_00035840)();
        CAN231_Unpack();
        uVar1 = FUN_00035bda();
        return uVar1;
      }
    }
  }
  return uVar1;
}

