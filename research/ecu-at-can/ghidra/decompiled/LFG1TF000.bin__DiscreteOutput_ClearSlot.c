/* Ghidra analysis output; verify against original SH instructions. */

/* WritesFF toindexed910Dslot. Original1F3CE clearsdisabledstockslots4/6. See
   tcu-source-inhibit.txt. */

void DiscreteOutput_ClearSlot(undefined4 param_1)

{
  (*DAT_0001f480)((int)DAT_0001f476,param_1,(int)DAT_0001f474);
  return;
}

