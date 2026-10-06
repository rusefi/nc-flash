/* Ghidra analysis output; verify against original SH instructions. */

/* Calls35C1C/35C38/35C9A. Full body executed. Each builder updates only while734A bit40 set; MT
   markerFF,discrete flags,wordFFFF. */

void CAN231_BuildMTFields(void)

{
  CAN231_SetMTMarker();
  CAN231_BuildMTDiscreteFlags();
  CAN231_SetMTWordMarker();
  return;
}

