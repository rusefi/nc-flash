/* Ghidra analysis output; verify against original SH instructions. */

/* Executed neutral transition latch8EB6, exact float6D5C threshold8EB8/held8EB9, reset9462 and hold
   gate8EDC. Input units unresolved. */

undefined * LocalInputDiag_UpdateActivity(void)

{
  undefined *puVar1;
  char cVar3;
  char cVar4;
  undefined *puVar2;
  float extraout_fr0;
  
  cVar3 = (*(code *)PTR_FUN_0006c028)(PTR_DAT_0006c024);
  if (cVar3 == '\x01') {
    *PTR_DAT_0006c02c = 0;
  }
  else {
    cVar3 = *PTR_DAT_0006c030;
    cVar4 = (*(code *)PTR_FUN_0006c028)(PTR_DAT_0006c034);
    if (cVar3 != cVar4) {
      *PTR_DAT_0006c02c = 1;
    }
  }
  puVar2 = (undefined *)(*(code *)PTR_FUN_0006c03c)(PTR_DAT_0006c038);
  if (extraout_fr0 <= *(float *)PTR_DAT_0006c040) {
    *PTR_DAT_0006c044 = 0;
  }
  else {
    *PTR_DAT_0006c044 = 1;
    *PTR_DAT_0006c048 = 1;
  }
  puVar1 = PTR_DAT_0006c048;
  if (*PTR_DAT_0006c04c == '\0') {
    *PTR_DAT_0006c048 = 0;
    puVar2 = puVar1;
  }
  return puVar2;
}

