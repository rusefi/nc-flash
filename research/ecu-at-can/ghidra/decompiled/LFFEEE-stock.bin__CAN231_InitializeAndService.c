/* Ghidra analysis output; verify against original SH instructions. */

/* Seeds6B6C=FFFE,calls MT builders and packer, then falls through36D52. First service
   incrementsFFFF and can request TX immediately.16 initializer cases stop before actual driver. */

undefined4 CAN231_InitializeAndService(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined4 uVar3;
  char cVar4;
  int iVar5;
  
  puVar1 = PTR_CAN231_BuildMTFields_00036e18;
  *(short *)PTR_CAN231_ECUTxCounter_00036e14 = (short)DAT_00036e10;
  (*(code *)puVar1)();
  uVar3 = CAN231_PackWhenNonAT();
  puVar1 = PTR_CAN231_ECUTxCounter_00036e14;
  *(short *)PTR_CAN231_ECUTxCounter_00036e14 = *(short *)PTR_CAN231_ECUTxCounter_00036e14 + 1;
  if (0x18 < *(ushort *)puVar1) {
    if (((*PTR_TransmissionModeFlags_00036e1c & 0x40) != 0) ||
       (cVar4 = (*(code *)PTR_FUN_00036e24)(PTR_ATReceiveConfigurationGate_00036e20), cVar4 == '\0')
       ) {
      (*(code *)PTR_FUN_00036e2c)(PTR_CAN231_TxDescriptor_00036e28);
    }
    puVar2 = PTR_FUN_00036e30;
    iVar5 = (int)DAT_00036e0e;
    *(undefined2 *)puVar1 = 0;
    uVar3 = (*(code *)puVar2)(iVar5);
    return uVar3;
  }
  return uVar3;
}

