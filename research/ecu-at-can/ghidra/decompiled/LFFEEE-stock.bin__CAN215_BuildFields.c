/* Ghidra analysis output; verify against original SH instructions. */

/* Copies6E2E to6B62; executes numeric/status builders and tail36C74. Verified together with packer;
   see can215-feedback.txt. */

void CAN215_BuildFields(void)

{
  *PTR_CAN215_EncodeInvalidFlag_00036a24 = *PTR_DAT_00036a20;
  CAN215_EncodeWord0();
  CAN215_EncodeWord2();
  CAN215_EncodeWord4();
  CAN215_EncodeSelectedControlByte();
  FUN_00036c74();
  return;
}

