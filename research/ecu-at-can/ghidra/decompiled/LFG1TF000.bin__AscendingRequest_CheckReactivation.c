/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004ddf2) */
/* WARNING: Removing unreachable block (ram,0x0004ddd0) */
/* WARNING: Removing unreachable block (ram,0x0004de48) */
/* Returns1 iff u8(8081)>=1,record+8bit20set,s16(80EE)>=s32(reference+firstbound),and s16(80F0)>=0.
   Computes but doesnot use secondbound.3888 direct cases pluswrap/retainedmanager checks. */

undefined4 AscendingRequest_CheckReactivation(undefined4 param_1,int param_2)

{
  short sVar1;
  short sVar2;
  undefined4 uVar3;
  int iStack_30;
  int iStack_2c;
  int iStack_28;
  int iStack_24;
  int iStack_18;
  undefined4 uStack_14;
  
  uStack_14 = *(undefined4 *)
               (PTR_Phase_ProducedReferenceWords_0004df1c +
               (uint)(byte)PTR_DAT_0004df18[*(byte *)(param_2 + 1)] * 4);
  iStack_24 = 0;
  iStack_28 = DAT_0004def4;
  iStack_18 = param_2;
  sVar1 = (*(code *)PTR_FUN_0004def8)();
  iStack_28 = (int)sVar1;
  iStack_2c = 0;
  iStack_30 = DAT_0004def4;
  sVar1 = (*(code *)PTR_FUN_0004def8)();
  iStack_2c = (int)sVar1;
  (*(code *)PTR_AscendingRequest_AdmissionBounds_0004df24)(&iStack_30,&iStack_2c,iStack_28);
  sVar1 = Measurement_DerivativeForRequest;
  uVar3 = 0;
  if ((((CAN231_SixStateSource != 0) && ((*(byte *)(param_2 + 8) & 0x20) != 0)) &&
      (iStack_30 + iStack_24 <= (int)Phase_MeasuredSourceSample)) &&
     (sVar2 = (*(code *)PTR_FUN_0004def8)(), sVar2 <= sVar1)) {
    uVar3 = 1;
  }
  return uVar3;
}

