/* Ghidra analysis output; verify against original SH instructions. */

/* Selects parameter groupbase+10+recordindex; indices0..4.4D7CC compares hold elapsed; units
   unknown. See tcu-request-dispatch.txt. */

undefined1 SparkRequest_SelectHoldDuration(int param_1)

{
  byte bVar1;
  char cVar2;
  undefined *puVar3;
  undefined1 uVar4;
  
  bVar1 = *(byte *)(param_1 + 0xd);
  cVar2 = *(char *)(param_1 + 1);
  puVar3 = PTR_SparkRequest_FirstListDurationTables_70__0004d4b0;
  if ((((cVar2 != '\t') &&
       (puVar3 = PTR_SparkRequest_FirstListDurationTables_55__0004d4b4, cVar2 != '\b')) &&
      (cVar2 != '\v')) &&
     (puVar3 = PTR_SparkRequest_FirstListDurationTables_115__0004d4b8, cVar2 != '\n')) {
    if (cVar2 == '\a') {
      uVar4 = PTR_SparkRequest_FirstListDurationTables_40__0004d4bc[bVar1];
      if ((*(byte *)(param_1 + 0x12) & 0x20) != 0) {
        uVar4 = PTR_SparkRequest_FirstListDurationTables_85__0004d4ac[bVar1];
      }
      goto LAB_0004d440;
    }
    puVar3 = PTR_SparkRequest_FirstListDurationTables_25__0004d4c0;
    if (cVar2 != '\x06') {
      puVar3 = PTR_SparkRequest_FirstListDurationTables_10__0004d4c4;
    }
  }
  uVar4 = puVar3[bVar1];
LAB_0004d440:
  if (*(char *)(param_1 + 8) == '\x18') {
    uVar4 = PTR_SparkRequest_FirstListDurationTables_100__0004d4c8[bVar1];
  }
  if (*(char *)(param_1 + 8) == '\x17') {
    uVar4 = PTR_SparkRequest_FirstListDurationTables_85__0004d4ac[bVar1];
  }
  return uVar4;
}

