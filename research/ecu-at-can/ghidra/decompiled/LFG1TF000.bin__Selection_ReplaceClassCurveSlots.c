/* Ghidra analysis output; verify against original SH instructions. */

/* For class1..5, i=class-1..4: upperpointer5DEAC and lowerpointer9C14+12*i; operation4/kind7.
   Class6 or signed<=0 leaves pointers. Scope0..6/inactive128/255; invalid positive classes not
   established safe. */

void Selection_ReplaceClassCurveSlots(char param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  
  puVar4 = PTR_Selection_ThresholdOperations_00047408;
  puVar3 = PTR_DAT_00047404;
  puVar2 = PTR_DAT_00047400;
  puVar1 = PTR_Selection_MaximumWordCurve_000473fc;
  iVar8 = (int)param_1;
  if ((iVar8 != 6) && (0 < iVar8)) {
    iVar7 = 0;
    iVar8 = 6 - iVar8;
    iVar9 = 5 - iVar8;
    if (0 < iVar8) {
      do {
        iVar5 = (int)DAT_000473f8;
        iVar7 = iVar7 + 1;
        *(undefined **)(puVar2 + iVar9 * 4) = puVar1;
        puVar4[iVar9] = 4;
        puVar3[iVar9] = 7;
        iVar6 = iVar9 + 5;
        *(int *)(puVar2 + iVar6 * 4) = iVar5 + iVar9 * 0xc;
        puVar4[iVar6] = 4;
        puVar3[iVar6] = 7;
        iVar9 = iVar9 + 1;
      } while (iVar7 < iVar8);
    }
  }
  return;
}

