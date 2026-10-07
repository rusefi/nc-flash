/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0003ae58) */
/* WARNING: Removing unreachable block (ram,0x0003ad1c) */
/* WARNING: Removing unreachable block (ram,0x0003ada4) */
/* WARNING: Removing unreachable block (ram,0x0003ae7c) */
/* Independent numeric model of both branches; signed16 divisor in ratio, curves/grids,
   constant-double conversions yield0. Complete application/selection/output chain;
   tcu-base-publication.txt. Rawunits/cadence open. */

int ClassApplication_BaseProducer(void)

{
  undefined *puVar1;
  int iVar2;
  char cVar8;
  uint uVar3;
  uint uVar4;
  short sVar5;
  short sVar6;
  short sVar7;
  undefined4 in_r7;
  int iVar9;
  short sVar10;
  undefined4 uVar11;
  short local_34 [2];
  undefined4 uStack_30;
  undefined2 local_2c [2];
  undefined1 local_28;
  
  iVar2 = (int)Phase_MeasuredSourceSample;
  cVar8 = (*(code *)PTR_FUN_0003ad64)();
  sVar5 = *(short *)PTR_DAT_0003ad68;
  local_34[0] = 0;
  local_2c[0] = 0;
  uStack_30._0_1_ = cVar8;
  (*(code *)PTR_ClassBase_CopyRawAxes_0003ad6c)(local_34,local_2c);
  puVar1 = PTR_Lookup_ByteGrid2D_Q8_0003ad70;
  if (uStack_30._0_1_ == '\x01') {
    local_28 = (*(code *)PTR_Phase_HasPendingWork_0003ad74)();
    iVar9 = (int)*(short *)PTR_DAT_0003ad78;
    if (*(short *)PTR_DAT_0003ad7c <= iVar9) {
      iVar9 = *(short *)PTR_DAT_0003ad7c + -1;
    }
    (*(code *)PTR_FixedPoint_DivideToSignedWord_0003ad80)
              ((sVar5 - iVar9) * 0x100,*(short *)PTR_DAT_0003ad7c - iVar9);
    uVar3 = (*(code *)puVar1)((int)local_34[0],iVar2,PTR_DAT_0003ad84);
    uVar4 = (*(code *)puVar1)((int)local_34[0],iVar2,PTR_DAT_0003ad88);
    uStack_30 = (*(code *)PTR_FUN_0003ad8c)((uVar4 & 0xffff) >> 2);
    iVar9 = 0;
    uVar11 = DAT_0003ad90;
    sVar5 = (*(code *)PTR_FUN_0003ad98)();
    uVar4 = (uint)sVar5;
    if (uStack_30._0_1_ != '\0') {
      uVar4 = (*(code *)puVar1)(iVar2,(int)DAT_ffff80fe << 1,PTR_DAT_0003ad9c,in_r7,uVar11);
      uVar4 = (uVar4 & 0xffff) >> 2;
    }
    iVar2 = (((uVar3 & 0xffff) >> 2) - iVar9) - uVar4;
  }
  else {
    iVar9 = *(int *)PTR_DAT_0003ada0;
    uVar11 = DAT_0003ad90;
    sVar6 = (*(code *)PTR_FUN_0003aea8)();
    if (iVar9 < sVar6) {
      sVar6 = *(short *)PTR_DAT_0003aeb0;
    }
    else {
      sVar6 = *(short *)PTR_DAT_0003aeac;
    }
    sVar7 = (*(code *)PTR_ClassBase_ReadShiftedWord_0003aeb4)();
    sVar10 = 1;
    if (((*PTR_DAT_0003aeb8 & 4) != 0) || (sVar7 < (short)(ushort)(byte)*PTR_DAT_0003aebc)) {
      sVar10 = 0;
    }
    uVar3 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0003aec4)
                      (iVar2,PTR_DAT_0003aec0 + sVar10 * 0xd);
    uVar3 = (uVar3 & 0xffff) >> 2;
    iVar9 = (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_0003aecc)
                      ((int)(short)(*(short *)PTR_DAT_0003aec8 + sVar5) * (int)sVar6,0x14,0x10,in_r7
                       ,uVar3,uVar11,uVar3);
    iVar9 = iVar9 + uVar3;
    uVar3 = (uint)*(short *)PTR_DAT_0003aed0;
    if ((*PTR_DAT_0003aeb8 & 8) != 0) {
      uVar3 = (*(code *)puVar1)(iVar2,(int)local_34[0],PTR_DAT_0003aed4);
      uVar3 = (uVar3 & 0xffff) >> 2;
    }
    iVar2 = (*(code *)PTR_ClassBase_ConstantZero_0003aed8)(iVar2);
    iVar2 = iVar2 + uVar3 + iVar9;
    sVar5 = (*(code *)PTR_FUN_0003aea8)();
    if (iVar2 < sVar5) {
      sVar5 = (*(code *)PTR_FUN_0003aea8)();
      iVar2 = (int)sVar5;
    }
  }
  return iVar2;
}

