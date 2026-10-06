/* Ghidra analysis output; verify against original SH instructions. */

/* Reads indexedbyte from605C/626E banks withthreshold010D;signextendsresult.1536 roundtripcases
   verified. Usedby44CD0/48BC0 initialization. */

int StateCache_ReadByte(ushort param_1)

{
  int iVar1;
  uint uVar2;
  
  if ((int)(uint)param_1 < (int)DAT_000245be) {
    uVar2 = (uint)param_1;
    iVar1 = DAT_000245c8;
  }
  else {
    uVar2 = (int)DAT_000245c0 + (uint)param_1;
    iVar1 = DAT_000245cc;
  }
  return (int)*(char *)(uVar2 + iVar1);
}

