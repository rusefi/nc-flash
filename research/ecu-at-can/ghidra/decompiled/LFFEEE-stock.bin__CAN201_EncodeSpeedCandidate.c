/* Ghidra analysis output; verify against original SH instructions. */

/* 6D58 -> (value+100)/0.01 +0.5 then truncate/clamp10000..40000. 8EC6=1 OR6E18>65536 forcesFFFF
   even when4B0 selected. */

undefined4 * CAN201_EncodeSpeedCandidate(void)

{
  ushort uVar2;
  undefined4 *puVar1;
  undefined *puVar3;
  
  uVar2 = (*(code *)PTR_FUN_0003684c)
                    (*(undefined4 *)PTR_SpeedCandidate_Selected_0003686c,DAT_00036874,DAT_00036870);
  puVar1 = (undefined4 *)0x1;
  if ((*PTR_DAT_00036878 == '\x01') ||
     (puVar1 = &DAT_0003687c, DAT_0003687c < *(float *)PTR_CAN216_SpeedCandidateFallback_00036880))
  {
    *(short *)PTR_CAN201_SpeedCandidateWord_000367e8 = (short)DAT_00036844;
  }
  else {
    puVar3 = PTR_LAB_00036914;
    if (((int)(uint)uVar2 <= (int)PTR_LAB_00036914) &&
       (puVar3 = (undefined *)(int)DAT_0003690e, (int)puVar3 <= (int)(uint)uVar2)) {
      *(ushort *)PTR_CAN201_SpeedCandidateWord_000367e8 = uVar2;
      return &DAT_0003687c;
    }
    puVar1 = &DAT_0003687c;
    *(short *)PTR_CAN201_SpeedCandidateWord_000367e8 = (short)puVar3;
  }
  return puVar1;
}

