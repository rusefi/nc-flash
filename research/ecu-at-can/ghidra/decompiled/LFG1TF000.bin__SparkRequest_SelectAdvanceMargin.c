/* Ghidra analysis output; verify against original SH instructions. */

/* Selects parameter groupbase+5+recordindex; indices0..4 from3138A. Resulttimes64 enters4D7A2
   threshold. See tcu-request-dispatch.txt. */

undefined1 SparkRequest_SelectAdvanceMargin(int param_1)

{
  byte bVar1;
  char cVar2;
  undefined *puVar3;
  undefined1 uVar4;
  
  bVar1 = *(byte *)(param_1 + 0xd);
  cVar2 = *(char *)(param_1 + 1);
  puVar3 = PTR_SparkRequest_FirstListDurationTables_65__0004d490;
  if ((((cVar2 != '\t') &&
       (puVar3 = PTR_SparkRequest_FirstListDurationTables_50__0004d494, cVar2 != '\b')) &&
      (cVar2 != '\v')) &&
     (puVar3 = PTR_SparkRequest_FirstListDurationTables_110__0004d498, cVar2 != '\n')) {
    if (cVar2 == '\a') {
      uVar4 = PTR_SparkRequest_FirstListDurationTables_35__0004d49c[bVar1];
      if ((*(byte *)(param_1 + 0x12) & 0x20) != 0) {
        uVar4 = PTR_SparkRequest_FirstListDurationTables_80__0004d48c[bVar1];
      }
      goto LAB_0004d3b8;
    }
    puVar3 = PTR_SparkRequest_FirstListDurationTables_20__0004d4a0;
    if (cVar2 != '\x06') {
      puVar3 = PTR_SparkRequest_FirstListDurationTables_5__0004d4a4;
    }
  }
  uVar4 = puVar3[bVar1];
LAB_0004d3b8:
  if (*(char *)(param_1 + 8) == '\x18') {
    uVar4 = PTR_SparkRequest_FirstListDurationTables_95__0004d4a8[bVar1];
  }
  if (*(char *)(param_1 + 8) == '\x17') {
    uVar4 = PTR_SparkRequest_FirstListDurationTables_80__0004d48c[bVar1];
  }
  return uVar4;
}

