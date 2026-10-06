/* Ghidra analysis output; verify against original SH instructions. */

/* Code0..4/default0:76805+50*bank map(80F8,record+18)>>2. If+8bit10clear andu16(+16)>=76738[bank],
   multiply by(76913+9*bank curve(8276<<8)>>8), then>>4.845 map/1925 scale cases. */

uint AscendingRequest_CalculateMapCandidate(int param_1)

{
  char cVar1;
  uint uVar2;
  uint uVar3;
  undefined *puVar4;
  ushort uVar5;
  undefined *puVar6;
  
  cVar1 = *(char *)(param_1 + 1);
  if (cVar1 == '\x04') {
    uVar5 = *(ushort *)(PTR_AscendingRequest_ScaleThresholds_0004e53c + 8);
    puVar4 = PTR_AscendingRequest_Maps_200__0004e540;
    puVar6 = PTR_AscendingRequest_ScaleCurves_36__0004e544;
  }
  else if (cVar1 == '\x03') {
    uVar5 = *(ushort *)(PTR_AscendingRequest_ScaleThresholds_0004e53c + 6);
    puVar4 = PTR_AscendingRequest_Maps_150__0004e548;
    puVar6 = PTR_AscendingRequest_ScaleCurves_27__0004e54c;
  }
  else if (cVar1 == '\x02') {
    uVar5 = *(ushort *)(PTR_AscendingRequest_ScaleThresholds_0004e53c + 4);
    puVar4 = PTR_AscendingRequest_Maps_100__0004e550;
    puVar6 = PTR_AscendingRequest_ScaleCurves_18__0004e554;
  }
  else if (cVar1 == '\x01') {
    uVar5 = *(ushort *)(PTR_AscendingRequest_ScaleThresholds_0004e53c + 2);
    puVar4 = PTR_AscendingRequest_Maps_50__0004e558;
    puVar6 = PTR_AscendingRequest_ScaleCurves_9__0004e55c;
  }
  else {
    uVar5 = *(ushort *)PTR_AscendingRequest_ScaleThresholds_0004e53c;
    puVar4 = PTR_AscendingRequest_Maps_0004e560;
    puVar6 = PTR_AscendingRequest_ScaleCurves_0004e564;
  }
  uVar2 = (*(code *)PTR_Lookup_ByteGrid2D_Q8_0004e568)
                    ((int)AscendingRequest_LiveMapAxis,(int)*(short *)(param_1 + 0x12),puVar4);
  uVar2 = (uVar2 & 0xffff) >> 2;
  if (((*(byte *)(param_1 + 8) & 0x10) == 0) && (uVar5 <= *(ushort *)(param_1 + 0x10))) {
    uVar3 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0004e538)((uint)*DAT_0004e56c << 8,puVar6);
    uVar2 = uVar2 * ((uVar3 & 0xffff) >> 8) >> 4;
  }
  return uVar2;
}

