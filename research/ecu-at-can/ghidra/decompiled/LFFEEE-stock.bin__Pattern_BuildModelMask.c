/* Ghidra analysis output; verify against original SH instructions. */

/* 7182 ->4632A index tables using6542 ->74F4;718C gates/caps74F0;4639C uses74F2 to produce74F1.
   Executed within40660; event sampling and cylinder inhibition now in traction-pattern.txt. */

void Pattern_BuildModelMask(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined1 uVar4;
  char cVar5;
  
  uVar4 = Pattern_MapIndexToLevel((int)(char)*PTR_Pattern_EnabledIndex_00046364);
  puVar3 = PTR_FUN_00046374;
  puVar2 = PTR_DAT_00046370;
  puVar1 = PTR_Pattern_Level_0004636c;
  *PTR_Pattern_UngatedLevel_00046368 = uVar4;
  cVar5 = (*(code *)puVar3)(puVar2);
  if (cVar5 == '\0') {
    *puVar1 = 0;
  }
  else if ((byte)*PTR_Pattern_UngatedLevel_00046368 < 8) {
    *puVar1 = *PTR_Pattern_UngatedLevel_00046368;
  }
  else {
    *puVar1 = 7;
  }
  uVar4 = Pattern_SelectPhaseMask((int)(char)*puVar1);
  *PTR_Pattern_EventMask_00046378 = uVar4;
  return;
}

