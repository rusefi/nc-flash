/* Ghidra analysis output; verify against original SH instructions. */

/* Index0..3 uses11228;hardware byte19 gate,alternate20 branch clearsTIER8
   bit;otherwisecompare=TCNT1A-1 and ifDSTRbitclear writesDCNTzero twice.720 register-sample cases;
   no pin simulation. */

void Output_CancelTimerChannel(uint param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  int iVar4;
  undefined4 local_18 [2];
  
  puVar1 = PTR_Output_TimerSoftwareRecords_00009834;
  iVar4 = (param_1 & 0xff) * 0x18;
  if (PTR_Output_TimerSoftwareRecords_00009834[iVar4 + 0x13] == '\0') {
    (*(code *)PTR_FUN_00009838)(local_18,(int)DAT_0000982a);
    puVar2 = PTR_Output_TimerChannels_0000983c;
    uVar3 = param_1 & 0xff;
    if (puVar1[iVar4 + 0x14] == '\x01') {
      (*(code *)PTR_Register_UpdateMaskedWord_00009840)
                ((int)DAT_0000982c,
                 (int)*(short *)(PTR_Output_TimerChannels_0000983c + uVar3 * 0xc + 8),0);
      puVar1[iVar4 + 0x14] = 0;
    }
    else {
      **(short **)(PTR_Output_TimerChannels_0000983c + uVar3 * 0xc + 4) =
           *(short *)(int)DAT_0000982e + (short)DAT_00009844;
      if ((*(ushort *)(puVar2 + uVar3 * 0xc + 8) & *(ushort *)(int)DAT_00009830) == 0) {
        (*(code *)PTR_Output_WriteCounterTwice_00009848)
                  (*(undefined4 *)(PTR_Output_TimerChannels_0000983c + (param_1 & 0xff) * 0xc),0);
      }
    }
    (*(code *)PTR_FUN_0000984c)(local_18[0]);
  }
  puVar1[iVar4 + 0x13] = 0;
  return;
}

