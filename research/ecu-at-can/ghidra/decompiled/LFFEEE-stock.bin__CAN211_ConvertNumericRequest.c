/* Ghidra analysis output; verify against original SH instructions. */

/* Near-zero7154 selects711C. Otherwise715C=max(714C,7148)/(6A28==1?1:7154)+71C4.94 cases execute;2
   inexact cases correctly rejected. See can211-spark.txt. */

void CAN211_ConvertNumericRequest(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  float fVar4;
  undefined4 uVar5;
  float fVar6;
  
  puVar1 = PTR_FUN_0003fbc0;
  fVar4 = (float)(*(code *)PTR_FUN_0003fbc0)(PTR_CAN211_ConversionFactor_0003fbc4);
  cVar3 = (*(code *)PTR_FUN_0003fbcc)(fVar4,0,DAT_0003fbc8);
  puVar2 = PTR_DAT_0003fbd0;
  if (cVar3 == '\0') {
    uVar5 = (*(code *)puVar1)(PTR_DAT_0003fbd4);
    *(undefined4 *)puVar2 = uVar5;
  }
  else {
    uVar5 = (*(code *)puVar1)(PTR_CAN211_NumericBound_0003fbd8);
    fVar6 = (float)(*(code *)PTR_FUN_0003fbe0)(uVar5,*(undefined4 *)PTR_DAT_0003fbdc);
    cVar3 = (*(code *)PTR_FUN_0003fbe8)(PTR_CAN211_ConversionBypass_0003fbe4);
    if (cVar3 != '\x01') {
      fVar6 = fVar6 / fVar4;
    }
    fVar4 = (float)(*(code *)puVar1)(DAT_0003fbec);
    *(float *)puVar2 = fVar6 + fVar4;
  }
  return;
}

