/* Ghidra analysis output; verify against original SH instructions. */

/* Executed stock eight6x6 grids with original software arithmetic. Byte axes/values
   scaled256,firstinterpolateX thenY,truncating signed increments; endpoint clamping.
   Knots/midpoints validated; no arbitrary-double claim. */

uint Lookup_ByteGrid2D_Q8(short param_1,ushort param_2,byte *param_3)

{
  byte bVar1;
  bool bVar2;
  ushort uVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  byte *pbVar7;
  uint uVar8;
  byte *pbVar9;
  int iVar10;
  uint unaff_r12;
  byte *pbVar11;
  int iVar12;
  int iVar13;
  undefined1 *local_6c [3];
  undefined1 *local_60;
  undefined1 *local_5c [3];
  undefined1 *local_50;
  undefined1 auStack_4c [24];
  byte *local_34;
  int iStack_30;
  ushort uStack_2c;
  byte *pbStack_28;
  int iStack_24;
  
  bVar1 = *param_3;
  iVar12 = (int)(char)bVar1;
  pbVar9 = param_3 + 2;
  pbVar11 = param_3 + bVar1 + 2;
  uVar8 = (uint)param_3[1];
  param_3 = param_3 + bVar1 + 3;
  iVar10 = bVar1 + 1;
  local_34 = param_3 + (uVar8 - 1) * iVar10;
  pbVar7 = param_3;
  uStack_2c = param_2;
  iStack_30._0_2_ = param_1;
  if ((param_2 < (ushort)((ushort)*pbVar11 << 8)) ||
     (pbVar7 = local_34, (ushort)((ushort)pbVar11[(uVar8 - 1) * iVar10] << 8) <= param_2)) {
    uVar8 = Lookup_InterpolateByteCurve((int)param_1,iVar12,pbVar9,pbVar7);
  }
  else {
    iVar4 = 1;
    bVar2 = false;
    while ((iVar4 < (int)uVar8 && (!bVar2))) {
      iVar13 = iVar10 * iVar4;
      unaff_r12 = (uint)pbVar11[iVar13];
      iVar4 = iVar4 + 1;
      if (param_2 < (ushort)((ushort)pbVar11[iVar13] << 8)) {
        bVar2 = true;
      }
    }
    iStack_24 = iVar4 + -2;
    local_34 = param_3 + iVar10 * iStack_24;
    pbStack_28 = param_3 + iVar10 * (iVar4 + -1);
    uVar3 = Lookup_InterpolateByteCurve((int)param_1,iVar12,pbVar9,local_34);
    local_34._0_2_ = uVar3;
    uVar8 = Lookup_InterpolateByteCurve((int)iStack_30._0_2_,iVar12,pbVar9,pbStack_28);
    uVar5 = (uint)pbVar11[iStack_24 * iVar10];
    if (uVar5 != (unaff_r12 & 0xffff)) {
      uVar6 = (uint)local_34._0_2_;
      iStack_30 = (uint)uStack_2c + uVar5 * -0x100;
      local_50 = (undefined1 *)&local_50;
      (*(code *)PTR_FUN_000109b0)
                (uVar5,((unaff_r12 & 0xffff) - uVar5) * 0x100,uVar6,(uVar8 & 0xffff) - uVar6);
      local_5c[0] = (undefined1 *)local_5c;
      (*(code *)PTR_FUN_000109b4)();
      local_60 = auStack_4c;
      (*(code *)PTR_FUN_000109b8)();
      local_6c[0] = (undefined1 *)local_6c;
      (*(code *)PTR_FUN_000109b4)();
      (*(code *)PTR_FUN_000109bc)();
      iVar10 = (*(code *)PTR_FUN_000109c0)();
      uVar8 = iVar10 + uVar6;
    }
  }
  return uVar8;
}

