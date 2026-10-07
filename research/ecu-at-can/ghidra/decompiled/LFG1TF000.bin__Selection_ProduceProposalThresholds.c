/* Ghidra analysis output; verify against original SH instructions. */

/* Captures axis9B3E, or941E for ENTRY source13/14, before dispatch5DE90 updates source.
   tcu-threshold-axis-history.txt verifies60 calls/600 lookups/60 scans; exiting13/14 can change
   next proposal1->4. Class overlay47240 independently modeled. Optional44E14/44F5A now
   modeled:3283direct,72admission,48threshold/scan and16full replays in tcu-optional-thresholds.txt.
   Upstream stored adjustments/task order remain open. */

void Selection_ProduceProposalThresholds(void)

{
  byte bVar1;
  short sVar2;
  short sVar3;
  short sVar4;
  bool bVar5;
  undefined4 uVar6;
  int iVar7;
  uint uVar8;
  int iVar9;
  undefined4 *puVar10;
  
  sVar2 = *(short *)PTR_Selection_ProposalLookupAxis_00045474;
  sVar3 = *(short *)PTR_DAT_00045478;
  sVar4 = *(short *)PTR_DAT_0004547c;
  bVar1 = *PTR_DAT_00045480;
  bVar5 = false;
  if ((*PTR_Selection_SourceCode_00045484 == '\r') || (*PTR_Selection_SourceCode_00045484 == '\x0e')
     ) {
    sVar2 = *(short *)PTR_DAT_00045488;
  }
  puVar10 = (undefined4 *)PTR_Selection_ThresholdProducerDispatch_0004548c;
  for (iVar9 = 0; iVar9 < *(short *)PTR_Selection_ThresholdProducerCount_00045490; iVar9 = iVar9 + 1
      ) {
    (*(code *)*puVar10)();
    puVar10 = puVar10 + 1;
  }
  if ((((*(short *)PTR_DAT_00045494 <= DAT_ffff80f2) &&
       ((*PTR_Request_CancellationFlags_00045498 & 0x10) == 0)) && ((*PTR_DAT_0004549c & 0x10) == 0)
      ) && ((TransmissionStateClass != 0xff && ((*PTR_DAT_000454a0 & 1) == 0)))) {
    bVar5 = true;
  }
  iVar9 = 0;
  uVar8 = ((int)(char)*PTR_DAT_000454a4 & 1U) + (uint)(byte)-(((bVar1 & 8) == 0) + -1) * 2;
  do {
    uVar6 = (*(code *)PTR_Lookup_InterpolateWordCurve_000454ac)
                      ((int)sVar2,*(undefined4 *)(PTR_DAT_000454a8 + iVar9 * 4));
    if (((PTR_DAT_000454b0[iVar9] == '\0') || (PTR_DAT_000454b0[iVar9] == '\x01')) &&
       ((bVar5 && ((((iVar9 != 4 && (iVar9 != 9)) && (iVar9 != 3)) && (iVar9 != 8)))))) {
      uVar6 = (*(code *)PTR_Selection_AdjustThresholdFromStoredOffset_000454b4)
                        (iVar9,uVar6,(int)sVar3 << 1);
    }
    if (((1 < iVar9) && (iVar9 < 5)) && ((uVar8 & 0xff) != 0)) {
      uVar6 = (*(code *)PTR_Selection_ApplyModeThresholdFloor_000454b8)
                        (iVar9,uVar6,(int)(short)(sVar4 << 3),uVar8);
    }
    iVar7 = iVar9 * 2;
    iVar9 = iVar9 + 1;
    *(short *)(PTR_Selection_ProposalThresholds_000454bc + iVar7) = (short)uVar6;
  } while (iVar9 < 10);
  return;
}

