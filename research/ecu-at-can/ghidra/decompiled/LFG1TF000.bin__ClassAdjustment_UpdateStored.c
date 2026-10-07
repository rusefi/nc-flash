/* Ghidra analysis output; verify against original SH instructions. */

/* 36DBC class0..2;98DCoutsideinclusive[-701,-527]
   chooses+/-1,clampsselectedslot+/-80,36E90spreads,39F94tailrelaxesinput.4513direct/96caller/100retained/45scheduled
   in tcu-class-adjustments.txt. CONDITIONAL: stock369A4 admission is impossible; see
   tcu-class-admission.txt. */

void ClassAdjustment_UpdateStored(void)

{
  undefined4 uVar1;
  short sVar2;
  int iVar3;
  char cVar4;
  
  uVar1 = ClassAdjustment_Classify();
  cVar4 = (char)uVar1;
  if (cVar4 != '\x7f') {
    iVar3 = 0;
    if ((int)*(short *)PTR_DAT_00036e54 + (int)*(short *)PTR_DAT_00036e58 <
        (int)*(short *)PTR_ClassAdjustment_UpdateInput_00036e50) {
      iVar3 = (int)*(short *)PTR_DAT_00036e5c;
    }
    if ((int)*(short *)PTR_ClassAdjustment_UpdateInput_00036e50 <
        (int)*(short *)PTR_DAT_00036e58 - (int)*(short *)PTR_DAT_00036e54) {
      iVar3 = -(int)*(short *)PTR_DAT_00036e5c;
    }
    if (iVar3 != 0) {
      sVar2 = (*(code *)PTR_StoredWord_ReadSignedAdjustment_00036e64)
                        ((int)*(short *)(PTR_DAT_00036e60 + cVar4 * 2));
      iVar3 = sVar2 + iVar3;
      if (*(short *)PTR_DAT_00036e68 < iVar3) {
        iVar3 = (int)*(short *)PTR_DAT_00036e68;
      }
      if (iVar3 < *(short *)PTR_DAT_00036e6c) {
        iVar3 = (int)*(short *)PTR_DAT_00036e6c;
      }
      (*(code *)PTR_StoredWord_WriteAdjustment_00036e70)
                ((int)*(short *)(PTR_DAT_00036e60 + cVar4 * 2),iVar3);
      ClassAdjustment_SpreadUnmarked(uVar1,iVar3);
                    /* WARNING: Could not recover jumptable at 0x00036dae. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (*(code *)PTR_ClassAdjustment_RelaxUpdateInput_00036e78)
                ((int)*(short *)PTR_DAT_00036e54,(int)*(short *)PTR_DAT_00036e58,
                 (int)*(short *)PTR_DAT_00036e74,(int)*(short *)PTR_DAT_00036e5c);
      return;
    }
  }
  return;
}

