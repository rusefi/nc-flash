/* Ghidra analysis output; verify against original SH instructions. */

/* u8index*2 reads BEword4352;all19payloadwords checked afterfulltransfers. */

int SCI1_ReadReplyWord(uint param_1)

{
  return (int)*(short *)(PTR_SCI1_ReplyBuffer_0000c254 + (param_1 & 0xff) * 2);
}

