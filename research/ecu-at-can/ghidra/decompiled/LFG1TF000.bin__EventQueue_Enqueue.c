/* Ghidra analysis output; verify against original SH instructions. */

/* Eight-byte entries atA1B0+80*queue+8*tail: group,operation,payloadpointer; capacity10. Full
   request lifecycle executed; queue overflow not newly tested. See tcu-request-dispatch.txt. */

undefined4 EventQueue_Enqueue(uint param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  char cVar1;
  undefined2 *puVar2;
  byte *pbVar3;
  
  pbVar3 = PTR_DAT_0004c3ac + (param_1 & 0xff) * 3;
  if (9 < *pbVar3) {
    return 0xffffffff;
  }
  cVar1 = pbVar3[2] + 1;
  puVar2 = (undefined2 *)(PTR_DAT_0004c3b0 + (uint)pbVar3[2] * 8 + (param_1 & 0xff) * 0x50);
  *puVar2 = (short)((uint)param_3 >> 0x10);
  puVar2[1] = (short)param_3;
  *(undefined4 *)(puVar2 + 2) = param_4;
  *pbVar3 = *pbVar3 + 1;
  if (cVar1 == '\n') {
    cVar1 = '\0';
  }
  PTR_DAT_0004c3b4[(param_1 & 0xff) * 3] = cVar1;
  return 0;
}

