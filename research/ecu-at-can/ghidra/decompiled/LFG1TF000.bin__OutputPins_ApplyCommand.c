/* Ghidra analysis output; verify against original SH instructions. */

/* Exact8A18==1 selectsGPIOlow;previous8A19==1/current0 selectsPWM;otherpairsretainselection.
   Updatesprevious andPFDRbit14 viaoriginalhelpers. See tcu-output-pin-switch.txt. */

void OutputPins_ApplyCommand(void)

{
  char cVar1;
  undefined *puVar2;
  
  cVar1 = *(char *)(int)DAT_00018642;
  if (cVar1 == '\x01') {
    (*(code *)PTR_OutputPins_SelectGeneralLow_00018650)();
  }
  if ((*(char *)(int)DAT_00018644 == '\x01') && (cVar1 == '\0')) {
    (*(code *)PTR_OutputPins_SelectTimerOutputs_00018654)();
  }
  puVar2 = PTR_DAT_00018648;
  *(char *)(int)DAT_00018644 = cVar1;
  (*(code *)PTR_PortOutput_WriteDescriptor_0001864c)(puVar2,cVar1 == '\x01');
  return;
}

