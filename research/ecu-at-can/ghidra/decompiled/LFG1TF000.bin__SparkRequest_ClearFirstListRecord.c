/* Ghidra analysis output; verify against original SH instructions. */

/* Executed clearsrecord+18bit80 andrecord+4,sets allocated list entry0/mode0 through4C6DA. */

void SparkRequest_ClearFirstListRecord(undefined4 param_1,int param_2)

{
  undefined *puVar1;
  short sVar2;
  
  puVar1 = PTR_FUN_0004cfc0;
  *(byte *)(param_2 + 0x12) = *(byte *)(param_2 + 0x12) & 0x7f;
  sVar2 = (*(code *)puVar1)();
  puVar1 = PTR_SparkRequest_SetFirstListEntry_0004d00c;
  *(short *)(param_2 + 4) = sVar2;
  (*(code *)puVar1)((int)*(char *)(param_2 + 2),(int)sVar2,
                    -((((int)*(char *)(param_2 + 0x12) & 0x80U) == 0) - 1));
  return;
}

