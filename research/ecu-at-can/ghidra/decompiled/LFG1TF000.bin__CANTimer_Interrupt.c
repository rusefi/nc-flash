/* Ghidra analysis output; verify against original SH instructions. */

/* Original prefix to166FA preRTE:profileindex8/table5F620=16, clearF480bit10, F4E2+=625, call11FB2.
   20 component prefixes wholeRAM/MMIO/register PASS;600 native timeline interrupts with432 admitted
   frames. External timing/GSR/mailbox samples; TXPR commands only, no bus delivery.
   tcu-can-task-interrupt.txt. */

undefined8 CANTimer_Interrupt(void)

{
  undefined *puVar1;
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar2;
  short *psVar3;
  
  psVar3 = (short *)(int)DAT_00016708;
  (*(code *)PTR_OutputTask_RecordInterruptEntry_00016710)
            (8,(int)*(short *)(int)DAT_00016704 - (int)*psVar3);
  puVar2 = (ushort *)(int)DAT_00016700;
  if ((*puVar2 & DAT_00016702) != 0) {
    *puVar2 = *puVar2 & (ushort)PTR_DAT_0001670c;
    puVar1 = PTR_CANTask_AdmitAndDispatch_00016714;
    *psVar3 = *psVar3 + DAT_00016706;
    (*(code *)puVar1)();
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_00016718)(8);
  return CONCAT44(in_r1,in_r0);
}

