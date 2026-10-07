/* Ghidra analysis output; verify against original SH instructions. */

/* State1 clears for modes2/3/4/5/6 elseholds; state2 stock36948rejects to0; explicitstate3
   calls36B26(+11) thenclears.280fullcases. Otherstatesretain; no global reachability claim. */

int ClassAdjustment_UniformStateMachine(void)

{
  int iVar1;
  
  if (*(char *)(int)DAT_000368e0 == '\x01') {
    FUN_0003689e();
  }
  else if (*(char *)(int)DAT_000368e0 == '\x02') {
    FUN_000368b6();
  }
  if (*(char *)(int)DAT_000368e0 != 3) {
    return (int)*(char *)(int)DAT_000368e0;
  }
  (*(code *)PTR_ClassAdjustment_ShiftAll_000368ec)((int)*(short *)PTR_DAT_000368e8);
  iVar1 = FUN_000368d6();
  return iVar1;
}

