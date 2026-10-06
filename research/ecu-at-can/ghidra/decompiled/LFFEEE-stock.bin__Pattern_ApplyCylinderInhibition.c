/* Ghidra analysis output; verify against original SH instructions. */

/* 6DFE==1,cylinder7493!=0,749A==1 sets749E+c mask40;always calls42EA8.120 CAN211-to-mask paths;
   final hardware unproved. */

void Pattern_ApplyCylinderInhibition(void)

{
  if (((*PTR_DAT_0004612c == '\x01') && (*DAT_00046128 != 0)) &&
     (*PTR_Pattern_CurrentEventInhibit_00046130 == '\x01')) {
    PTR_DAT_00046134[*DAT_00046128] = PTR_DAT_00046134[*DAT_00046128] | 0x40;
  }
  (*(code *)PTR_AggregateCylinderCutMask_00046138)();
  return;
}

