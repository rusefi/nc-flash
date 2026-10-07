/* Ghidra analysis output; verify against original SH instructions. */

/* Signed word616A+2*u16(index),readRTS delay slot.140paired setter/getter cases plus49FE0 producer
   traces. Stock initialization and threshold consumers executed; physical persistence unproved.
   tcu-stored-adjustments.txt. */

int StoredWord_ReadSignedAdjustment(ushort param_1)

{
  return (int)*(short *)(DAT_000245d0 + (uint)param_1 * 2);
}

