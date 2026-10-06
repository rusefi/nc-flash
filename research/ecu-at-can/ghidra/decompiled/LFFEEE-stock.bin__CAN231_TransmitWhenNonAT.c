/* Ghidra analysis output; verify against original SH instructions. */

/* 25-count threshold after u16 increment; sends when mode bit40 set OR734C==0. Initializer36D40
   seedsFFFE and falls through for an immediate eligible attempt.6144 admission cases stop before
   driver6A48; no hardware transmission claim. See mt-can231.txt. */

void CAN231_TransmitWhenNonAT(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  int iVar4;
  
  puVar1 = PTR_CAN231_ECUTxCounter_00036e14;
  *(short *)PTR_CAN231_ECUTxCounter_00036e14 = *(short *)PTR_CAN231_ECUTxCounter_00036e14 + 1;
  if (0x18 < *(ushort *)puVar1) {
    if (((*PTR_TransmissionModeFlags_00036e1c & 0x40) != 0) ||
       (cVar3 = (*(code *)PTR_FUN_00036e24)(PTR_ATReceiveConfigurationGate_00036e20), cVar3 == '\0')
       ) {
      (*(code *)PTR_FUN_00036e2c)(PTR_CAN231_TxDescriptor_00036e28);
    }
    puVar2 = PTR_FUN_00036e30;
    iVar4 = (int)DAT_00036e0e;
    *(undefined2 *)puVar1 = 0;
    (*(code *)puVar2)(iVar4);
    return;
  }
  return;
}

