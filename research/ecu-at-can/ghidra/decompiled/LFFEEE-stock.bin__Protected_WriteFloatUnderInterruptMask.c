/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0001534c) */
/* Finite2310decay/init useoriginalwriter withduplicatedchecksumandinterruptmaskrestore.
   Nonfinitepathnotmodeled;control-history.txt. */

undefined4 Protected_WriteFloatUnderInterruptMask(undefined4 param_1,undefined4 *param_2)

{
  undefined *puVar1;
  ushort uVar2;
  undefined4 local_18;
  undefined4 local_14;
  
  local_14._2_2_ = (short)param_1;
  local_14._0_2_ = (short)((uint)param_1 >> 0x10);
  uVar2 = local_14._2_2_ + local_14._0_2_;
  local_14 = param_1;
  (*(code *)PTR_FUN_0001533c)(&local_18,(int)DAT_00015338);
  puVar1 = PTR_FUN_00015348;
  *(ushort *)(param_2 + 1) = ~uVar2;
  *param_2 = param_1;
  *(ushort *)((int)param_2 + 6) = ~uVar2;
  (*(code *)puVar1)(local_18);
  return 0;
}

