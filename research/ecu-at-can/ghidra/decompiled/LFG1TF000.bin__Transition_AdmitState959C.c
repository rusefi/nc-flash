/* Ghidra analysis output; verify against original SH instructions. */

/* 9564==2 admits959C=2, snapshots80F2 to959E and resets81D7. Also computes95A0bit0; latter
   thresholds not exhaustively asserted.1280 cases in transition-gate.txt. */

void Transition_AdmitState959C(void)

{
  short sVar1;
  char cVar2;
  short *psVar3;
  byte *pbVar4;
  
  sVar1 = DAT_ffff80f2;
  pbVar4 = (byte *)(int)DAT_0002f28e;
  *pbVar4 = *pbVar4 & 0xfe;
  if (((((*PTR_DAT_0002f298 & 4) != 0) && (*(short *)PTR_DAT_0002f29c < *(short *)PTR_DAT_0002f2a0))
      && (*(short *)PTR_DAT_0002f2a4 <= sVar1)) && (sVar1 < *(short *)PTR_DAT_0002f2a8)) {
    *pbVar4 = *pbVar4 | 1;
  }
  cVar2 = Transition_CheckState959CAdmission();
  if (cVar2 == '\x01') {
    psVar3 = (short *)(int)DAT_0002f290;
    *(undefined1 *)(int)DAT_0002f28a = 2;
    *psVar3 = sVar1;
    *PTR_DAT_0002f294 = 0;
  }
  return;
}

