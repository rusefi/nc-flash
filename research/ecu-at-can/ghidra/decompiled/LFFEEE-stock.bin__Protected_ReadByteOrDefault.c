/* Ghidra analysis output; verify against original SH instructions. */

/* Value/complementcheck;invalidusesR5default,recordsaddressat534C,calls157F0toset5354.
   Sparsefixtureinvalid210C/2076/2088/208A affectscommandmode1;control-timers.txt. */

int Protected_ReadByteOrDefault(byte *param_1,byte param_2)

{
  byte bVar1;
  undefined *puVar2;
  undefined4 local_14;
  byte bStack_10;
  
  bStack_10 = param_2;
  (*(code *)PTR_FUN_000151e4)(&local_14,(int)DAT_000151d8);
  bVar1 = bStack_10;
  puVar2 = PTR_Protected_MarkInvalidRead_000151ec;
  if (*param_1 == (byte)~param_1[1]) {
    bVar1 = *param_1;
  }
  else {
    *(byte **)PTR_Protected_InvalidByteRecordAddress_000151e8 = param_1;
    (*(code *)puVar2)();
  }
  (*(code *)PTR_FUN_000151f0)(local_14);
  return (int)(char)bVar1;
}

