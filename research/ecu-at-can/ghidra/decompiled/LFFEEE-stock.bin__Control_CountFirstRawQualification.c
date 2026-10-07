/* Ghidra analysis output; verify against original SH instructions. */

/* 9462/8F00 exact1 reload50/50/3/3; else exact1 low/high flags saturatingdecrement.2048 cases;
   disabled qualification holds counters. See control-raw-enable.txt. */

char Control_CountFirstRawQualification(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  char cVar6;
  char cVar7;
  
  puVar5 = PTR_DAT_0006ce7c;
  puVar4 = PTR_DAT_0006ce78;
  puVar3 = PTR_DAT_0006ce70;
  puVar2 = PTR_DAT_0006ce6c;
  cVar6 = (*(code *)PTR_FUN_0006cea0)(PTR_DAT_0006ce9c);
  puVar1 = PTR_DAT_0006ce68;
  if ((cVar6 == '\x01') || (*PTR_DAT_0006ce98 == '\x01')) {
    cVar7 = '\x01';
    *puVar2 = *PTR_DAT_0006ce68;
    *puVar3 = *puVar1;
    puVar1 = PTR_DAT_0006ce74;
    *puVar4 = *PTR_DAT_0006ce74;
    *puVar5 = *puVar1;
  }
  else {
    cVar6 = (char)DAT_0006cf9a;
    if (*PTR_DAT_0006cf9c == '\x01') {
      if (*puVar2 != '\0') {
        *puVar2 = *puVar2 + cVar6;
      }
      if (*puVar4 != '\0') {
        *puVar4 = *puVar4 + cVar6;
      }
    }
    cVar7 = *PTR_DAT_0006cfa0;
    if (cVar7 == '\x01') {
      if (*puVar3 != '\0') {
        *puVar3 = *puVar3 + cVar6;
      }
      if (*puVar5 != '\0') {
        *puVar5 = *puVar5 + cVar6;
      }
    }
  }
  return cVar7;
}

