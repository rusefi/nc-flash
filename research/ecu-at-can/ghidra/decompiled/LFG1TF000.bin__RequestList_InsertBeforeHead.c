/* Ghidra analysis output; verify against original SH instructions. */

/* Executed insert node at tail before given head with supplied value; stock active/free lists
   verified. */

void RequestList_InsertBeforeHead(byte param_1,byte param_2,int param_3,undefined2 param_4)

{
  byte bVar1;
  byte *pbVar2;
  
  pbVar2 = (byte *)((uint)param_1 * 4 + param_3);
  bVar1 = *pbVar2;
  *pbVar2 = param_2;
  pbVar2 = (byte *)((uint)param_2 * 4 + param_3);
  *(byte *)((uint)bVar1 * 4 + param_3 + 1) = param_2;
  *pbVar2 = bVar1;
  pbVar2[1] = param_1;
  *(undefined2 *)(pbVar2 + 2) = param_4;
  return;
}

