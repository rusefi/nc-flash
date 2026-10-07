/* Ghidra analysis output; verify against original SH instructions. */

/* 80EA/80EE ->80C2/C6=min(u16(2*raw),A000), then314C4 ->80C4/C8.144 boundary pairs verified;
   captures809A/809C to80CC/CE. */

void Request_CaptureSourceAxes(undefined4 param_1)

{
  undefined *puVar1;
  int iVar2;
  int iVar3;
  char cVar4;
  undefined *puVar5;
  
  iVar2 = (int)DAT_ffff80ea;
  iVar3 = (int)Phase_MeasuredSourceSample;
  cVar4 = (*(code *)PTR_Phase_ClassifyDirection_000314d4)();
  puVar1 = PTR_DAT_000314d8;
  puVar5 = (undefined *)(iVar2 << 1);
  if ((int)PTR_DAT_000314d8 < (int)((uint)(iVar2 << 1) & 0xffff)) {
    puVar5 = PTR_DAT_000314d8;
  }
  Request_CapturedSourceAxisRaw = SUB42(puVar5,0);
  Request_CapturedSourceAxisScaled = Request_DoubleCapturedAxis(puVar5);
  puVar5 = (undefined *)(iVar3 << 1);
  if ((int)puVar1 < (int)((uint)(iVar3 << 1) & 0xffff)) {
    puVar5 = puVar1;
  }
  Request_CapturedMeasurementRaw = SUB42(puVar5,0);
  Request_CapturedMeasurementScaled = Request_DoubleCapturedAxis(puVar5);
  if (cVar4 == '\0') {
    FUN_00031400(param_1);
  }
  else {
    SparkRequest_ProduceParameterIndex(param_1);
  }
  FUN_000313d0();
  DAT_ffff80cc = Primary_ApplicationInput;
  DAT_ffff80ce = Comparison_ApplicationInput;
  DAT_ffff80d0 = *(undefined2 *)PTR_Comparison_HistoryChange_000314dc;
  DAT_ffff808e = *PTR_DAT_000314e0;
  DAT_ffff808f = *PTR_DAT_000314e4;
  DAT_ffff8090 = *PTR_DAT_000314e8;
  DAT_ffff8091 = *PTR_DAT_000314ec;
  DAT_ffff8092 = *PTR_DAT_000314f0;
  DAT_ffff8094 = *PTR_DAT_000314f4;
  DAT_ffff8095 = *PTR_DAT_000314f8;
  return;
}

