/* Ghidra analysis output; verify against original SH instructions. */

/* State0 holds published until lowfalse; pendinghigh usesunsigned84D0>=deadline; state2/high
   startsnow+2000. Highfalse resetsstate2 butpreservespublished. Included56B06 wholeRAMoracle. */

void Diagnostic_UpdateAdmissionDeadline(char *param_1,char *param_2,undefined1 *param_3)

{
  uint uVar1;
  int iVar2;
  
  if (*param_1 == '\0') {
    if (param_2[1] == '\0') {
      *param_1 = '\x02';
      *param_3 = 0;
      return;
    }
  }
  else if (*param_2 == '\0') {
    *param_1 = '\x02';
  }
  else {
    if (*param_1 != '\x01') {
      iVar2 = (*(code *)PTR_Tick_Read_00056cd8)();
      *(uint *)(param_1 + 4) = (uint)*(ushort *)PTR_DAT_00056cdc + iVar2;
      *param_1 = '\x01';
      return;
    }
    uVar1 = (*(code *)PTR_Tick_Read_00056cd8)();
    if (*(uint *)(param_1 + 4) <= uVar1) {
      *param_3 = 1;
      *param_1 = '\0';
      return;
    }
  }
  return;
}

