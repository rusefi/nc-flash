/* Ghidra analysis output; verify against original SH instructions. */

/* 7002 override sets1;734C==1 uses CAN231 selector flags6AD2/6AD4;else inverted44A4 bit0. Writes
   protected723A and7244. Paired execution verified. */

void Selector_UpdateCombinedFlag(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar4;
  undefined4 uVar3;
  
  puVar2 = PTR_FUN_00041350;
  puVar1 = PTR_FUN_0004134c;
  cVar4 = (*(code *)PTR_FUN_0004134c)(PTR_DAT_00041354);
  if (cVar4 == '\x01') {
    (*(code *)puVar2)(PTR_Selector_CombinedFlag_00041358,1);
  }
  else {
    cVar4 = (*(code *)puVar1)(PTR_ATReceiveConfigurationGate_0004135c);
    if (cVar4 == '\x01') {
      if ((*PTR_DAT_00041360 == '\x01') || (*PTR_DAT_00041364 == '\x01')) {
        uVar3 = 1;
      }
      else {
        uVar3 = 0;
      }
      (*(code *)puVar2)(PTR_Selector_CombinedFlag_00041358,uVar3);
    }
    else {
      (*(code *)puVar2)(PTR_Selector_CombinedFlag_00041358,
                        (*PTR_Input_FilteredSerialBankOne_00041368 & 1) == 0);
    }
  }
  uVar3 = (*(code *)puVar1)(PTR_Selector_CombinedFlag_00041358);
  (*(code *)puVar2)(PTR_DAT_0004136c,uVar3);
  return;
}

