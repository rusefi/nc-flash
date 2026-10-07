/* Ghidra analysis output; verify against original SH instructions. */

/* 9462 exact1 or8F38 exact1 reloads50/50/3/3; else exact1 low/high flags decrement corresponding
   counters saturatingzero.2048 cases. See control-raw-provenance.txt. */

char Control_CountRawQualification(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  char cVar6;
  char cVar7;
  
  puVar5 = PTR_DAT_0006d95c;
  puVar4 = PTR_DAT_0006d958;
  puVar3 = PTR_DAT_0006d950;
  puVar2 = PTR_DAT_0006d94c;
  cVar6 = (*(code *)PTR_FUN_0006d980)(PTR_DAT_0006d97c);
  puVar1 = PTR_DAT_0006d948;
  if ((cVar6 == '\x01') || (*PTR_DAT_0006d978 == '\x01')) {
    cVar7 = '\x01';
    *puVar2 = *PTR_DAT_0006d948;
    *puVar3 = *puVar1;
    puVar1 = PTR_DAT_0006d954;
    *puVar4 = *PTR_DAT_0006d954;
    *puVar5 = *puVar1;
  }
  else {
    cVar6 = (char)DAT_0006da7a;
    if (*PTR_DAT_0006da7c == '\x01') {
      if (*puVar2 != '\0') {
        *puVar2 = *puVar2 + cVar6;
      }
      if (*puVar4 != '\0') {
        *puVar4 = *puVar4 + cVar6;
      }
    }
    cVar7 = *PTR_DAT_0006da80;
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

