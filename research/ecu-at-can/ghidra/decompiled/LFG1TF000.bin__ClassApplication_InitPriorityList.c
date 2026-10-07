/* Ghidra analysis output; verify against original SH instructions. */

/* DescriptorAE18 stock0304FFFF:3heads,4entries,sentinelFFFF. Original30454 initializes98B4
   andselected98D4;98B2=FFFF. Tests use real init andallocation. */

void ClassApplication_InitPriorityList(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  code *pcVar4;
  
  pcVar4 = DAT_00039c40;
  puVar3 = PTR_ClassApplication_PriorityList_00039c3c;
  puVar2 = PTR_DAT_00039c38;
  puVar1 = PTR_DAT_00039c34;
  *(undefined2 *)(int)DAT_00039c14 = 0xffff;
  (*pcVar4)(puVar3,puVar2,puVar1);
  return;
}

