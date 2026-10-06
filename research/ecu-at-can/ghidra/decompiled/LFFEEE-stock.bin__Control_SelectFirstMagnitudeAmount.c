/* Ghidra analysis output; verify against original SH instructions. */

/* 810C=0unless7242exact1;else eightstockconstants selectedby67ACexact1,7012exact1,abs72B4>=9999.
   Signedboundarytests; no physicalsourceidentity. */

char Control_SelectFirstMagnitudeAmount(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  undefined4 uVar4;
  float fVar5;
  undefined4 uVar6;
  
  uVar6 = 0;
  uVar4 = (*(code *)PTR_FUN_00059698)(PTR_Control_FirstMagnitudeInput_00059694);
  fVar5 = (float)(*(code *)PTR_FUN_0005969c)(uVar4,uVar6);
  puVar2 = PTR_Control_FirstMagnitudeAmount_000596a4;
  puVar1 = PTR_FUN_000596a0;
  cVar3 = (*(code *)PTR_FUN_000596a0)(PTR_DAT_000596a8);
  if (cVar3 == '\x01') {
    cVar3 = (*(code *)puVar1)(PTR_DAT_000596ac);
    if (cVar3 == '\x01') {
      if (fVar5 < *(float *)PTR_DAT_000596b0) {
        cVar3 = (*(code *)puVar1)(PTR_DAT_000596b4);
        if (cVar3 == '\x01') {
          uVar4 = *(undefined4 *)PTR_DAT_000596c0;
        }
        else {
          uVar4 = *(undefined4 *)PTR_DAT_000596c4;
        }
        *(undefined4 *)puVar2 = uVar4;
      }
      else {
        cVar3 = (*(code *)puVar1)(PTR_DAT_000596b4);
        if (cVar3 == '\x01') {
          uVar4 = *(undefined4 *)PTR_DAT_000596b8;
        }
        else {
          uVar4 = *(undefined4 *)PTR_DAT_000596bc;
        }
        *(undefined4 *)puVar2 = uVar4;
      }
    }
    else if (fVar5 < *(float *)PTR_DAT_000596b0) {
      cVar3 = (*(code *)puVar1)(PTR_DAT_000596b4);
      if (cVar3 == '\x01') {
        uVar4 = *(undefined4 *)PTR_DAT_000596d0;
      }
      else {
        uVar4 = *(undefined4 *)PTR_DAT_000596d4;
      }
      *(undefined4 *)puVar2 = uVar4;
    }
    else {
      cVar3 = (*(code *)puVar1)(PTR_DAT_000596b4);
      if (cVar3 == '\x01') {
        uVar4 = *(undefined4 *)PTR_DAT_000596c8;
      }
      else {
        uVar4 = *(undefined4 *)PTR_DAT_000596cc;
      }
      *(undefined4 *)puVar2 = uVar4;
    }
  }
  else {
    *(undefined4 *)puVar2 = uVar6;
  }
  return cVar3;
}

