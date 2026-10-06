/* Ghidra analysis output; verify against original SH instructions. */

/* 71EC ->6B58 ->bytes0/1: truncate(source+512+0.5), clamp0..65534.6B62 exactly1 emitsFFFF. */

char CAN215_EncodeWord0(void)

{
  char cVar1;
  ushort uVar2;
  
  uVar2 = (*(code *)PTR_FUN_00036b58)
                    (*(undefined4 *)PTR_CAN215_PrimaryModelInput_00036b50,0x3f800000,DAT_00036b54);
  cVar1 = *PTR_CAN215_EncodeInvalidFlag_00036b5c;
  if (cVar1 == '\x01') {
    *(short *)PTR_CAN215_EncodedWord0_00036b20 = (short)DAT_00036b60;
  }
  else if (DAT_00036b64 < (int)(uint)uVar2) {
    *(short *)PTR_CAN215_EncodedWord0_00036b20 = (short)DAT_00036b64;
  }
  else {
    *(ushort *)PTR_CAN215_EncodedWord0_00036b20 = uVar2;
  }
  return cVar1;
}

