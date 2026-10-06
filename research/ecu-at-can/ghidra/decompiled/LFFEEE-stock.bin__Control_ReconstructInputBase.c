/* Ghidra analysis output; verify against original SH instructions. */

/* Ifabs(RTZ(1-8054))>.00390625,protected804C=RTZ(RTZ(806C-RTZ(8054*8084))/RTZ(1-8054));elseholdentirerecord.
   Stockcoefficientproducer staysoutsidenearzero guard. */

uint Control_ReconstructInputBase(void)

{
  uint uVar1;
  float fVar2;
  
  fVar2 = 1.0 - *(float *)PTR_Control_InputHistoryCoefficient_00058b08;
  uVar1 = (*(code *)PTR_FUN_00058b3c)(fVar2,0,DAT_00058b38);
  if ((uVar1 & 0xff) != 0) {
    uVar1 = (*(code *)PTR_FUN_00058b4c)
                      ((*(float *)PTR_Control_InputTarget_00058b44 -
                       *(float *)PTR_Control_InputHistoryCoefficient_00058b08 *
                       *(float *)PTR_Control_PriorInputTargetSnapshot_00058b40) / fVar2,
                       PTR_Control_ProtectedInputBase_00058b48);
    return uVar1;
  }
  return uVar1;
}

