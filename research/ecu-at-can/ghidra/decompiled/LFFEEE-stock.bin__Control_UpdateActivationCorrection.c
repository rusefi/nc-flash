/* Ghidra analysis output; verify against original SH instructions. */

/* 67ACzero clears80E0;nonzero withprevious80F0zero selectsstockpulse
   by7242/7012/6E3C;elsedecaysold80E0 bystock.0005,floor0. Alwayssave67ACto80F0.
   Doesnotread7978;raw67AC2activeherebutnot59154. */

uint Control_UpdateActivationCorrection(void)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  char cVar5;
  uint uVar4;
  undefined4 extraout_fr0;
  float fVar6;
  undefined4 uVar7;
  
  puVar1 = PTR_FUN_0005933c;
  uVar3 = (*(code *)PTR_FUN_0005933c)(PTR_DAT_00059338);
  puVar2 = PTR_Control_ActivationCorrection_00059390;
  uVar7 = 0;
  if ((uVar3 & 0xff) == 0) {
    *(undefined4 *)PTR_Control_ActivationCorrection_00059390 = 0;
    uVar4 = uVar3;
  }
  else if (*PTR_Control_PreviousContributionEnable_00059394 == '\0') {
    cVar5 = (*(code *)puVar1)(PTR_DAT_00059398);
    if (cVar5 == '\x01') {
      uVar4 = (*(code *)puVar1)(PTR_DAT_0005935c);
      uVar4 = uVar4 & 0xff;
      if (uVar4 == 1) {
        uVar4 = (*(code *)puVar1)(PTR_DAT_0005939c);
        uVar4 = uVar4 & 0xff;
        if (uVar4 == 1) {
          uVar7 = *(undefined4 *)PTR_DAT_000593a0;
        }
        else {
          uVar7 = *(undefined4 *)PTR_DAT_000593a4;
        }
        *(undefined4 *)puVar2 = uVar7;
      }
      else {
        *(undefined4 *)puVar2 = *(undefined4 *)PTR_DAT_000593a8;
      }
    }
    else {
      uVar4 = (*(code *)puVar1)(PTR_DAT_0005935c);
      uVar4 = uVar4 & 0xff;
      if (uVar4 == 1) {
        uVar4 = (*(code *)puVar1)(PTR_DAT_0005939c);
        uVar4 = uVar4 & 0xff;
        if (uVar4 == 1) {
          uVar7 = *(undefined4 *)PTR_DAT_000593ac;
        }
        else {
          uVar7 = *(undefined4 *)PTR_DAT_000593b0;
        }
        *(undefined4 *)puVar2 = uVar7;
      }
      else {
        *(undefined4 *)puVar2 = *(undefined4 *)PTR_DAT_000593b4;
      }
    }
  }
  else {
    cVar5 = (*(code *)puVar1)(PTR_DAT_0005935c);
    if (cVar5 == '\x01') {
      cVar5 = (*(code *)puVar1)(PTR_DAT_0005939c);
      if (cVar5 == '\x01') {
        fVar6 = *(float *)PTR_DAT_000593b8;
      }
      else {
        fVar6 = *(float *)PTR_DAT_000593bc;
      }
    }
    else {
      fVar6 = *(float *)PTR_DAT_000593c0;
    }
    uVar4 = (*(code *)PTR_FUN_0005938c)(*(float *)puVar2 - fVar6,uVar7);
    *(undefined4 *)puVar2 = extraout_fr0;
  }
  *PTR_Control_PreviousContributionEnable_00059394 = (char)uVar3;
  return uVar4;
}

