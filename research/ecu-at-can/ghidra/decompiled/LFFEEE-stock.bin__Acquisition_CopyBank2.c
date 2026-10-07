/* Ghidra analysis output; verify against original SH instructions. */

/* Positive4055 clears4053/54; recognized1/4/8 copies channels24 onward descending. Zero retains
   flags/data; otherpositive clearsflags only. Exhaustivecountbyte execution. */

char Acquisition_CopyBank2(void)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar4;
  undefined2 *puVar5;
  
  puVar3 = PTR_DAT_00005014;
  puVar2 = PTR_Acquisition_ADCResultBank_00005010;
  if (PTR_DAT_00005014[2] == '\0') {
    return '\0';
  }
  PTR_DAT_00005014[1] = 0;
  *puVar3 = 0;
  cVar1 = puVar3[2];
  if (cVar1 == '\b') {
    puVar5 = (undefined2 *)(int)sRam00004ffe;
    *(undefined2 *)(puVar2 + 0x3e) = *puVar5;
    *(undefined2 *)(puVar2 + 0x3c) = *(undefined2 *)(int)sRam00005000;
    *(undefined2 *)(puVar2 + 0x3a) = puVar5[-2];
    *(undefined2 *)(puVar2 + 0x38) = *(undefined2 *)(int)sRam00005002;
  }
  else if (cVar1 != '\x04') {
    cVar4 = '\x01';
    if (cVar1 != '\x01') {
      return cVar1;
    }
    goto LAB_00004fde;
  }
  puVar5 = (undefined2 *)(int)sRam00005004;
  *(undefined2 *)(puVar2 + 0x36) = *puVar5;
  *(undefined2 *)(puVar2 + 0x34) = *(undefined2 *)(int)sRam00005006;
  cVar4 = '2';
  *(undefined2 *)(puVar2 + 0x32) = puVar5[-2];
LAB_00004fde:
  *(undefined2 *)(puVar2 + 0x30) = *(undefined2 *)(int)sRam00005008;
  return cVar4;
}

