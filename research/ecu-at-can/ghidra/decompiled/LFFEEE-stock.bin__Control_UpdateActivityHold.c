/* Ghidra analysis output; verify against original SH instructions. */

/* Executed9984 fullRAM cases:9149 from8FD4nonzero/925E1/915C1 or14450-qualified282Czero/default
   with914D/A562/900Azero. A556fall latches914D;always914E=A556. Invalidprotectedread
   records534C/5354. Eightactualtaskboundaries verifybefore42BCC andlater6F422 timerupdate.
   control-activity-hold.txt. */

undefined * Control_UpdateActivityHold(void)

{
  char cVar1;
  char cVar3;
  undefined *puVar2;
  
  cVar1 = *PTR_DAT_00074e58;
  if ((*PTR_Control_PreviousActivitySource_00074e5c != '\0') && (cVar1 == '\0')) {
    *PTR_Control_ActivityFallingLatch_00074e60 = 1;
  }
  puVar2 = PTR_Control_ActivityHoldCounter_00074e64;
  if ((*(short *)PTR_Control_ActivityHoldCounter_00074e64 == 0) &&
     (puVar2 = (undefined *)0x1, *PTR_DAT_00074e68 != '\x01')) {
    cVar3 = (*(code *)PTR_Control_CheckActivityReadEligibility_00074e6c)();
    if ((cVar3 == '\x01') &&
       (((*PTR_Control_ActivityFallingLatch_00074e60 == '\0' && (*PTR_DAT_00074e70 == '\0')) &&
        (*PTR_DAT_00074e74 == '\0')))) {
      cVar3 = (*(code *)PTR_Protected_ReadByteOrDefault_00074e7c)(PTR_DAT_00074e78,0);
      puVar2 = (undefined *)0x0;
      if (cVar3 == '\0') goto LAB_00074de0;
    }
    puVar2 = (undefined *)0x1;
    if (*PTR_Control_IndependentActivityHold_00074e80 != '\x01') {
      puVar2 = (undefined *)0x0;
      *PTR_Control_ActivityHold_00074e84 = 0;
      goto LAB_00074dee;
    }
  }
LAB_00074de0:
  *PTR_Control_ActivityHold_00074e84 = 1;
LAB_00074dee:
  *PTR_Control_PreviousActivitySource_00074e5c = cVar1;
  return puVar2;
}

