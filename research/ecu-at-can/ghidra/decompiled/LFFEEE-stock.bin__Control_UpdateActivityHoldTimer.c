/* Ghidra analysis output; verify against original SH instructions. */

/* Executed6144cases:735Abit7clear reloadsword8FD4=stock480+120+40=640;else8FD8zero clears,otherwise
   decrementspositive. Eightactualtaskreturns checked;74D62 alreadyconsumedpriorvalue.
   Countsnotmilliseconds. */

uint Control_UpdateActivityHoldTimer(void)

{
  undefined4 uVar1;
  undefined2 uVar3;
  uint uVar2;
  
  uVar1 = (*(code *)PTR_FUN_0006f4c8)
                    ((int)*(short *)PTR_DAT_0006f4c4,(int)*(short *)PTR_DAT_0006f4c0);
  uVar3 = (*(code *)PTR_FUN_0006f4c8)(uVar1,(int)*(short *)PTR_DAT_0006f4cc);
  uVar2 = (uint)*DAT_0006f510;
  if ((uVar2 & 0x80) == 0) {
    *(undefined2 *)PTR_Control_ActivityHoldCounter_0006f4d0 = uVar3;
  }
  else if (*PTR_Control_ActivityTimerEnable_0006f520 == '\0') {
    uVar2 = 0;
    *(undefined2 *)PTR_Control_ActivityHoldCounter_0006f4d0 = 0;
  }
  else if (*(short *)PTR_Control_ActivityHoldCounter_0006f4d0 != 0) {
    *(short *)PTR_Control_ActivityHoldCounter_0006f4d0 =
         *(short *)PTR_Control_ActivityHoldCounter_0006f4d0 + (short)DAT_0006f524;
  }
  return uVar2;
}

