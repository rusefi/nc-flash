/* Ghidra analysis output; verify against original SH instructions. */

/* 64originalSH7058-samplecases:return0 forSDSRhighbyte0B. SavesSYSCR2,clearsH-UDI-stop
   bit2,readswordF7C2,restoresSYSCR2. NoapplicationRAMwrites;CMPleavesT1.
   Otherclassbranchesstaticonly;notphysicalchipidentity. */

int Runtime_ClassifyHudiStatus(void)

{
  char cVar1;
  char cVar2;
  int iVar3;
  
  cVar1 = *(char *)(int)DAT_0000f590;
  (*(code *)PTR_Hardware_WriteSystemControl2_0000f598)((int)DAT_0000f592 & (int)cVar1);
  cVar2 = (char)((ushort)*(undefined2 *)(int)DAT_0000f594 >> 8);
  (*(code *)PTR_Hardware_WriteSystemControl2_0000f598)((int)cVar1);
  if ((cVar2 == '\v') || (cVar2 == '\r')) {
    iVar3 = 0;
  }
  else if (cVar2 == 'P') {
    iVar3 = 1;
  }
  else if ((cVar2 == '\x0e') || (cVar2 == '\x0f')) {
    iVar3 = 2;
  }
  else {
    iVar3 = (int)DAT_0000f596;
  }
  return iVar3;
}

