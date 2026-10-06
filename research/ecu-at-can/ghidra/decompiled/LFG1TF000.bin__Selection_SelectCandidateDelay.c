/* Ghidra analysis output; verify against original SH instructions. */

/* Stock75310 four5-byte rows:37/37/37/0/0,zeros,18s,zeros. Risingrow selected9C79bit1/9410bit2;
   fallingrow3. Timeunitsunproved. */

undefined1 Selection_SelectCandidateDelay(uint param_1)

{
  int iVar1;
  undefined1 uVar2;
  
  uVar2 = *(undefined1 *)(int)DAT_00048ac4;
  if (*(char *)(int)DAT_00048ac6 == '\x01') {
    iVar1 = 0;
    if (((*(byte *)(int)DAT_00048ac8 & 2) == 0) &&
       (iVar1 = 1, (*PTR_Request_EnableFlags_00048ad4 & 4) != 0)) {
      iVar1 = 2;
    }
    if ((param_1 & 0xff) == 0) {
      param_1 = 0;
    }
    else {
      param_1 = (int)DAT_00048aca + param_1;
    }
    uVar2 = PTR_DAT_00048ad0[(param_1 & 0xff) + iVar1 * 5];
  }
  else if (*(char *)(int)DAT_00048ac6 == '\x02') {
    if ((param_1 & 0xff) == 5) {
      param_1 = 4;
    }
    uVar2 = PTR_DAT_00048ad0[(param_1 & 0xff) + 0xf];
  }
  return uVar2;
}

