/* Ghidra analysis output; verify against original SH instructions. */

/* Executed descriptorB028=010C7FFF from original startup copy;12 entries,modesA245..A252.
   Bookkeeping counter not explicitly reset here. */

undefined4 SparkRequest_InitializeFirstList(void)

{
  undefined4 uVar1;
  undefined1 *puVar2;
  undefined1 *puVar3;
  
  DAT_ffff80e2 = DAT_0004c700;
  uVar1 = (*(code *)PTR_RequestList_Initialize_0004c728)
                    (PTR_DAT_0004c724,PTR_SparkRequest_FirstListDescriptor_0004c720,PTR_DAT_0004c71c
                    );
  puVar3 = (undefined1 *)(int)DAT_0004c702;
  puVar2 = puVar3 + 0xe;
  do {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  } while (puVar3 < puVar2);
  return uVar1;
}

