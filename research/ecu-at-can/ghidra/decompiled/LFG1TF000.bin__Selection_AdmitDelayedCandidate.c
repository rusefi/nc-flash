/* Ghidra analysis output; verify against original SH instructions. */

/* Reads8084, lastrequest9C75, direction9C77, timer815F/duration9C76; returnsFF whilepending
   elsecandidate.9C74 storesresult. Full37/18 countboundarylifecycles verified. */

int Selection_AdmitDelayedCandidate(void)

{
  char cVar1;
  short sVar2;
  int iVar3;
  byte bVar4;
  uint uVar5;
  byte bVar6;
  uint uVar7;
  byte *pbVar8;
  int iVar9;
  undefined1 *puVar10;
  int iVar11;
  
  bVar4 = Selection_ApplicationIndex;
  iVar11 = (int)DAT_000489c0;
  iVar3 = (int)(char)Selection_ApplicationIndex;
  cVar1 = *PTR_DAT_000489d4;
  Selection_UpdateDelayRowLatch();
  iVar9 = 0;
  bVar6 = *(byte *)(iVar11 + 1) & 1;
  if (bVar4 == *(byte *)(int)DAT_000489bc) {
    if (bVar6 != 1) goto LAB_0004895a;
  }
  else {
    if (bVar6 == 0) {
      *PTR_Selection_CandidateDelayTimer_000489d0 = 0;
    }
    bVar6 = CAN231_SixStateSource;
    puVar10 = (undefined1 *)(int)DAT_000489c2;
    *puVar10 = 0;
    if (bVar6 < bVar4) {
      *puVar10 = 1;
    }
    else if (bVar4 < bVar6) {
      *puVar10 = 2;
    }
  }
  iVar9 = Selection_SelectCandidateDelay(iVar3);
LAB_0004895a:
  sVar2 = DAT_000489be;
  uVar7 = (uint)DAT_000489be;
  uVar5 = ((uint)(byte)*PTR_Selection_CandidateDelayTimer_000489d0 - iVar9) + uVar7;
  if ((int)uVar7 < (int)(uVar5 & 0xffff)) {
    uVar5 = uVar7;
  }
  if ((cVar1 == '\x01') || (cVar1 == '\x02')) {
    uVar5 = uVar7;
  }
  *(char *)(int)DAT_000489c4 = (char)iVar9;
  *PTR_DAT_000489cc = (char)uVar5;
  if ((uVar5 & 0xff) == uVar7) {
    *(byte *)(iVar11 + 1) = *(byte *)(iVar11 + 1) & 0xfe;
    bVar6 = bVar4;
  }
  else {
    bVar6 = (byte)sVar2;
    *(byte *)(iVar11 + 1) = *(byte *)(iVar11 + 1) | 1;
  }
  *(byte *)(int)DAT_000489bc = bVar4;
  pbVar8 = (byte *)(int)DAT_000489ba;
  *pbVar8 = bVar6;
  if ((*PTR_ApplicationFaultFlags92D5_000489d8 & 1) == 0) {
    bVar4 = *(byte *)(iVar11 + 1) & 0xfb;
  }
  else {
    bVar4 = *(byte *)(iVar11 + 1) | 4;
  }
  *(byte *)(iVar11 + 1) = bVar4;
  return (int)(char)*pbVar8;
}

