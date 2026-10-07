/* Ghidra analysis output; verify against original SH instructions. */

/* Stock widthDA710-DA714=-7;80F4=clamp(RTZ(RTZ(6D5C-7)/-7),.5,1),80F8=clampsameinput[1,1]=1.
   Original207C/2118helpers; nearzero-widthalternatecalibrationunexecuted. */

void Control_UpdateMagnitudeScales(void)

{
  undefined *puVar1;
  char cVar2;
  float fVar3;
  undefined4 uVar4;
  float fVar5;
  undefined4 uVar6;
  
  fVar5 = *(float *)PTR_DAT_000596fc - *(float *)PTR_DAT_000596f8;
  cVar2 = (*(code *)PTR_FUN_00059704)(fVar5,0,DAT_00059700);
  uVar6 = 0x3f800000;
  if (cVar2 == '\0') {
    *(undefined4 *)PTR_Control_MagnitudeBaselineScale_00059714 = 0x3f800000;
    *(undefined4 *)PTR_Control_MagnitudePulseScale_0005971c = 0x3f800000;
  }
  else {
    fVar3 = (float)(*(code *)PTR_FUN_00059698)(PTR_SpeedCandidate_ProtectedSelected_00059708);
    fVar5 = (fVar3 - *(float *)PTR_DAT_000596f8) / fVar5;
    uVar4 = (*(code *)PTR_FUN_00059710)(fVar5,*(undefined4 *)PTR_DAT_0005970c,uVar6);
    puVar1 = PTR_DAT_00059718;
    *(undefined4 *)PTR_Control_MagnitudeBaselineScale_00059714 = uVar4;
    uVar6 = (*(code *)PTR_FUN_00059710)(fVar5,*(undefined4 *)puVar1,uVar6);
    *(undefined4 *)PTR_Control_MagnitudePulseScale_0005971c = uVar6;
  }
  return;
}

