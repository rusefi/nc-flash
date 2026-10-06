/* Ghidra analysis output; verify against original SH instructions. */

/* Protected71C4 ->6B5C ->bytes4/5 with same offset/rounding/clamp/sentinel. Shared model input also
   affects CAN211. */

char CAN215_EncodeWord4(void)

{
  char cVar1;
  ushort uVar2;
  undefined4 uVar3;
  
  uVar3 = (*(code *)PTR_FUN_00036c54)(PTR_CAN215_SharedModelOffset_00036c50);
  uVar2 = (*(code *)PTR_FUN_00036c3c)(uVar3,0x3f800000,DAT_00036c38);
  cVar1 = *PTR_CAN215_EncodeInvalidFlag_00036c44;
  if (cVar1 == '\x01') {
    *(short *)PTR_CAN215_EncodedWord4_00036c58 = (short)DAT_00036c48;
  }
  else if (DAT_00036c4c < (int)(uint)uVar2) {
    *(short *)PTR_CAN215_EncodedWord4_00036c58 = (short)DAT_00036c4c;
  }
  else {
    *(ushort *)PTR_CAN215_EncodedWord4_00036c58 = uVar2;
  }
  return cVar1;
}

