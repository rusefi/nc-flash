/* Ghidra analysis output; verify against original SH instructions. */

/* Reset9462/8F00 exact1 clears8EFB..EFE and8EF8.Else zerocounters setlatches;8EFD/E exact1
   sets8EF8=1 and8EFF=0.2048 cases and320 retained cycles. See control-raw-enable.txt. */

char Control_UpdateFirstRawFallbackLatches(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  
  puVar1 = PTR_DAT_0006cfa4;
  cVar3 = (*(code *)PTR_FUN_0006cfac)(PTR_DAT_0006cfa8);
  puVar2 = PTR_DAT_0006cfb8;
  if ((cVar3 == '\x01') || (*PTR_DAT_0006cfb0 == '\x01')) {
    cVar3 = '\x01';
    *PTR_DAT_0006cfb4 = 0;
    *puVar2 = 0;
    *puVar1 = 0;
    *PTR_DAT_0006cfbc = 0;
    *PTR_DAT_0006cfc0 = 0;
  }
  else {
    if (*PTR_DAT_0006cfc4 == '\0') {
      *PTR_DAT_0006cfb4 = 1;
    }
    if (*PTR_DAT_0006cfc8 == '\0') {
      *PTR_DAT_0006cfb8 = 1;
    }
    if (*PTR_DAT_0006cfcc == '\0') {
      *puVar1 = 1;
    }
    if (*PTR_DAT_0006cfd0 == '\0') {
      *PTR_DAT_0006cfbc = 1;
    }
    puVar2 = PTR_DAT_0006cfd4;
    cVar3 = '\x01';
    if ((*puVar1 == '\x01') || (cVar3 = *PTR_DAT_0006cfbc, cVar3 == '\x01')) {
      *PTR_DAT_0006cfc0 = 1;
      *puVar2 = 0;
    }
  }
  return cVar3;
}

