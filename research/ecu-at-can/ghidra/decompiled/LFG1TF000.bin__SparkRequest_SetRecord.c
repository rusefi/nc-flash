/* Ghidra analysis output; verify against original SH instructions. */

/* r4 index,r5 signed-word value,r6 mode byte ->915C+2*index and9166+index.175 set/reset cases cover
   validindices0..4 only. */

void SparkRequest_SetRecord(char param_1,undefined4 param_2,char param_3)

{
  (*(code *)PTR_FUN_0001fc1c)((int)DAT_0001fc00,(int)param_1,param_2);
  (*(code *)PTR_FUN_0001fc20)((int)DAT_0001fc04,(int)param_1,(int)param_3);
  return;
}

