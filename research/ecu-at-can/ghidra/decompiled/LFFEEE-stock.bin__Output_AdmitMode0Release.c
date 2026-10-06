/* Ghidra analysis output; verify against original SH instructions. */

/* Distance>=child+16(record+32). Original callback executes within20290. */

undefined4 Output_AdmitMode0Release(int param_1,int param_2)

{
  uint uVar1;
  undefined4 uVar2;
  
  for (uVar1 = param_1 + 0x10;
      (uVar2 = 1, uVar1 < param_1 + 0x28U && (uVar2 = 0, *(int *)(uVar1 + 0x10) <= param_2));
      uVar1 = uVar1 + 0x18) {
  }
  return uVar2;
}

