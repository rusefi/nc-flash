/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0002165c) */
/* Floor(8808*256/10) signed16 intermediate, cap25600;92D5mask08 ->zero. Verified over received
   raw0..254 and bounded held values. */

int CAN201_SelectByte6ApplicationValue(void)

{
  short sVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_c;
  undefined4 local_8;
  undefined1 local_4 [4];
  
  puVar4 = (undefined4 *)local_4;
  sVar1 = (*(code *)PTR_FixedPoint_DivideToSignedWord_000216bc)
                    ((uint)*(ushort *)PTR_CAN201_Byte6Scaled_000216b8 << 8,10);
  iVar3 = 1;
  if ((*PTR_ApplicationFaultFlags92D5_000216c0 & 8) != 0) {
    local_8 = 0;
    local_c = DAT_000216c4;
    puVar4 = &local_c;
    sVar1 = (*(code *)PTR_FUN_000216cc)();
  }
  iVar2 = (int)sVar1;
  if (iVar3 == 0) {
    *(undefined4 *)((int)puVar4 + -4) = 0;
    *(undefined4 *)((int)puVar4 + -8) = DAT_000216d4;
  }
  else {
    *(undefined4 *)((int)puVar4 + -4) = 0;
    *(undefined4 *)((int)puVar4 + -8) = DAT_000216d0;
  }
  sVar1 = (*(code *)PTR_FUN_000216cc)();
  if (sVar1 < iVar2) {
    if (iVar3 == 0) {
      *(undefined4 *)((int)puVar4 + -0xc) = 0;
      *(undefined4 *)((int)puVar4 + -0x10) = DAT_000216d4;
    }
    else {
      *(undefined4 *)((int)puVar4 + -0xc) = 0;
      *(undefined4 *)((int)puVar4 + -0x10) = DAT_000216d0;
    }
    sVar1 = (*(code *)PTR_FUN_000216cc)();
    iVar2 = (int)sVar1;
  }
  return iVar2;
}

