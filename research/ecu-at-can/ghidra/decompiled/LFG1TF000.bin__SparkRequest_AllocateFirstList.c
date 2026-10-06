/* Ghidra analysis output; verify against original SH instructions. */

/* Executed first-list allocation; incrementsA202 even when helper returnsFF due exhaustion. No
   invalid-handle setter test. */

void SparkRequest_AllocateFirstList(undefined4 param_1)

{
  (*(code *)PTR_RequestList_Allocate_0004c72c)
            (param_1,PTR_DAT_0004c724,PTR_SparkRequest_FirstListDescriptor_0004c720);
  *(short *)(int)DAT_0004c704 = *(short *)(int)DAT_0004c704 + 1;
  return;
}

