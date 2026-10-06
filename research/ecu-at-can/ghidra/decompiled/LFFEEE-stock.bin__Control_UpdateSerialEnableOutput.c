/* Ghidra analysis output; verify against original SH instructions. */

/* 5676=(566Bzero&&updated5668<201);original22E4/E744/22F4
   writesPDDRbit11,preservesotherbits/restoresinterruptmask. Physicalpinroleopen. */

void Control_UpdateSerialEnableOutput(void)

{
  undefined *puVar1;
  undefined4 local_c [2];
  
  puVar1 = PTR_Control_SerialEnableOutput_00024c30;
  if ((*PTR_Control_OverrideBypassResult_00024c0c == '\0') &&
     (*(ushort *)PTR_Control_RelativeOverrideTimer_00024c28 < *(ushort *)PTR_DAT_00024c34)) {
    *PTR_Control_SerialEnableOutput_00024c30 = 1;
  }
  else {
    *PTR_Control_SerialEnableOutput_00024c30 = 0;
  }
  (*(code *)PTR_FUN_00024d28)(local_c,(int)DAT_00024d20);
  (*(code *)PTR_Register_UpdateMaskedWord_00024d2c)
            ((int)DAT_00024d24,(int)DAT_00024d22,*puVar1 == '\x01');
  (*(code *)PTR_FUN_00024d30)(local_c[0]);
  return;
}

