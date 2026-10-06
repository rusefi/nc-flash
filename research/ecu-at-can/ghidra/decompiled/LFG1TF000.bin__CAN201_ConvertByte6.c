/* Ghidra analysis output; verify against original SH instructions. */

/* Executed raw*5 ->8808, validity880A=2;FF holds old numeric with validity1. Physical role
   unproven. */

void CAN201_ConvertByte6(void)

{
  undefined *puVar1;
  undefined2 uVar2;
  undefined1 uVar3;
  
  uVar2 = *(undefined2 *)PTR_CAN201_Byte6Scaled_000170b8;
  uVar3 = 1;
  if ((uint)(byte)*PTR_DAT_000170c0 != (int)DAT_000170b2) {
    puVar1 = (undefined *)
             (*(code *)PTR_FUN_000170cc)
                       ((uint)(byte)*PTR_DAT_000170c0,PTR_DAT_000170c8,PTR_DAT_000170c4);
    if ((int)PTR_DAT_000170d0 < (int)puVar1) {
      puVar1 = PTR_DAT_000170d0;
    }
    if ((int)puVar1 < 0) {
      puVar1 = (undefined *)0x0;
    }
    uVar2 = SUB42(puVar1,0);
    uVar3 = 2;
  }
  puVar1 = PTR_CAN201_Byte6Validity_000170bc;
  *(undefined2 *)PTR_CAN201_Byte6Scaled_000170b8 = uVar2;
  *puVar1 = uVar3;
  return;
}

