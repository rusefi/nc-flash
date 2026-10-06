/* Ghidra analysis output; verify against original SH instructions. */

/* 6DFE==1 and7493!=0;active718C==1 with old749B0 resets7492,otherwise increments through0..7. */

char Pattern_AdvanceEventPosition(void)

{
  undefined *puVar1;
  char cVar2;
  
  puVar1 = PTR_Pattern_EventPosition_00045f08;
  cVar2 = *PTR_DAT_00045ef0;
  if ((cVar2 == '\x01') && (*PTR_Pattern_EventCylinder_00045ef8 != '\0')) {
    cVar2 = (*(code *)PTR_FUN_00045f10)(PTR_DAT_00045f0c);
    if ((cVar2 == '\x01') && (*PTR_Pattern_PreviousActive_00045f14 == '\0')) {
      cVar2 = '\0';
      *puVar1 = 0;
    }
    else if ((byte)*puVar1 < *DAT_00045f18) {
      *puVar1 = *puVar1 + 1;
    }
    else {
      *puVar1 = 0;
    }
  }
  return cVar2;
}

