/* Ghidra analysis output; verify against original SH instructions. */

/* Action1 skips groups36/37/38 whenGSRconfiguration,8BCD!=0 orA721mask04.16 combinations verified;
   skipped producer leaves previous raw bytes unchanged. */

uint CAN_GateReceiveDiagnosticsDuringRecovery(uint param_1)

{
  uint uVar1;
  
  param_1 = param_1 & 0xff;
  if (param_1 == 0) {
    CAN_EvaluateReceiveQualification(0,0x36);
    CAN_EvaluateReceiveQualification(0,0x37);
    uVar1 = CAN_EvaluateReceiveQualification(0,0x38);
    return uVar1;
  }
  if (param_1 == 1) {
    param_1 = (*(code *)PTR_HCAN_ReadConfigurationStatus_0001a114)();
    if ((((param_1 & 0xffff) == 0) &&
        (param_1 = (uint)(byte)*PTR_DAT_0001a118, (*PTR_DAT_0001a118 & 4) == 0)) &&
       (*(char *)(int)DAT_0001a0fa == '\0')) {
      CAN_EvaluateReceiveQualification(1,0x36,0);
      CAN_EvaluateReceiveQualification(1,0x37,0);
      uVar1 = CAN_EvaluateReceiveQualification(1,0x38,0);
      return uVar1;
    }
  }
  else if (param_1 != 7) {
    return param_1;
  }
  return param_1;
}

