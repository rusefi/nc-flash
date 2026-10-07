/* Ghidra analysis output; verify against original SH instructions. */

/* 8wholeRAM fixtures:originalcode writeszeroFFFF4000 thenDMA0 fixedsource/incrementdest
   8168longwords throughFFFFBF9F;pollsTE thenclearsDE/TE. Mode1F0129,noIE. Withheldservice waits.
   ExplicitboundedDMAmodel,notphysicalreset/timing. SubsequentCA94/1619A/10events pass.
   control-initialize-dma.txt. */

void Runtime_ClearVolatileRamWithDma(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  int iVar4;
  uint *puVar5;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 auStack_1c [2];
  
  puVar1 = PTR_FUN_00010220;
  iVar4 = (int)DAT_00010208;
  (*(code *)PTR_FUN_00010220)(auStack_1c,iVar4);
  *(ushort *)(int)DAT_0001020a = *(ushort *)(int)DAT_0001020a & (ushort)PTR_DAT_00010224 | 1;
  puVar2 = PTR_FUN_00010228;
  (*(code *)PTR_FUN_00010228)(auStack_1c[0]);
  puVar3 = PTR_PTR_0001022c;
  **(undefined4 **)PTR_PTR_0001022c = 0;
  (*(code *)puVar1)(&local_20,iVar4);
  *(undefined4 *)(int)DAT_0001020c = *(undefined4 *)puVar3;
  *(undefined4 *)(int)DAT_0001020e = *(undefined4 *)puVar3;
  *(undefined2 *)(int)DAT_00010212 = DAT_00010210;
  puVar5 = (uint *)(int)DAT_00010214;
  *puVar5 = DAT_00010230;
  (*(code *)puVar2)(local_20);
  *(uint *)(int)DAT_00010216 = (*(int *)PTR_PTR_00010234 - *(int *)puVar3) + 1U >> 2 & DAT_00010238;
  (*(code *)puVar1)(&local_24,iVar4);
  *puVar5 = *puVar5 & 0xfffffff9 | 1;
  (*(code *)puVar2)(local_24);
  do {
  } while ((*puVar5 & 2) == 0);
  (*(code *)puVar1)(&local_28,iVar4);
  *puVar5 = *puVar5 & 0xfffffffc;
  (*(code *)puVar2)(local_28);
  return;
}

