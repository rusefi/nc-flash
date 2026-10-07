/* Ghidra analysis output; verify against original SH instructions. */

/* Writes6940=(6943exact1 OR6944exact1 OR695Bbit3) AND raw7346exact1 AND DB0C0exact1. StockDB0C0=0
   forceszero;256directcases and36five-call slices pass. Doesnotproduce67E4. */

undefined1 TargetAdjustment_PublishActiveGate(void)

{
  char cVar1;
  undefined1 uVar2;
  
  if ((((*PTR_DAT_00031ecc == '\x01') || (*PTR_DAT_00031ed0 == '\x01')) ||
      ((*PTR_ControlMode_SelectedBit_00031ed4 & 8) != 0)) &&
     ((cVar1 = (*(code *)PTR_FUN_00031edc)(PTR_DAT_00031ed8), cVar1 == '\x01' &&
      (*PTR_DAT_00031ee0 == '\x01')))) {
    *PTR_TargetAdjustment_IncrementGate_00031ee4 = 1;
    uVar2 = 1;
  }
  else {
    uVar2 = 0;
    *PTR_TargetAdjustment_IncrementGate_00031ee4 = 0;
  }
  return uVar2;
}

