/* Ghidra analysis output; verify against original SH instructions. */

/* Positive4052 clears4050/51; recognized1/4/8/12 copies channels12 onward descending. Zero retains
   flags/data; otherpositive clearsflags only. Exhaustivecountbyte execution. */

uint Acquisition_CopyBank1(void)

{
  short sVar1;
  undefined *puVar2;
  undefined *puVar3;
  uint uVar4;
  undefined2 *puVar5;
  
  puVar3 = PTR_Acquisition_ADCResultBank_00005010;
  puVar2 = PTR_DAT_0000500c;
  if (PTR_DAT_0000500c[2] == '\0') {
    return 0;
  }
  PTR_DAT_0000500c[1] = 0;
  *puVar2 = 0;
  uVar4 = (uint)(byte)puVar2[2];
  if (uVar4 == 0xc) {
    puVar5 = (undefined2 *)(int)sRam00004fea;
    *(undefined2 *)(puVar3 + 0x2e) = *puVar5;
    *(undefined2 *)(puVar3 + 0x2c) = *(undefined2 *)(int)sRam00004fec;
    *(undefined2 *)(puVar3 + 0x2a) = puVar5[-2];
    *(undefined2 *)(puVar3 + 0x28) = *(undefined2 *)(int)sRam00004fee;
LAB_00004f3c:
    puVar5 = (undefined2 *)(int)sRam00004ff0;
    *(undefined2 *)(puVar3 + 0x26) = *puVar5;
    *(undefined2 *)(puVar3 + 0x24) = *(undefined2 *)(int)sRam00004ff2;
    *(undefined2 *)(puVar3 + 0x22) = puVar5[-2];
    *(undefined2 *)(puVar3 + 0x20) = *(undefined2 *)(int)sRam00004ff4;
  }
  else {
    if (uVar4 == 8) goto LAB_00004f3c;
    if (uVar4 != 4) {
      if (uVar4 != 1) {
        return uVar4;
      }
      goto LAB_00004f6e;
    }
  }
  *(undefined2 *)(puVar3 + 0x1e) = *(undefined2 *)(int)sRam00004ff6;
  *(undefined2 *)(puVar3 + 0x1c) = *(undefined2 *)(int)sRam00004ff8;
  *(undefined2 *)(puVar3 + 0x1a) = *(undefined2 *)(int)sRam00004ffa;
LAB_00004f6e:
  sVar1 = *(short *)(int)sRam00004ffc;
  *(short *)(puVar3 + 0x18) = sVar1;
  return (int)sVar1;
}

