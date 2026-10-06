/* Ghidra analysis output; verify against original SH instructions. */

/* Static ISR: tests/clears TSR0FFFFF42C bit0, reads32-bit ICR0AFFFFF434, passes captured value
   to179A8. Interrupt/peripheral execution not emulated. */

undefined8 Capture0A_Interrupt(void)

{
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar1;
  
  (*(code *)PTR_FUN_00016cd4)(5,0);
  puVar1 = (ushort *)(int)DAT_00016cd0;
  if ((*puVar1 & 1) != 0) {
    *puVar1 = *puVar1 & (ushort)PTR_DAT_00016cd8;
    (*(code *)PTR_Capture0A_ProcessCapturedCount_00016cdc)(*(undefined4 *)(int)DAT_00016cd2);
  }
  (*(code *)PTR_FUN_00016ce0)(5);
  return CONCAT44(in_r1,in_r0);
}

