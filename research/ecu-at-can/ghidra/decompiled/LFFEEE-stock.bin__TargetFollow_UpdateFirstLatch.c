/* Ghidra analysis output; verify against original SH instructions. */

/* 692A reload20/decrement;693Eclear/set/retain. StockDB0BF0 clearonreloadcondition,
   timerexpirydoesnotclearlatch.3664direct/54eight-call/130retained/320pairedcycles;
   control-target-followers.txt. */

uint TargetFollow_UpdateFirstLatch(void)

{
  bool bVar1;
  undefined *puVar2;
  char cVar4;
  uint uVar3;
  uint uVar5;
  float extraout_fr0;
  
  puVar2 = PTR_FUN_00031cb8;
  bVar1 = (*PTR_DAT_00031cb4 & 0x10) == 0;
  cVar4 = (*(code *)PTR_FUN_00031cb8)(PTR_DAT_00031cbc);
  uVar3 = (*(code *)puVar2)(PTR_DAT_00031cc0);
  uVar3 = uVar3 & 0xff;
  if (uVar3 == 0) {
LAB_00031c74:
    uVar5 = 1;
  }
  else {
    if (cVar4 == '\0') {
      uVar3 = (*(code *)puVar2)(PTR_DAT_00031cc4);
      uVar3 = uVar3 & 0xff;
      if (uVar3 == 0) goto LAB_00031c74;
    }
    uVar5 = 0;
  }
  puVar2 = PTR_TargetFollow_FirstCountdown_00031cc8;
  if ((bVar1) || (uVar3 = uVar5, uVar5 == 1)) {
    *PTR_TargetFollow_FirstCountdown_00031cc8 = *PTR_DAT_00031ccc;
  }
  else {
    uVar3 = (uint)(byte)*PTR_TargetFollow_FirstCountdown_00031cc8;
    if (uVar3 != 0) {
      *PTR_TargetFollow_FirstCountdown_00031cc8 =
           *PTR_TargetFollow_FirstCountdown_00031cc8 + (char)DAT_00031dc2;
    }
  }
  if ((((bVar1) || (uVar3 = uVar5, uVar5 == 1)) &&
      ((*PTR_DAT_00031dc4 == '\0' || ((uVar5 == 1 && (uVar3 = 1, *PTR_DAT_00031dc4 == '\x01'))))))
     || ((cVar4 == '\0' && (uVar3 = (uint)(byte)*PTR_DAT_00031dc4, uVar3 == 2)))) {
    *PTR_TargetFollow_FirstRetainedFlag_00031dc8 = 0;
  }
  else {
    uVar3 = 0;
    if ((((*puVar2 != '\0') &&
         (uVar3 = (*(code *)PTR_FUN_00031dd4)(*(undefined4 *)PTR_DAT_00031dcc,PTR_DAT_00031dd0),
         extraout_fr0 <= *(float *)PTR_DAT_00031dd8)) &&
        (uVar3 = -(((*PTR_ControlMode_SelectedBit_00031ddc & 8) == 0) - 1), uVar3 == 1)) &&
       ((uVar3 = (uint)(char)*PTR_TransmissionModeFlags_00031de0, (uVar3 & 0x40) == 0 ||
        (uVar3 = (uint)(char)*PTR_DAT_00031de4, (uint)(int)(char)*PTR_DAT_00031de8 <= uVar3)))) {
      *PTR_TargetFollow_FirstRetainedFlag_00031dc8 = 1;
    }
  }
  return uVar3;
}

