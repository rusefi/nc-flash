/* Ghidra analysis output; verify against original SH instructions. */

/* Clears30 five-byte records at FFFF8818. */

undefined4 Input_InitializeFilterRecords(void)

{
  undefined *puVar1;
  undefined1 *puVar2;
  
  puVar2 = PTR_DAT_00017334 + DAT_00017332;
  puVar1 = PTR_DAT_00017334;
  do {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0;
    puVar1[3] = 0;
    puVar1[4] = 0;
    puVar1 = puVar1 + 5;
  } while (puVar1 < puVar2);
  return 0;
}

