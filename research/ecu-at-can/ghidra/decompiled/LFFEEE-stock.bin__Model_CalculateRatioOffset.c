/* Ghidra analysis output; verify against original SH instructions. */

/* If abs6814>0.48828125:7200=(6828/6814)*curveA2230(67DC);elsehold.71E0=7200+C1428
   onlyif67AC==1.162 cases. */

char Model_CalculateRatioOffset(void)

{
  undefined *puVar1;
  char cVar2;
  float fVar3;
  float fVar4;
  
  fVar4 = *(float *)PTR_DAT_00040a2c;
  cVar2 = (*(code *)PTR_FUN_00040a34)(fVar4,0,DAT_00040a30);
  puVar1 = PTR_DAT_00040a38;
  if (cVar2 != '\0') {
    fVar3 = (float)(*(code *)PTR_Lookup_FloatCurve_00040a44)
                             (*(undefined4 *)PTR_DAT_00040a3c,DAT_00040a40);
    *(float *)PTR_DAT_00040a48 = fVar3;
    *(float *)puVar1 = (*(float *)PTR_DAT_00040a4c / fVar4) * fVar3;
  }
  cVar2 = (*(code *)PTR_FUN_00040a54)(PTR_DAT_00040a50);
  if (cVar2 == '\x01') {
    *(float *)PTR_Model_RatioOffset_00040a5c = *(float *)PTR_DAT_00040a58 + *(float *)puVar1;
  }
  else {
    *(undefined4 *)PTR_Model_RatioOffset_00040a5c = *(undefined4 *)puVar1;
  }
  return cVar2;
}

