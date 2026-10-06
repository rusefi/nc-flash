/* Ghidra analysis output; verify against original SH instructions. */

/* 9415==0 andA939==1 admit.8BCE>=10 producesraw7 ->group35/C073 ->A98E ->CAN201 substitution/cut
   inhibit.1024 producer/gate cases; healthy active recovery keeps stored report. */

void HCAN_ProduceDiagnosticGroup35(char param_1)

{
  char cVar2;
  uint uVar1;
  ushort uVar3;
  char *pcVar4;
  byte *pbVar5;
  undefined4 uVar6;
  uint uVar7;
  
  if ((param_1 != '\0') && (param_1 == '\x01')) {
    uVar7 = 0;
    uVar6 = 0;
    cVar2 = (*(code *)PTR_FUN_0001a5e4)();
    pbVar5 = (byte *)(int)DAT_0001a5d8;
    pcVar4 = (char *)(int)DAT_0001a5da;
    if ((cVar2 == '\0') && (*PTR_DAT_0001a5e8 == '\x01')) {
      uVar7 = 1;
      uVar6 = 1;
      uVar3 = (ushort)*pbVar5;
      if (9 < uVar3) {
        uVar7 = 3;
      }
      if (*(ushort *)(PTR_DAT_0001a5ec + 4) <= uVar3) {
        uVar7 = uVar7 | 4;
      }
      if (*pcVar4 == '\0') {
        uVar6 = 3;
        if ((*PTR_DAT_0001a5f0 & 2) != 0) {
          uVar7 = uVar7 | (int)DAT_0001a5dc;
        }
        uVar1 = (*(code *)PTR_FUN_0001a5f4)(0x35);
        if (((*PTR_DAT_0001a5f0 & 4) != 0) && ((uVar1 & 1) == 1)) {
          uVar7 = uVar7 | (int)DAT_0001a5dc;
        }
      }
    }
    else {
      *(undefined1 *)(int)DAT_0001a5de = 0;
      *pcVar4 = '\0';
      *pbVar5 = 0;
    }
    (*(code *)PTR_Diagnostic_StoreGroupStatus_0001a5f8)(0x35,uVar7);
    (*(code *)PTR_Diagnostic_StoreMappedStatus_0001a5fc)(0x20,uVar6);
    return;
  }
  return;
}

