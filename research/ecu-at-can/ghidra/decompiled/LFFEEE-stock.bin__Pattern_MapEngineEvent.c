/* Ghidra analysis output; verify against original SH instructions. */

/* With6DFE==1 map6DF2 events2/0/4/6 to7493 cylinders1/2/3/4;7494 alternate mapping. Otherwise
   hold.1152 mapping/position cases. */

char Pattern_MapEngineEvent(void)

{
  char cVar1;
  char cVar2;
  undefined1 uVar3;
  
  cVar1 = *PTR_DAT_00045ef4;
  cVar2 = *PTR_DAT_00045ef0;
  if (*PTR_DAT_00045ef0 == '\x01') {
    cVar2 = cVar1;
    if (cVar1 == '\x02') {
      *PTR_Pattern_EventCylinder_00045ef8 = 1;
    }
    else if (cVar1 == '\0') {
      *PTR_Pattern_EventCylinder_00045ef8 = 2;
    }
    else if (cVar1 == '\x04') {
      *PTR_Pattern_EventCylinder_00045ef8 = 3;
      cVar2 = '\x03';
    }
    else {
      if (cVar1 == '\x06') {
        uVar3 = 4;
      }
      else {
        uVar3 = 0;
      }
      *PTR_Pattern_EventCylinder_00045ef8 = uVar3;
    }
    if (cVar1 == '\0') {
      *PTR_Pattern_AlternateEventCylinder_00045efc = 1;
    }
    else if (cVar1 == '\x06') {
      *PTR_Pattern_AlternateEventCylinder_00045efc = 2;
      cVar2 = cVar1;
    }
    else if (cVar1 == '\x02') {
      *PTR_Pattern_AlternateEventCylinder_00045efc = 3;
      cVar2 = cVar1;
    }
    else if (cVar1 == '\x04') {
      *PTR_Pattern_AlternateEventCylinder_00045efc = 4;
      cVar2 = cVar1;
    }
    else {
      *PTR_Pattern_AlternateEventCylinder_00045efc = 0;
      cVar2 = cVar1;
    }
  }
  return cVar2;
}

