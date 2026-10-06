/* Ghidra analysis output; verify against original SH instructions. */

/* Executed doubly linked node unlink; independent queue invariants checked across600 stateful
   operations. */

void RequestList_Unlink(uint param_1,int param_2)

{
  byte bVar1;
  byte bVar2;
  byte *pbVar3;
  
  pbVar3 = (byte *)((param_1 & 0xff) * 4 + param_2);
  bVar1 = *pbVar3;
  bVar2 = pbVar3[1];
  *(byte *)((uint)bVar1 * 4 + param_2 + 1) = bVar2;
  *(byte *)((uint)bVar2 * 4 + param_2) = bVar1;
  return;
}

