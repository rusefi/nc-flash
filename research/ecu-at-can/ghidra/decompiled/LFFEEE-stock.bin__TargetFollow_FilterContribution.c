/* Ghidra analysis output; verify against original SH instructions. */

/* Original2508 filters prior6808->6828;6956zero retention.94531 vsANYnonzero.99;eps125/65536.
   ExactRTZ140directcases; consumespriorcontributioninthe1Bcallerregion. */

void TargetFollow_FilterContribution(void)

{
  undefined *puVar1;
  char cVar2;
  undefined4 uVar3;
  float fVar4;
  float fVar5;
  
  puVar1 = PTR_TargetFollow_FilteredContribution_00031730;
  fVar5 = 1.0;
  uVar3 = DAT_0003172c;
  cVar2 = (*(code *)PTR_FUN_00031738)(PTR_TargetRamp_FallSelector_00031734);
  if (cVar2 == '\0') {
    fVar4 = *(float *)PTR_DAT_0003173c;
  }
  else {
    fVar4 = *(float *)PTR_DAT_00031740;
  }
  uVar3 = (*(code *)PTR_FUN_00031748)
                    (*(undefined4 *)PTR_Control_BoundedInputTermSum_00031744,*(undefined4 *)puVar1,
                     fVar5 - fVar4,uVar3);
  *(undefined4 *)puVar1 = uVar3;
  return;
}

