/* Ghidra analysis output; verify against original SH instructions. */

/* 1024originalmodeprefixes:4acceptedlowbyte0/1020rejects. Accepted
   savesSR/PR/callerSP12D8,loadsROMidleSPFFFF11A8/maskB0,sets12B8=100,tails3DD8.
   96localSTCSRcases/2rejects. control-scheduler-start.txt. */

undefined4 Scheduler_AdmitMode(byte param_1)

{
  undefined4 uVar1;
  uint in_sr;
  undefined1 auStack_8 [4];
  uint uStack_4;
  
  uStack_4 = in_sr & 0xfffffffe | (uint)((byte)*PTR_DAT_00003a70 <= param_1);
  if ((byte)*PTR_DAT_00003a70 <= param_1 != 0) {
    return 0;
  }
  *(undefined1 **)PTR_DAT_00003a80 = auStack_8;
  *(undefined4 *)(PTR_DAT_00003a84 + 8) = DAT_00003a64;
                    /* WARNING: Could not recover jumptable at 0x00003a60. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  uVar1 = (*(code *)PTR_Scheduler_InitializeStockMode_00003a74)();
  return uVar1;
}

