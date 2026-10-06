/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004e26c) */
/* WARNING: Removing unreachable block (ram,0x0004e168) */
/* WARNING: Removing unreachable block (ram,0x0004e11e) */
/* WARNING: Removing unreachable block (ram,0x0004e22c) */
/* WARNING: Removing unreachable block (ram,0x0004e290) */
/* Stock release requires saturated targeterror>=51 and>=dynamic derivative bound.
   progress=clamp(256-div16(error*256,captured+10),0,256). Stock knee0; first admitted update
   captures+4 into+6/setsbit40, then scales captured request by remaining ratio. No9410/92D5 gate
   read; tcu-ascending-release.txt. */

void AscendingRequest_PublishReleaseCandidate(undefined4 param_1,int param_2)

{
  undefined *puVar1;
  short sVar3;
  undefined4 uVar2;
  byte bVar4;
  int iVar5;
  int iVar6;
  uint *puVar7;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  uint uStack_38;
  uint uStack_34;
  uint uStack_30;
  undefined4 auStack_2c [2];
  undefined2 uStack_24;
  
  sVar3 = AscendingRequest_TargetError((int)(char)PTR_DAT_0004e140[*(byte *)(param_2 + 1)]);
  iVar6 = (int)sVar3;
  auStack_2c[0] = 0;
  uStack_30 = DAT_0004e148;
  uStack_24 = (*(code *)PTR_FUN_0004e150)();
  uStack_34 = 0;
  uStack_38 = DAT_0004e148;
  puVar7 = &uStack_38;
  sVar3 = (*(code *)PTR_FUN_0004e254)();
  uStack_30 = (uint)sVar3;
  (*(code *)PTR_AscendingRequest_ReleaseBounds_0004e258)(auStack_2c,&uStack_30,param_2);
  if ((iVar6 < auStack_2c[0]._0_2_) || (iVar6 < (int)uStack_30)) {
    uStack_3c = 0;
    uStack_40 = DAT_0004e268;
    puVar7 = &uStack_40;
    sVar3 = (*(code *)PTR_FUN_0004e254)();
    iVar6 = (int)sVar3;
  }
  else {
    iVar5 = (int)DAT_0004e24c;
    sVar3 = (*(code *)PTR_FixedPoint_DivideToSignedWord_0004e25c)
                      (iVar6 << 8,(int)*(short *)(param_2 + 10));
    iVar6 = iVar5 - sVar3;
    if (iVar6 < 0) {
      iVar6 = 0;
    }
    if (iVar5 < iVar6) {
      iVar6 = iVar5;
    }
    uStack_38 = uStack_38 & 0xffff;
    uStack_34 = uStack_34 & 0xffff;
    (*(code *)PTR_AscendingRequest_ReleaseShape_0004e260)(&uStack_38,&uStack_34,param_2);
    puVar1 = PTR_Arithmetic_SaturatingMultiplyShift_0004e264;
    if (iVar6 < uStack_38._0_2_) {
      iVar6 = (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_0004e264)
                        ((int)uStack_34._0_2_,iVar6,6);
      iVar6 = (*(code *)puVar1)((int)*(short *)(param_2 + 6),iVar5 - iVar6,8);
      puVar7 = &uStack_38;
    }
    else {
      if ((*(byte *)(param_2 + 8) & 0x40) == 0) {
        *(undefined2 *)(param_2 + 6) = *(undefined2 *)(param_2 + 4);
        *(byte *)(param_2 + 8) = *(byte *)(param_2 + 8) | 0x40;
      }
      uVar2 = (*(code *)puVar1)((int)*(short *)(param_2 + 6),iVar5 - iVar6,0);
      sVar3 = (*(code *)PTR_FixedPoint_DivideToSignedWord_0004e25c)(uVar2,iVar5 - uStack_38._0_2_);
      iVar6 = (int)sVar3;
    }
  }
  *(undefined4 *)((int)puVar7 + -4) = 0;
  *(undefined4 *)((int)puVar7 + -8) = DAT_0004e268;
  sVar3 = (*(code *)PTR_FUN_0004e304)();
  if (sVar3 < iVar6) {
    bVar4 = *(byte *)(param_2 + 8) | 0x80;
  }
  else {
    *(undefined4 *)((int)puVar7 + -0xc) = 0;
    *(undefined4 *)((int)puVar7 + -0x10) = DAT_0004e308;
    sVar3 = (*(code *)PTR_FUN_0004e304)();
    iVar6 = (int)sVar3;
    bVar4 = *(byte *)(param_2 + 8) & 0x7f;
  }
  puVar1 = PTR_SparkRequest_SetFirstListEntry_0004e30c;
  *(byte *)(param_2 + 8) = bVar4;
  *(short *)(param_2 + 4) = (short)iVar6;
  (*(code *)puVar1)((int)*(char *)(param_2 + 2),iVar6,
                    -((((int)*(char *)(param_2 + 8) & 0x80U) == 0) - 1));
  return;
}

