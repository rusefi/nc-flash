/* Ghidra analysis output; verify against original SH instructions. */

/* 71B4 ->6B5A ->bytes2/3: truncate(source+512+0.5), clamp0..65534.6B62 exactly1 emitsFFFF. */

char CAN215_EncodeWord2(void)

{
  char cVar1;
  ushort uVar2;
  
  uVar2 = (*(code *)PTR_FUN_00036c3c)
                    (*(undefined4 *)PTR_CAN215_SecondModelInput_00036c34,0x3f800000,DAT_00036c38);
  cVar1 = *PTR_CAN215_EncodeInvalidFlag_00036c44;
  if (cVar1 == '\x01') {
    *(short *)PTR_DAT_00036c40 = (short)DAT_00036c48;
  }
  else if (DAT_00036c4c < (int)(uint)uVar2) {
    *(short *)PTR_DAT_00036c40 = (short)DAT_00036c4c;
  }
  else {
    *(ushort *)PTR_DAT_00036c40 = uVar2;
  }
  return cVar1;
}

