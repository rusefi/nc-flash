/* Ghidra analysis output; verify against original SH instructions. */

/* Poll descriptor 3791C only if mode bit 40 clear and FFFF734C == 1. */

uint CAN218_Receive(void)

{
  uint uVar1;
  
  uVar1 = (uint)(char)*PTR_TransmissionModeFlags_000351e8;
  if ((uVar1 & 0x40) == 0) {
    uVar1 = (*(code *)PTR_FUN_000351f0)(PTR_ATReceiveConfigurationGate_000351ec);
    uVar1 = uVar1 & 0xff;
    if (uVar1 == 1) {
      uVar1 = (*(code *)PTR_FUN_000351f8)(PTR_CAN218_RxDescriptor_000351f4);
      uVar1 = uVar1 & 0xff;
      if (uVar1 == 0) {
        (*(code *)PTR_FUN_000351fc)();
        CAN218_Unpack();
        uVar1 = FUN_0003545e();
        return uVar1;
      }
    }
  }
  return uVar1;
}

