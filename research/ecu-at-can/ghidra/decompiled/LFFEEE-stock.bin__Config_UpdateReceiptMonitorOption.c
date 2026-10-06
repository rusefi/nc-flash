/* Ghidra analysis output; verify against original SH instructions. */

/* Stock E0D1C00 callsA1638 selector67 length1. Return0 sets9710 iff byte41 and91DC/91E0 zero;
   failure retains prior. Full execution stops at peripheralFFFFF74E; runtime value/physical name
   unproven. */

void Config_UpdateReceiptMonitorOption(void)

{
  undefined *puVar1;
  char cVar2;
  char local_c [8];
  
  puVar1 = PTR_DAT_0008f394;
  if ((byte)*PTR_DAT_0008f398 == DAT_0008f390) {
    if ((byte)*PTR_DAT_0008f39c == DAT_0008f390) {
      *PTR_DAT_0008f394 = 1;
    }
    else {
      *PTR_DAT_0008f394 = 0;
    }
  }
  else {
    cVar2 = (*(code *)PTR_FUN_0008f3a0)(0x67,local_c,1);
    if (cVar2 == '\0') {
      if (((local_c[0] == 'A') && (*PTR_DAT_0008f3a4 == '\0')) && (*PTR_DAT_0008f3a8 == '\0')) {
        *puVar1 = 1;
      }
      else {
        *puVar1 = 0;
      }
    }
  }
  return;
}

