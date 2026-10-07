/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00044f0c) */
/* WARNING: Removing unreachable block (ram,0x00044e6c) */
/* WARNING: Removing unreachable block (ram,0x00044e90) */
/* WARNING: Removing unreachable block (ram,0x00044f32) */
/* Upper0..4: alternate-axis curve plus signed616A indexed offset clamped0..32767
   into9B42;809C>=23040 replaces,elseminimum. Lower5..9: cachedupper
   minusbyte*64,signedwordfloorzero,minimum. Production slots0/1/2/5/6/7;
   tcu-optional-thresholds.txt. */

uint Selection_AdjustThresholdFromStoredOffset(int param_1,uint param_2,short param_3)

{
  uint uVar1;
  short sVar2;
  undefined4 *puVar3;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  short local_20;
  int local_1c;
  short local_18;
  
  local_1c = param_1 * 2;
  local_20 = param_3;
  local_18 = (*(code *)PTR_StoredWord_ReadSignedAdjustment_00044eec)
                       ((int)*(short *)(PTR_PTR_00044ee8 + local_1c));
  if (param_1 < 5) {
    uVar1 = (*(code *)PTR_Lookup_InterpolateWordCurve_00044ef4)
                      ((int)local_20,*(undefined4 *)(PTR_DAT_00044ef0 + param_1 * 4));
    uVar1 = (uVar1 & 0xffff) + (int)local_18;
    if ((int)DAT_00044ee4 < (int)uVar1) {
      uVar1 = (int)DAT_00044ee4;
    }
    local_24 = 0;
    local_28 = DAT_00044ef8;
    puVar3 = &local_28;
    sVar2 = (*(code *)PTR_FUN_00044f00)();
    if ((int)uVar1 < (int)sVar2) {
      local_2c = 0;
      local_30 = DAT_00044ef8;
      puVar3 = &local_30;
      sVar2 = (*(code *)PTR_FUN_00044f00)();
      uVar1 = (uint)sVar2;
    }
    *(short *)(*(int *)((int)puVar3 + 4) + (int)DAT_00044ee6) = (short)uVar1;
    if ((*(short *)PTR_DAT_00044f04 <= Comparison_ApplicationInput) ||
       ((uVar1 & 0xffff) < (param_2 & 0xffff))) {
      param_2 = uVar1;
    }
  }
  else {
    uVar1 = (int)*(short *)((param_1 + -5) * 2 + (int)DAT_00044ee6) +
            (uint)(byte)PTR_DAT_00044f08[param_1 + -5] * -0x40;
    local_24 = 0;
    local_28 = DAT_00044ef8;
    sVar2 = (*(code *)PTR_FUN_0004510c)();
    if ((short)uVar1 < sVar2) {
      local_2c = 0;
      local_30 = DAT_00045110;
      sVar2 = (*(code *)PTR_FUN_0004510c)();
      uVar1 = (uint)sVar2;
    }
    if ((uVar1 & 0xffff) < (param_2 & 0xffff)) {
      param_2 = uVar1;
    }
  }
  return param_2;
}

