/* Ghidra analysis output; verify against original SH instructions. */

/* 6B34 /0.25 via20E8 capFFFE;6B4F or6DFB==1 sendsFFFF;70F0==1 sends0. Source3499..4000 and6B4F
   invalidation executed. */

uint CAN201_EncodeWord0(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_DAT_000367dc;
  if ((*PTR_DAT_0003683c == '\x01') || (*PTR_DAT_00036840 == '\x01')) {
    uVar2 = 1;
    *(short *)PTR_DAT_000367dc = (short)DAT_00036844;
  }
  else if (*PTR_DAT_00036848 == '\x01') {
    *(undefined2 *)PTR_DAT_000367dc = 0;
    uVar2 = 1;
  }
  else {
    uVar2 = (*(code *)PTR_FUN_0003684c)(*(undefined4 *)PTR_DAT_0003681c,DAT_00036820,0);
    if (DAT_00036850 < (int)(uVar2 & 0xffff)) {
      *(short *)puVar1 = (short)DAT_00036850;
    }
    else {
      *(short *)puVar1 = (short)uVar2;
    }
  }
  return uVar2;
}

