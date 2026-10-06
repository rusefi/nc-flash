/* Ghidra analysis output; verify against original SH instructions. */

/* Executed MT-mode40 and911A qualification;9462 reset. Clutch8EBC/8EBD and neutral8EBE/8EBF;
   counterzero priority, otherwise transition recovery. */

uint LocalInputDiag_QualifyLatches(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  char cVar6;
  uint uVar5;
  
  puVar4 = PTR_LocalInputDiag_ClutchFault_0006c170;
  puVar3 = PTR_DAT_0006c16c;
  puVar2 = PTR_LocalInputDiag_NeutralFault_0006c168;
  puVar1 = PTR_DAT_0006c164;
  cVar6 = (*(code *)PTR_FUN_0006c154)(PTR_DAT_0006c174);
  if (cVar6 == '\x01') {
    *puVar4 = 0;
    *puVar3 = 0;
    *puVar2 = 0;
    uVar5 = 1;
  }
  else {
    uVar5 = -(((*PTR_TransmissionModeFlags_0006c240 & 0x40) == 0) - 1);
    if (uVar5 != 1) {
      return uVar5;
    }
    if ((byte)*PTR_DAT_0006c244 != 1) {
      return (uint)(byte)*PTR_DAT_0006c244;
    }
    if (*PTR_LocalInputDiag_ClutchEventCounter_0006c248 == '\0') {
      *puVar4 = 1;
      *puVar3 = 0;
      uVar5 = 1;
    }
    else {
      uVar5 = (uint)(byte)*PTR_DAT_0006c24c;
      if (uVar5 == 1) {
        *puVar4 = 0;
        *puVar3 = 1;
      }
    }
    if (*PTR_LocalInputDiag_NeutralEventCounter_0006c250 != '\0') {
      if ((byte)*PTR_DAT_0006c254 != 1) {
        return (uint)(byte)*PTR_DAT_0006c254;
      }
      *puVar2 = 0;
      *puVar1 = 1;
      return 1;
    }
    *puVar2 = 1;
  }
  *puVar1 = 0;
  return uVar5;
}

