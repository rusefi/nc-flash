/* Ghidra analysis output; verify against original SH instructions. */

/* Float6CF8 ->6B3A via20B8 scale0.5 offset0; bounded quantization verified. TP_6CF8 XML clue is not
   proof of physical source. */

void CAN201_EncodeByte6Candidate(void)

{
  undefined1 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00036834)(*(undefined4 *)PTR_DAT_00036830,DAT_0003682c,0);
  *PTR_DAT_00036838 = uVar1;
  return;
}

