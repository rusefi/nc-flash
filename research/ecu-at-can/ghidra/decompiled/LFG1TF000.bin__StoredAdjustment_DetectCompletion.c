/* Ghidra analysis output; verify against original SH instructions. */

/* Queuephase exact1 after oldsignedphase<=0, or92D1bit0 rising vs9CA4bit0;
   storescurrentphase9C9A.144 cases. Completion doesnotguarantee49FE0 write. */

undefined4 StoredAdjustment_DetectCompletion(void)

{
  char cVar1;
  undefined4 uVar2;
  
  cVar1 = (*(code *)PTR_ApplicationPhase_ReadForCode_00049fd8)((int)*(short *)(int)DAT_00049fb4);
  uVar2 = 0;
  if (((cVar1 == '\x01') && (*(char *)(int)DAT_00049fbc < '\x01')) ||
     (((*PTR_DAT_00049fdc & 1) == 1 && ((*(byte *)(int)DAT_00049fbe & 1) == 0)))) {
    uVar2 = 1;
  }
  *(char *)(int)DAT_00049fbc = cVar1;
  return uVar2;
}

