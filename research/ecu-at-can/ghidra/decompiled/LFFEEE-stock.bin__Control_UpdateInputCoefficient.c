/* Ghidra analysis output; verify against original SH instructions. */

/* Stock8054 from8058 minusA35BC(6D28),scaled/clamped0..D9F14~.89844;gates7346/nonzero7016.
   7010exact1or7EEEnonzero halves. Fullbody405cases. */

char Control_UpdateInputCoefficient(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  char cVar4;
  undefined4 uVar5;
  float fVar6;
  
  uVar5 = (*(code *)PTR_FUN_00058af8)(PTR_Control_RawFirstAlternate_00058af4);
  uVar5 = (*(code *)PTR_Lookup_FloatCurve_00058b00)(uVar5,DAT_00058afc);
  *(undefined4 *)PTR_Control_InputCoefficientThreshold_00058b04 = uVar5;
  puVar2 = PTR_FUN_00058b0c;
  puVar1 = PTR_Control_InputHistoryCoefficient_00058b08;
  uVar5 = 0;
  cVar3 = (*(code *)PTR_FUN_00058b0c)(PTR_DAT_00058b10);
  if ((cVar3 != '\0') && (*PTR_DAT_00058b14 == '\0')) {
    cVar4 = (*(code *)puVar2)(PTR_DAT_00058b18);
    cVar3 = '\0';
    if (cVar4 != '\0') {
      if (*(float *)PTR_DAT_00058b1c == 0.0) {
        return cVar4;
      }
      fVar6 = (float)(*(code *)PTR_FUN_00058b28)
                               (((*(float *)PTR_Control_ScaledPositiveInputGap_00058b20 -
                                 *(float *)PTR_Control_InputCoefficientThreshold_00058b04) *
                                *(float *)PTR_DAT_00058b24) / *(float *)PTR_DAT_00058b1c,uVar5,
                                *(float *)PTR_DAT_00058b24);
      cVar4 = (*(code *)puVar2)(PTR_DAT_00058b2c);
      cVar3 = '\x01';
      if (cVar4 != '\x01') {
        cVar3 = (*(code *)puVar2)(PTR_DAT_00058b30);
        if (cVar3 == '\0') {
          *(float *)puVar1 = fVar6;
          return '\0';
        }
      }
      *(float *)puVar1 = *(float *)PTR_DAT_00058b34 * fVar6;
      return cVar3;
    }
  }
  *(undefined4 *)puVar1 = uVar5;
  return cVar3;
}

