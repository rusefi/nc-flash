/* Ghidra analysis output; verify against original SH instructions. */

/* Lowbytecode<5:group7 unlesslowwordoperation18. Codes5..11:group8 unlessoperation6/8/10/12/16/17.
   Othercodes orsuppressedoperation returnFFFF.5632 directcases;code6/op8 explainsno numericrequest
   inoriginalreplacementtrace. tcu-transition-progress.txt. */

undefined4 * SparkRequest_SelectManagedGroup(undefined1 param_1,short param_2)

{
  undefined4 *puVar1;
  
  puVar1 = (undefined4 *)PTR_DAT_0004c89c;
  switch(param_1) {
  case 0:
  case 1:
  case 2:
  case 3:
  case 4:
    if (param_2 != 0x12) {
      puVar1 = (undefined4 *)0x7;
    }
    break;
  case 5:
  case 6:
  case 7:
  case 8:
  case 9:
  case 10:
  case 0xb:
    if ((((param_2 != 6) && (param_2 != 8)) && (param_2 != 10)) &&
       (((param_2 != 0xc && (param_2 != 0x10)) && (param_2 != 0x11)))) {
      puVar1 = &DAT_00000008;
    }
  }
  return puVar1;
}

