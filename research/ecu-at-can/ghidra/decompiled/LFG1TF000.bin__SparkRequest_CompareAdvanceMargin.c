/* Ghidra analysis output; verify against original SH instructions. */

/* Signed80EE>=signed32reference9218[5D446[code]]-64*argument; measured source alsofeedsCAN216byte4.
   See tcu-request-dispatch.txt. */

bool SparkRequest_CompareAdvanceMargin(int param_1,int param_2)

{
  return *(int *)(PTR_Phase_ProducedReferenceWords_0004d860 +
                 (uint)(byte)PTR_DAT_0004d85c[*(byte *)(param_2 + 1)] * 4) + param_1 * -0x40 <=
         (int)Phase_MeasuredSourceSample;
}

