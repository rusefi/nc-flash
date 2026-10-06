/* Ghidra analysis output; verify against original SH instructions. */

/* Word5 accepted at6A56: MT ->0; FFFF ->65537; else max(0,raw*binary32(0.01)-100) ->6E18. Paired
   setter/receiver execution. */

undefined4 * CAN216_ConvertSpeedFallback(void)

{
  undefined4 *puVar1;
  float extraout_fr0;
  float fVar2;
  float fVar3;
  
  fVar3 = 0.0;
  if ((*PTR_TransmissionModeFlags_0003b8ec & 0x40) == 0) {
    if (*(ushort *)PTR_DAT_0003b914 == DAT_0003b918) {
      puVar1 = &DAT_0003b91c;
      fVar2 = DAT_0003b91c;
    }
    else {
      puVar1 = (undefined4 *)(*(code *)PTR_FUN_0003b928)(DAT_0003b924,DAT_0003b920);
      fVar2 = extraout_fr0;
      if (extraout_fr0 < 0.0) {
        fVar2 = fVar3;
      }
    }
  }
  else {
    puVar1 = (undefined4 *)0x1;
    fVar2 = 0.0;
  }
  *(float *)PTR_CAN216_SpeedCandidateFallback_0003b92c = fVar2;
  return puVar1;
}

