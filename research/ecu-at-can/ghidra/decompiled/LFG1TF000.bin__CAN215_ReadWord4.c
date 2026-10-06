/* Ghidra analysis output; verify against original SH instructions. */

/* Returns BE word bytes4/5 of CAN215 receive buffer8F2C; executed by complete callback. */

undefined2 CAN215_ReadWord4(void)

{
  undefined2 uVar1;
  
  (*(code *)PTR_FUN_0001c8bc)();
  uVar1 = *(undefined2 *)(PTR_DAT_0001c8c8 + 4);
  (*(code *)PTR_FUN_0001c8c4)();
  return uVar1;
}

