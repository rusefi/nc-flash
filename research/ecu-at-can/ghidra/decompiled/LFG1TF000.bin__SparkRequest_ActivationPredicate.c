/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004cd78) */
/* WARNING: Removing unreachable block (ram,0x0004cd9a) */
/* Executed phase>=1 AND measured80EE >=ref-A OR >=ref-B AND >=ref-80F0*factor, withphase gate
   outside OR. Ref9218[5D446[code]], curves4D2D0/4D6F0. See tcu-request-dispatch.txt. See
   tcu-request-dispatch.txt. */

undefined4 SparkRequest_ActivationPredicate(undefined4 param_1,int param_2)

{
  byte bVar1;
  int iVar2;
  short sVar3;
  char cVar4;
  undefined4 uVar5;
  int iVar6;
  int iStack_40;
  int iStack_3c;
  int iStack_38;
  int iStack_34;
  int iStack_30;
  int iStack_28;
  int iStack_24;
  int iStack_20;
  
  iVar2 = (int)Phase_MeasuredSourceSample;
  uVar5 = 0;
  iStack_24 = param_2;
  sVar3 = (*(code *)PTR_SparkRequest_ActivationDerivativeFactor_0004cfa8)(param_2);
  iStack_20 = (int)Measurement_DerivativeForRequest * (int)sVar3;
  bVar1 = *(byte *)(iStack_24 + 1);
  iStack_28 = CONCAT13(bVar1,iStack_28._1_3_);
  iVar6 = *(int *)(PTR_Phase_ProducedReferenceWords_0004cfb0 +
                  (uint)(byte)PTR_DAT_0004cfac[bVar1] * 4);
  cVar4 = (*(code *)PTR_ApplicationPhase_ReadForCode_0004cfb4)(bVar1);
  iStack_28 = (int)cVar4;
  iStack_34 = 0;
  iStack_38 = DAT_0004cfb8;
  sVar3 = (*(code *)PTR_FUN_0004cfc0)();
  iStack_34 = (int)sVar3;
  iStack_3c = 0;
  iStack_40 = DAT_0004cfb8;
  sVar3 = (*(code *)PTR_FUN_0004cfc0)();
  iStack_40 = (int)sVar3;
  (*(code *)PTR_SparkRequest_ActivationOffsets_0004cfc4)(&iStack_3c,&iStack_40,param_2);
  if ((0 < iStack_38) &&
     ((iVar6 - iStack_3c <= iVar2 || ((iVar6 - iStack_40 <= iVar2 && (iVar6 - iStack_30 <= iVar2))))
     )) {
    uVar5 = 1;
  }
  return uVar5;
}

