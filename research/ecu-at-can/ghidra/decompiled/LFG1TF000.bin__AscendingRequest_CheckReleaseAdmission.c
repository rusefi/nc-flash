/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004df78) */
/* WARNING: Removing unreachable block (ram,0x0004df9a) */
/* Returns1 if s16(80EE)<s32(reference+first) OR< s32(reference+second), capturing saturated4E2D6
   error to+10. Otherwise0 and preserves+10. Equality tobothbounds rejects.324 direct cases plus
   signed-wrap/manager checks; not an outside-band test. */

undefined4 AscendingRequest_CheckReleaseAdmission(undefined4 param_1,int param_2)

{
  int iVar1;
  short sVar2;
  undefined2 uVar3;
  int iVar4;
  undefined4 uVar5;
  int iStack_34;
  int iStack_30;
  int iStack_2c;
  int iStack_28;
  int iStack_1c;
  
  uVar5 = 0;
  iVar1 = (int)Phase_MeasuredSourceSample;
  iVar4 = *(int *)(PTR_Phase_ProducedReferenceWords_0004e144 +
                  (uint)(byte)PTR_DAT_0004e140[*(byte *)(param_2 + 1)] * 4);
  iStack_28 = 0;
  iStack_2c = DAT_0004e148;
  iStack_1c = param_2;
  sVar2 = (*(code *)PTR_FUN_0004e150)();
  iStack_28 = (int)sVar2;
  iStack_30 = 0;
  iStack_34 = DAT_0004e148;
  sVar2 = (*(code *)PTR_FUN_0004e150)();
  iStack_34 = (int)sVar2;
  (*(code *)PTR_AscendingRequest_AdmissionBounds_0004e154)(&iStack_30,&iStack_34,iStack_2c);
  if ((iVar1 < iStack_30 + iVar4) || (iVar1 < iStack_34 + iVar4)) {
    uVar5 = 1;
    uVar3 = AscendingRequest_TargetError((int)(char)PTR_DAT_0004e140[*(byte *)(param_2 + 1)]);
    *(undefined2 *)(param_2 + 10) = uVar3;
  }
  return uVar5;
}

