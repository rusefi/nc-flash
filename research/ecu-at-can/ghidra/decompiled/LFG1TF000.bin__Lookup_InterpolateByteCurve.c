/* Ghidra analysis output; verify against original SH instructions. */

/* Original software arithmetic verified for all65536 inputs of703C0. Descending segment truncates
   signed delta before adding origin;5000 ->8554. */

int Lookup_InterpolateByteCurve(ushort param_1,byte param_2,byte *param_3,byte *param_4)

{
  ushort uVar1;
  bool bVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  byte bVar7;
  int iVar6;
  int iVar8;
  int *piVar9;
  uint *puVar10;
  uint local_2c;
  short sStack_28;
  uint uStack_24;
  short sStack_20;
  
  local_2c = (uint)param_1;
  puVar10 = &local_2c;
  sStack_28 = (ushort)*param_3 << 8;
  uStack_24 = (uint)param_2;
  sStack_20 = (ushort)param_3[uStack_24 - 1] << 8;
  if (local_2c < (uint)*param_3 << 8) {
    bVar7 = *param_4;
  }
  else {
    if (local_2c < (uint)param_3[uStack_24 - 1] << 8) {
      iVar8 = 1;
      bVar2 = false;
      iVar6 = 0;
      while( true ) {
        if ((int)(uint)param_2 <= iVar8) {
          return iVar6;
        }
        if (bVar2) break;
        bVar7 = (param_3 + iVar8)[-1];
        iVar5 = (uint)param_3[iVar8] << 8;
        *(ushort *)(puVar10 + 1) = (ushort)(param_4 + iVar8)[-1] << 8;
        iVar3 = (uint)param_4[iVar8] << 8;
        if (((uint)bVar7 << 8 != iVar5) && (iVar3 = iVar6, (int)*puVar10 < iVar5)) {
          uVar1 = *(ushort *)(puVar10 + 1);
          puVar10[-7] = (uint)(puVar10 + -7);
          (*(code *)PTR_FUN_00010bec)();
          puVar10[-10] = (uint)(puVar10 + -10);
          (*(code *)PTR_FUN_00010bf0)();
          puVar10[-0xb] = (uint)(puVar10 + -6);
          (*(code *)PTR_FUN_00010bf4)();
          puVar10[-0xe] = (uint)(puVar10 + -0xe);
          (*(code *)PTR_FUN_00010bf0)();
          piVar4 = (int *)(puVar10 + -10);
          piVar9 = (int *)(puVar10 + -0xf);
          puVar10 = puVar10 + -0xf;
          *piVar9 = (int)piVar4;
          (*(code *)PTR_FUN_00010bf8)();
          iVar3 = (*(code *)PTR_FUN_00010bfc)();
          iVar3 = iVar3 + (uint)uVar1;
          bVar2 = true;
        }
        iVar8 = iVar8 + 1;
        iVar6 = iVar3;
      }
      return iVar6;
    }
    bVar7 = param_4[uStack_24 - 1];
  }
  return (uint)bVar7 << 8;
}

