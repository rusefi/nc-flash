/* Ghidra analysis output; verify against original SH instructions. */

/* 88EE/88EA ->AC7A: either1 ->1;both2 ->2;otherwise3.25 combinations plus full CAN215
   invalid/recovery lifecycles verified; sharedgroup3B can substitute both values. */

void CAN_CombineTwoValidityInputs(void)

{
  undefined1 uVar1;
  
  uVar1 = 3;
  if ((*PTR_CAN215_SecondDifferenceValidity_00058534 == '\x02') &&
     (*PTR_CAN215_DifferenceValidity_00058538 == '\x02')) {
    uVar1 = 2;
  }
  if ((*PTR_CAN215_SecondDifferenceValidity_00058534 == '\x01') ||
     (*PTR_CAN215_DifferenceValidity_00058538 == '\x01')) {
    uVar1 = 1;
  }
  *(undefined1 *)(int)DAT_00058532 = uVar1;
  return;
}

