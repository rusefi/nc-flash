/* Ghidra analysis output; verify against original SH instructions. */

/* Executed byte-index+13 selection from eight15-byte tables763FC..76465;code+1 andoperation+8
   overrides,flag+18bit20 forcode7. Indices0..14 tested; origin bounds and time units open. */

undefined1 SparkRequest_SelectFirstListRampDuration(int param_1)

{
  byte bVar1;
  char cVar2;
  undefined *puVar3;
  undefined1 uVar4;
  
  bVar1 = *(byte *)(param_1 + 0xd);
  cVar2 = *(char *)(param_1 + 1);
  puVar3 = PTR_SparkRequest_FirstListDurationTables_60__0004d5c8;
  if ((((cVar2 != '\t') &&
       (puVar3 = PTR_SparkRequest_FirstListDurationTables_45__0004d5cc, cVar2 != '\b')) &&
      (cVar2 != '\v')) &&
     (puVar3 = PTR_SparkRequest_FirstListDurationTables_105__0004d5d0, cVar2 != '\n')) {
    if (cVar2 == '\a') {
      uVar4 = PTR_SparkRequest_FirstListDurationTables_30__0004d5d4[bVar1];
      if ((*(byte *)(param_1 + 0x12) & 0x20) != 0) {
        uVar4 = PTR_SparkRequest_FirstListDurationTables_75__0004d5c4[bVar1];
      }
      goto LAB_0004d534;
    }
    puVar3 = PTR_SparkRequest_FirstListDurationTables_15__0004d5d8;
    if (cVar2 != '\x06') {
      puVar3 = PTR_SparkRequest_FirstListDurationTables_0004d5dc;
    }
  }
  uVar4 = puVar3[bVar1];
LAB_0004d534:
  if (*(char *)(param_1 + 8) == '\x18') {
    uVar4 = PTR_SparkRequest_FirstListDurationTables_90__0004d5e0[bVar1];
  }
  if (*(char *)(param_1 + 8) == '\x17') {
    uVar4 = PTR_SparkRequest_FirstListDurationTables_75__0004d5c4[bVar1];
  }
  return uVar4;
}

