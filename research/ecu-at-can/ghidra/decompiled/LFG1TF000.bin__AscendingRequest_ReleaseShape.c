/* Ghidra analysis output; verify against original SH instructions. */

/* Two-way calibration selector record+12>=773F0[code]. Breakpoint768FF+2*code+side stock0;
   slope76909+2*code+side stock64.1792 code/selector cases; stock progress<breakpoint branch
   unreachable. */

undefined * AscendingRequest_ReleaseShape(ushort *param_1,ushort *param_2,int param_3)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  
  puVar7 = PTR_AscendingRequest_ReleaseSlopes_0004e688;
  puVar6 = PTR_AscendingRequest_ReleaseSlopes_2__0004e67c;
  puVar5 = PTR_AscendingRequest_ReleaseSlopes_4__0004e670;
  puVar4 = PTR_AscendingRequest_ReleaseSlopes_6__0004e664;
  puVar8 = PTR_AscendingRequest_ReleaseSlopes_8__0004e658;
  bVar2 = *(byte *)(param_3 + 0xc);
  cVar3 = *(char *)(param_3 + 1);
  if (cVar3 == '\x04') {
    bVar1 = *PTR_AscendingRequest_ReleaseShapeSelectors_4__0004e650;
    *param_1 = (ushort)(byte)PTR_AscendingRequest_ReleaseBreakpoints_8__0004e654[bVar1 <= bVar2];
    *param_2 = (ushort)(byte)puVar8[bVar1 <= bVar2];
  }
  else if (cVar3 == '\x03') {
    bVar1 = *PTR_AscendingRequest_ReleaseShapeSelectors_3__0004e65c;
    *param_1 = (ushort)(byte)PTR_AscendingRequest_ReleaseBreakpoints_6__0004e660[bVar1 <= bVar2];
    *param_2 = (ushort)(byte)puVar4[bVar1 <= bVar2];
    puVar8 = puVar4;
  }
  else if (cVar3 == '\x02') {
    bVar1 = *PTR_AscendingRequest_ReleaseShapeSelectors_2__0004e668;
    *param_1 = (ushort)(byte)PTR_AscendingRequest_ReleaseBreakpoints_4__0004e66c[bVar1 <= bVar2];
    *param_2 = (ushort)(byte)puVar5[bVar1 <= bVar2];
    puVar8 = puVar5;
  }
  else if (cVar3 == '\x01') {
    bVar1 = *PTR_AscendingRequest_ReleaseShapeSelectors_1__0004e674;
    *param_1 = (ushort)(byte)PTR_AscendingRequest_ReleaseBreakpoints_2__0004e678[bVar1 <= bVar2];
    *param_2 = (ushort)(byte)puVar6[bVar1 <= bVar2];
    puVar8 = puVar6;
  }
  else {
    bVar1 = *PTR_AscendingRequest_ReleaseShapeSelectors_0004e680;
    *param_1 = (ushort)(byte)PTR_AscendingRequest_ReleaseBreakpoints_0004e684[bVar1 <= bVar2];
    *param_2 = (ushort)(byte)puVar7[bVar1 <= bVar2];
    puVar8 = puVar7;
  }
  return puVar8;
}

