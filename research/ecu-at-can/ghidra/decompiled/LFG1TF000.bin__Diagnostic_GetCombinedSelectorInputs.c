/* Ghidra analysis output; verify against original SH instructions. */

/* Writes bit4 from88B4==1 or88B6==1. Table5E980 associates identifier1704; service/physical
   semantics unverified. */

int Diagnostic_GetCombinedSelectorInputs(int param_1,undefined1 *param_2)

{
  undefined1 uVar1;
  
  uVar1 = 0;
  if ((*pcRam000555d0 == '\x01') || (*pcRam000555d4 == '\x01')) {
    uVar1 = 0x10;
  }
  *param_2 = uVar1;
  return (int)*(char *)(param_1 + 3);
}

