/* Ghidra analysis output; verify against original SH instructions. */

/* Executed descriptorB02C=01037FFF from original startup copy;3 entries,modesA271..A275. Full
   physical policy entry unproved. */

undefined4 SparkRequest_InitializeSecondList(void)

{
  undefined4 uVar1;
  undefined1 *puVar2;
  undefined1 *puVar3;
  
  *(undefined2 *)PTR_DAT_0004cb6c = DAT_0004cb64;
  uVar1 = (*(code *)PTR_RequestList_Initialize_0004cb7c)
                    (PTR_DAT_0004cb78,PTR_SparkRequest_SecondListDescriptor_0004cb74,
                     PTR_DAT_0004cb70);
  puVar3 = (undefined1 *)(int)DAT_0004cb66;
  puVar2 = puVar3 + 5;
  do {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  } while (puVar3 < puVar2);
  return uVar1;
}

