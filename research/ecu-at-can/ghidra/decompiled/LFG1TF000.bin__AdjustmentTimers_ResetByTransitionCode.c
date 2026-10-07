/* Ghidra analysis output; verify against original SH instructions. */

/* 95D0zero no-op; nonzero table5D446[u16code] chooses counterreset then95D0=2. Code1
   extra822E/8160;code2 extra8161.144cases knowncodes0..10/u16truncation; tcu-adjustment-timers.txt.
    */

void AdjustmentTimers_ResetByTransitionCode(ushort param_1)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  char *pcVar4;
  
  pcVar4 = (char *)(int)DAT_00031178;
  if (*pcVar4 == '\0') {
    return;
  }
  cVar1 = PTR_DAT_0003117c[param_1];
  puVar3 = PTR_DAT_00031180;
  if (cVar1 == '\0') {
LAB_0003115e:
    *puVar3 = 0;
  }
  else {
    puVar2 = PTR_StoredAdjustment_Group0AbortTimer_00031184;
    if (cVar1 != '\x01') {
      if (cVar1 == '\x02') {
        *PTR_StoredAdjustment_Group1AbortTimer_00031188 = 0;
        if (param_1 == 1) {
          *PTR_DAT_0003118c = 0;
          *PTR_DAT_00031190 = 0;
        }
        goto LAB_00031160;
      }
      if (cVar1 == '\x03') {
        *PTR_StoredAdjustment_Group2AbortTimer_00031194 = 0;
        if (param_1 == 2) {
          *PTR_DAT_00031198 = 0;
        }
        goto LAB_00031160;
      }
      puVar2 = PTR_DAT_0003119c;
      puVar3 = PTR_DAT_000311a0;
      if (cVar1 != '\x04') goto LAB_0003115e;
    }
    *puVar2 = 0;
  }
LAB_00031160:
  *pcVar4 = '\x02';
  return;
}

