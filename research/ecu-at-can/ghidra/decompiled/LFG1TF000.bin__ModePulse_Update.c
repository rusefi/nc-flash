/* Ghidra analysis output; verify against original SH instructions. */

/* StartupA520 exact0->1 with8280<stock92 createsfirst/secondpulse.
   Exact1requestbytes;second/thirdstateclearwhenrespectivebytecounter>=15.
   FullRAMoracleatactualphase0/4. See tcu-inhibit-writers.txt. */

void ModePulse_Update(void)

{
  bool bVar1;
  undefined *puVar2;
  undefined *puVar3;
  char *pcVar4;
  undefined1 uVar5;
  char cVar6;
  
  bVar1 = false;
  if ((((byte)*PTR_DAT_00023e98 < (byte)*PTR_ModePulse_StartupCounterLimit_00023ea0) &&
      (*(char *)(int)DAT_00023e88 == '\0')) && (*DAT_00023e9c == '\x01')) {
    bVar1 = true;
  }
  pcVar4 = (char *)(int)DAT_00023e82;
  *(char *)(int)DAT_00023e88 = *DAT_00023e9c;
  uVar5 = 0;
  if ((*pcVar4 == '\x01') || (bVar1)) {
    uVar5 = 1;
    *(undefined1 *)(int)DAT_00023e82 = 0;
  }
  puVar2 = PTR_ModePulse_SecondState_00023e90;
  *PTR_ModePulse_FirstState_00023e8c = uVar5;
  puVar3 = PTR_ModePulse_SecondCounter_00023ea4;
  cVar6 = *puVar2;
  if ((*(char *)(int)DAT_00023e84 == '\x01') || (bVar1)) {
    cVar6 = '\x01';
    *(undefined1 *)(int)DAT_00023e84 = 0;
    *puVar3 = 0;
  }
  if ((cVar6 == '\x01') && (0xe < (byte)*PTR_ModePulse_SecondCounter_00023ea4)) {
    cVar6 = '\0';
  }
  *PTR_ModePulse_SecondState_00023e90 = cVar6;
  puVar3 = PTR_ModePulse_ThirdCounter_00023ea8;
  puVar2 = PTR_ModePulse_ThirdState_00023e94;
  cVar6 = *PTR_ModePulse_ThirdState_00023e94;
  if (*(char *)(int)DAT_00023e86 == '\x01') {
    cVar6 = '\x01';
    *(undefined1 *)(int)DAT_00023e86 = 0;
    *puVar3 = 0;
  }
  if ((cVar6 == '\x01') && (0xe < (byte)*PTR_ModePulse_ThirdCounter_00023ea8)) {
    cVar6 = '\0';
  }
  *puVar2 = cVar6;
  return;
}

