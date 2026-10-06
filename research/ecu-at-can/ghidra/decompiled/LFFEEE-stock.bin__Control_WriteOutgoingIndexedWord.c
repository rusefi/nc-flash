/* Ghidra analysis output; verify against original SH instructions. */

/* u8index*2+437A storeswordR5;executed all19 record words. Staticcaller224DE loop;startC00A
   notexecuted. */

void Control_WriteOutgoingIndexedWord(uint param_1,undefined2 param_2)

{
  *(undefined2 *)(PTR_Control_OutgoingWordBuffer_0000c250 + (param_1 & 0xff) * 2) = param_2;
  return;
}

