/* Ghidra analysis output; verify against original SH instructions. */

/* Executed:70F0 exact1 OR91E6 zero reload91E4=stock10; otherwise byte decrement saturates0.
   4096cases and2 actualtask boundaries. No physical-time units. */

undefined * Control_UpdateActivityCountdown(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  puVar1 = PTR_DAT_00077f90;
  puVar2 = (undefined *)(uint)(byte)*PTR_DAT_00077f98;
  if ((puVar2 == (undefined *)0x1) || (*PTR_Control_ActivityHysteresisFlag_00077f9c == '\0')) {
    *PTR_Control_ActivityHoldCounter_00077f94 = *PTR_DAT_00077f90;
    puVar2 = puVar1;
  }
  else if (*PTR_Control_ActivityHoldCounter_00077f94 != '\0') {
    *PTR_Control_ActivityHoldCounter_00077f94 =
         *PTR_Control_ActivityHoldCounter_00077f94 + (char)DAT_00077f8c;
  }
  return puVar2;
}

