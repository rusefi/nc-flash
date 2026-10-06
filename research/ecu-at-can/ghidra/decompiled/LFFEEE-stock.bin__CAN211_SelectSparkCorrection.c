/* Ghidra analysis output; verify against original SH instructions. */

/* With718C!=0 and6590!=0,7D2C=max(7A84-7174,0), additionally capped at7D38 unless7D35==1;
   otherwise0.48 gate cases and20 complete wire-to-spark examples. */

uint CAN211_SelectSparkCorrection(void)

{
  undefined *puVar1;
  uint uVar2;
  undefined4 extraout_fr0;
  undefined4 extraout_fr0_00;
  undefined4 uVar3;
  
  puVar1 = PTR_CAN211_SparkCorrection_000535f0;
  uVar3 = 0;
  uVar2 = (*(code *)PTR_FUN_000535f8)(PTR_DAT_000535f4);
  uVar2 = uVar2 & 0xff;
  if ((uVar2 == 0) || (*PTR_DAT_000535fc == '\0')) {
    *(undefined4 *)puVar1 = uVar3;
  }
  else {
    if (*PTR_DAT_00053608 == '\x01') {
      uVar2 = (*(code *)PTR_FUN_0005360c)
                        (*(float *)PTR_DAT_00053604 -
                         *(float *)PTR_CAN211_InvertedModelValue_00053600,uVar3);
      uVar3 = extraout_fr0;
    }
    else {
      uVar2 = (*(code *)PTR_FUN_00053614)
                        (*(float *)PTR_DAT_00053604 -
                         *(float *)PTR_CAN211_InvertedModelValue_00053600,uVar3,
                         *(undefined4 *)PTR_DAT_00053610);
      uVar3 = extraout_fr0_00;
    }
    *(undefined4 *)puVar1 = uVar3;
  }
  return uVar2;
}

