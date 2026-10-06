/* Ghidra analysis output; verify against original SH instructions. */

/* Executed second-list allocation; incrementsA258 even when helper returnsFF due exhaustion. */

void SparkRequest_AllocateSecondList(undefined4 param_1)

{
  (*(code *)PTR_RequestList_Allocate_0004cb80)
            (param_1,PTR_DAT_0004cb78,PTR_SparkRequest_SecondListDescriptor_0004cb74);
  *(short *)(int)DAT_0004cb68 = *(short *)(int)DAT_0004cb68 + 1;
  return;
}

