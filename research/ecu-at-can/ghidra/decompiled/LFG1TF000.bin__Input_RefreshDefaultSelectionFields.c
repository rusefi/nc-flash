/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00021a2a) */
/* Unconditionally clears92D5mask10/20; setsbits0/1/2 fromA57C/D/E!=0 andbit6 fromA598bit0,
   preserves88.512 complete21734 cases.9304/6/8 defaultzero. */

undefined4 Input_RefreshDefaultSelectionFields(void)

{
  undefined *puVar1;
  undefined2 uVar3;
  byte bVar4;
  undefined4 uVar2;
  
  uVar3 = (*(code *)PTR_FUN_00021a7c)();
  *(undefined2 *)PTR_DAT_00021ab0 = uVar3;
  uVar3 = (*(code *)PTR_FUN_00021a7c)();
  *(undefined2 *)PTR_DAT_00021ab4 = uVar3;
  uVar3 = (*(code *)PTR_FUN_00021bd4)();
  *(undefined2 *)PTR_DAT_00021bd8 = uVar3;
  puVar1 = PTR_DAT_00021bdc;
  if (*PTR_DAT_00021be0 == '\0') {
    bVar4 = PTR_DAT_00021bdc[1] & 0xfe;
  }
  else {
    bVar4 = PTR_DAT_00021bdc[1] | 1;
  }
  PTR_DAT_00021bdc[1] = bVar4;
  if (*PTR_DAT_00021be4 == '\0') {
    bVar4 = puVar1[1] & 0xfd;
  }
  else {
    bVar4 = puVar1[1] | 2;
  }
  puVar1[1] = bVar4;
  if (*PTR_DAT_00021be8 == '\0') {
    bVar4 = puVar1[1] & 0xfb;
  }
  else {
    bVar4 = puVar1[1] | 4;
  }
  puVar1[1] = bVar4;
  puVar1[1] = puVar1[1] & 0xef;
  puVar1[1] = puVar1[1] & 0xdf;
  uVar2 = (*(code *)PTR_FUN_00021bf0)();
  return uVar2;
}

