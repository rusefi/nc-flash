/* Ghidra analysis output; verify against original SH instructions. */

/* 7016zero copies80BCto8048;nonzeroandabs6DB4>.9765625 addsorderedcorrections*7020/6DB4
   to804C;otherwisehold8048. Mode2differsfromdownstreamexact1selector. */

undefined4 Control_UpdateCurrentInput(void)

{
  char cVar2;
  char cVar3;
  undefined4 uVar1;
  float fVar4;
  float extraout_fr0;
  
  fVar4 = (float)(*(code *)PTR_FUN_00058af8)(PTR_DAT_00058b50);
  cVar2 = (*(code *)PTR_FUN_00058b3c)(fVar4,0,DAT_00058b54);
  cVar3 = (*(code *)PTR_FUN_00058b0c)(PTR_DAT_00058b18);
  if (cVar3 == '\0') {
    *(undefined4 *)PTR_Control_CurrentRatioInput_00058b5c =
         *(undefined4 *)PTR_Control_BaselineInput_00058b58;
    uVar1 = 0;
  }
  else {
    uVar1 = 0;
    if (cVar2 != '\0') {
      uVar1 = (*(code *)PTR_FUN_00058af8)(PTR_Control_ProtectedInputBase_00058b48);
      *(float *)PTR_Control_CurrentRatioInput_00058b5c =
           extraout_fr0 +
           ((*(float *)PTR_Control_ActivationCorrection_00058b64 +
             *(float *)PTR_Control_MagnitudeActivationCorrection_00058b60 +
             *(float *)PTR_DAT_00058b68 + *(float *)PTR_DAT_00058b6c + *(float *)PTR_DAT_00058b70) *
           *(float *)PTR_DAT_00058b74) / fVar4;
    }
  }
  return uVar1;
}

