/* Ghidra analysis output; verify against original SH instructions. */

/* Positive404F clears404D/E; recognized1/4/8/12 copies that many channels descending from bank0.
   Zero retains flags/data; otherpositive clearsflags only. Exhaustivecountbyte execution. */

uint Acquisition_CopyBank0(void)

{
  undefined1 *puVar1;
  undefined2 *puVar2;
  uint uVar3;
  uint uVar4;
  undefined2 *puVar5;
  
  puVar2 = puRam00004ee4;
  puVar1 = puRam00004ee0;
  if (puRam00004ee0[2] == '\0') {
    return 0;
  }
  puRam00004ee0[1] = 0;
  *puVar1 = 0;
  uVar3 = (uint)(byte)puVar1[2];
  if (uVar3 == 0xc) {
    puVar5 = (undefined2 *)(int)sRam00004eb4;
    puVar2[0xb] = *puVar5;
    puVar2[10] = *(undefined2 *)(int)sRam00004eb6;
    puVar2[9] = *(undefined2 *)(int)sRam00004eb8;
    puVar2[8] = puVar5[-3];
LAB_00004e7e:
    puVar5 = (undefined2 *)(int)sRam00004eba;
    puVar2[7] = *puVar5;
    puVar2[6] = *(undefined2 *)(int)sRam00004ebc;
    puVar2[5] = *(undefined2 *)(int)sRam00004ebe;
    puVar2[4] = puVar5[-3];
  }
  else {
    if (uVar3 == 8) goto LAB_00004e7e;
    if (uVar3 != 4) {
      uVar4 = 1;
      if (uVar3 != 1) {
        return uVar3;
      }
      goto LAB_00004ea8;
    }
  }
  puVar2[3] = *(undefined2 *)(int)sRam00004ec0;
  puVar2[2] = *(undefined2 *)(int)sRam00004ec2;
  uVar4 = (uint)*(short *)(int)sRam00004ec4;
  puVar2[1] = *(short *)(int)sRam00004ec4;
LAB_00004ea8:
  *puVar2 = *(undefined2 *)(int)sRam00004ec6;
  return uVar4;
}

