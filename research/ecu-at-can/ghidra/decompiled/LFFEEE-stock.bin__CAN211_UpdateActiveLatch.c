/* Ghidra analysis output; verify against original SH instructions. */

/* Updates protected718C from7140-7258*7154 versus714C, inhibition and ramp/hold inputs.2048
   synthetic cases; not complete torque actuation. */

char CAN211_UpdateActiveLatch(void)

{
  undefined *puVar1;
  char cVar2;
  char cVar3;
  float fVar4;
  float fVar5;
  
  puVar1 = PTR_FUN_0003fe84;
  fVar4 = (float)(*(code *)PTR_FUN_0003fe84)(PTR_DAT_0003febc);
  fVar5 = (float)(*(code *)puVar1)(PTR_CAN211_ConversionFactor_0003fec0);
  fVar5 = *(float *)PTR_DAT_0003fec4 - fVar4 * fVar5;
  cVar3 = *PTR_DAT_0003fe7c;
  fVar4 = (float)(*(code *)puVar1)(PTR_CAN211_NumericBound_0003fe80);
  if (((fVar4 < fVar5) &&
      ((*PTR_DAT_0003fec8 != '\0' ||
       ((((cVar2 = (*(code *)PTR_FUN_0003fe48)(PTR_DAT_0003fecc), cVar2 == '\0' &&
          (*PTR_DAT_0003fe94 == '\0')) && (cVar3 == '\0')) && (*PTR_DAT_0003fed0 == '\0')))))) ||
     (*PTR_DAT_0003fe8c == '\x01')) {
    (*(code *)PTR_FUN_0003fed4)(PTR_DAT_0003fe90,1);
  }
  else if (((*PTR_DAT_0004008c == '\0') && (*PTR_DAT_00040090 == '\0')) ||
          (*PTR_DAT_00040094 == '\x01')) {
    (*(code *)PTR_FUN_0004009c)(PTR_DAT_00040098,0);
  }
  cVar2 = '\x01';
  if ((*PTR_DAT_000400a4 == '\x01') || (cVar2 = cVar3, cVar3 == '\x01')) {
    *PTR_DAT_000400a0 = 1;
    cVar3 = cVar2;
  }
  else {
    *PTR_DAT_000400a0 = 0;
  }
  return cVar3;
}

