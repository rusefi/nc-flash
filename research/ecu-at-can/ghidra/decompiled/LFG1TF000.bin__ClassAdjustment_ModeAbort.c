/* Ghidra analysis output; verify against original SH instructions. */

/* Original371EA getter reads9870; lowbyte modes2/3/4/6 return1, else0. Covered through480 full369A4
   cases. */

undefined4 ClassAdjustment_ModeAbort(void)

{
  char cVar1;
  undefined4 uVar2;
  
  cVar1 = (*(code *)PTR_FUN_00036e4c)();
  uVar2 = 0;
  if ((((cVar1 == '\x02') || (cVar1 == '\x06')) || (cVar1 == '\x03')) || (cVar1 == '\x04')) {
    uVar2 = 1;
  }
  return uVar2;
}

