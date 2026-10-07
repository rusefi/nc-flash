/* Ghidra analysis output; verify against original SH instructions. */

/* Indexu8:wordA5F8+2i first8000, payloadA600+2i, finaltag0107. Complete1F2AA executesindex1;
   physicaloutput/concurrency unproved. */

void OutputRecord_PublishWord(uint param_1,undefined2 param_2)

{
  undefined2 uVar1;
  int iVar2;
  undefined2 *puVar3;
  
  uVar1 = DAT_000530a8;
  iVar2 = (param_1 & 0xff) * 2;
  puVar3 = (undefined2 *)(PTR_DAT_000530c0 + iVar2);
  *puVar3 = (short)PTR_DAT_000530bc;
  *(undefined2 *)(PTR_DAT_000530c4 + iVar2) = param_2;
  *puVar3 = uVar1;
  return;
}

