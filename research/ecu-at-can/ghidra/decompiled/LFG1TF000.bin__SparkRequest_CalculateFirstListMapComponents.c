/* Ghidra analysis output; verify against original SH instructions. */

/* Executed two-output producer. Mapaxis=(2*s16(80F6)+1900)low16,secondaxisrecord+16low16.6x6 maps
   andoptional offsetcurve each>>2. Code7/operation18 forcesbasezero;allstockoffsetcurveszero. See
   tcu-request-maps.txt. */

void SparkRequest_CalculateFirstListMapComponents(uint *param_1,uint *param_2,int param_3)

{
  char cVar1;
  short sVar3;
  uint uVar2;
  int *extraout_r3;
  undefined *puVar4;
  undefined *puVar5;
  uint **ppuVar6;
  undefined4 local_24;
  undefined4 local_20;
  uint *local_1c;
  int local_18;
  
  ppuVar6 = &local_1c;
  cVar1 = *(char *)(param_3 + 1);
  puVar4 = PTR_SparkRequest_FirstListMapTables_200__0004d5e8;
  puVar5 = PTR_SparkRequest_FirstListOffsetCurves_18__0004d5ec;
  if ((((cVar1 != '\t') &&
       (puVar4 = PTR_SparkRequest_FirstListMapTables_150__0004d5f0,
       puVar5 = PTR_SparkRequest_FirstListOffsetCurves_9__0004d5f4, cVar1 != '\b')) &&
      (cVar1 != '\v')) &&
     (puVar4 = PTR_SparkRequest_FirstListMapTables_350__0004d5f8,
     puVar5 = PTR_SparkRequest_FirstListOffsetCurves_36__0004d5fc, cVar1 != '\n')) {
    if (cVar1 == '\a') {
      puVar4 = PTR_SparkRequest_FirstListMapTables_100__0004d600;
      puVar5 = PTR_SparkRequest_FirstListOffsetCurves_27__0004d604;
      if ((*(byte *)(param_3 + 0x12) & 0x20) != 0) {
        puVar4 = PTR_SparkRequest_FirstListMapTables_300__0004d5e4;
      }
    }
    else {
      puVar4 = PTR_SparkRequest_FirstListMapTables_50__0004d608;
      puVar5 = PTR_SparkRequest_FirstListOffsetCurves_0004d60c;
      if (cVar1 != '\x06') {
        puVar4 = PTR_SparkRequest_FirstListMapTables_0004d6d4;
        puVar5 = (undefined *)0x0;
      }
    }
  }
  if (*(char *)(param_3 + 8) == '\x18') {
    puVar4 = PTR_SparkRequest_FirstListMapTables_250__0004d6d8;
  }
  if (*(char *)(param_3 + 8) == '\x17') {
    puVar4 = PTR_SparkRequest_FirstListMapTables_300__0004d5e4;
  }
  local_18 = DAT_ffff80f6 * 2 + (int)DAT_0004d6d0;
  local_1c = param_1;
  if ((*(char *)(param_3 + 8) == '\x18') && (*(char *)(param_3 + 1) == '\a')) {
    local_20 = 0;
    ppuVar6 = (uint **)&local_24;
    local_24 = DAT_0004d6dc;
    sVar3 = (*(code *)PTR_FUN_0004d6e0)();
    *extraout_r3 = (int)sVar3;
  }
  else {
    uVar2 = (*(code *)PTR_Lookup_ByteGrid2D_Q8_0004d6e4)
                      (local_18,(int)*(short *)(param_3 + 0x10),puVar4);
    *param_1 = (uVar2 & 0xffff) >> 2;
  }
  *(undefined4 *)((int)ppuVar6 + -4) = 0;
  *(undefined4 *)((int)ppuVar6 + -8) = DAT_0004d6dc;
  sVar3 = (*(code *)PTR_FUN_0004d6e0)();
  *param_2 = (int)sVar3;
  if ((puVar5 != (undefined *)0x0) && ((*(byte *)(param_3 + 0x12) & 0x40) != 0)) {
    if ((*(char *)(param_3 + 1) == '\a') || (*(char *)(param_3 + 1) == '\n')) {
      uVar2 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0004d6ec)
                        ((int)*(short *)PTR_TransitionProgress_AccumulatorC_0004d6e8,puVar5);
    }
    else {
      uVar2 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0004d6ec)
                        ((int)*(short *)(param_3 + 10),puVar5);
    }
    *param_2 = (uVar2 & 0xffff) >> 2;
  }
  return;
}

