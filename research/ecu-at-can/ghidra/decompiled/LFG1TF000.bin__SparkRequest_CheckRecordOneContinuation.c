/* Ghidra analysis output; verify against original SH instructions. */

/* Requires8171<ROM76FF6=122; phase953F3 additionally requires953A>0. Fullcaller boundary cases;
   time units unproved. */

undefined4 SparkRequest_CheckRecordOneContinuation(void)

{
  short sVar1;
  undefined4 uVar2;
  
  uVar2 = 1;
  if ((byte)*PTR_DAT_0002c4cc < (byte)*PTR_DAT_0002c4d0) {
    if (*(char *)(int)DAT_0002c4c2 != '\x03') {
      return 1;
    }
    sVar1 = (*(code *)PTR_FUN_0002c4d8)();
    if (sVar1 < *(short *)(int)DAT_0002c4c4) {
      return uVar2;
    }
  }
  return 0;
}

