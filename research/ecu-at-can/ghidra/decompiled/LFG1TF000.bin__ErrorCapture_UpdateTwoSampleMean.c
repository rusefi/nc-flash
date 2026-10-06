/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00030bce) */
/* State2: raw=30C20, output80D8=floor((s16 old95C0+s16 raw)/2), save raw95C0. Other states zero
   history/output via original arithmetic helper.280 filter/1020 reset cases and8 producer-driven
   request lifecycles. */

void ErrorCapture_UpdateTwoSampleMean(void)

{
  short sVar1;
  short *psVar2;
  
  psVar2 = (short *)(int)DAT_00030c10;
  if (*(char *)(int)DAT_00030c0a == '\x02') {
    sVar1 = ErrorCapture_ClippedDifference();
    Request_Code9HoldSource = (undefined2)((int)sVar1 + (int)*psVar2 >> 1);
    *psVar2 = sVar1;
  }
  else {
    sVar1 = (*(code *)PTR_FUN_00030c1c)();
    *psVar2 = sVar1;
    Request_Code9HoldSource = (*(code *)PTR_FUN_00030c1c)();
  }
  return;
}

