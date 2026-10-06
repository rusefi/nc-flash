/* Ghidra analysis output; verify against original SH instructions. */

/* FourreplywordsstartingindexR5 toRAMBB70+2*u16R4. Application9001..9080 writes8bytes
   perheaderindex;all128indiceschecked. */

undefined * SCI1_CopyReplyCalibrationWords(uint param_1,ushort param_2)

{
  undefined *puVar1;
  int iVar2;
  undefined2 *puVar3;
  byte bVar4;
  
  puVar1 = PTR_SCI1_ApplicationReplyRecord_000229b4;
  bVar4 = 0;
  puVar3 = (undefined2 *)((param_1 & 0xffff) * 2 + (int)DAT_000229b2);
  iVar2 = (uint)param_2 << 1;
  do {
    bVar4 = bVar4 + 1;
    *puVar3 = *(undefined2 *)(puVar1 + iVar2);
    puVar3 = puVar3 + 1;
    iVar2 = iVar2 + 2;
  } while (bVar4 < 4);
  return puVar1;
}

