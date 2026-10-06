/* Ghidra analysis output; verify against original SH instructions. */

/* AT branch reads protected2184 (CAN216 byte7 bit1) into6E53; MT clears it. Also normalizes CAN231
   states. Paired fault-reporting execution verified. */

uint CAN_UpdateATStatusFlags(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  uint uVar4;
  undefined1 uVar5;
  
  puVar3 = PTR_FUN_0003b400;
  puVar2 = PTR_DAT_0003b3fc;
  puVar1 = PTR_DAT_0003b3f8;
  if ((*PTR_TransmissionModeFlags_0003b3d4 & 0x40) == 0) {
    (*(code *)PTR_FUN_0003b400)(PTR_DAT_0003b404,*PTR_DAT_0003b414 == '\x01');
    (*(code *)puVar3)(PTR_DAT_0003b408,*PTR_DAT_0003b418 == '\x01');
    (*(code *)puVar3)(PTR_DAT_0003b40c,*PTR_DAT_0003b41c == '\x01');
    (*(code *)puVar3)(PTR_DAT_0003b410,*PTR_DAT_0003b420 == '\x01');
    if (*PTR_DAT_0003b424 == '\x01') {
      *puVar2 = 1;
    }
    else {
      *puVar2 = 0;
    }
    uVar4 = (*(code *)PTR_Protected_ReadByteOrDefault_0003b42c)(PTR_DAT_0003b428,0);
    if ((uVar4 & 0xff) != 1) {
      *puVar1 = 0;
      return uVar4 & 0xff;
    }
    uVar5 = 1;
    uVar4 = 1;
  }
  else {
    (*(code *)PTR_FUN_0003b400)(PTR_DAT_0003b404,0);
    (*(code *)puVar3)(PTR_DAT_0003b408,0);
    (*(code *)puVar3)(PTR_DAT_0003b40c,0);
    uVar4 = (*(code *)puVar3)(PTR_DAT_0003b410,0);
    *puVar2 = 0;
    uVar5 = 0;
  }
  *puVar1 = uVar5;
  return uVar4;
}

