/* Ghidra analysis output; verify against original SH instructions. */

/* 8080codes4/5/6; signed809C>=23040,80F2>=32000; class/flag exclusions.1550 cases including signed
   boundaries. */

undefined4 StoredAdjustment_AdmitLifecycle(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if (((((TransmissionStateClass == 6) || (TransmissionStateClass == 5)) ||
       (TransmissionStateClass == 4)) &&
      ((((*PTR_Selection_SourceCode_00049df4 != '\n' &&
         (*PTR_Selection_SourceCode_00049df4 != '\x11')) &&
        ((*(short *)PTR_DAT_00049df8 <= Comparison_ApplicationInput &&
         ((*(short *)PTR_DAT_00049dfc <= DAT_ffff80f2 &&
          ((*PTR_Request_CancellationFlags_00049e00 & 0x10) == 0)))))) &&
       ((*PTR_DAT_00049e04 & 1) == 0)))) &&
     ((((*PTR_DAT_00049e04 & 0x20) == 0 && ((*PTR_DAT_00049e08 & 0x10) == 0)) &&
      ((*PTR_DAT_00049e0c & 1) == 0)))) {
    uVar1 = 1;
  }
  return uVar1;
}

