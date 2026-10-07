/* Ghidra analysis output; verify against original SH instructions. */

/* 3072 wholeRAM gate cases:mode1 becomes3 when84A0/84D8 each2or3; mode3 with84A0=4 becomes5. 20
   complete1669A prefixes and600 native timeline IRQs PASS. CAN admitted220000/260000/280000phi
   before application readiness in explicit fixtures. tcu-can-task-interrupt.txt; no
   physical/fullboot proof. Extended native320 executes1310CANIRQs/960receipts, all1184oldprefix
   rows exact. Recovery868C0 due omittedfull15574, no healthy-recovery claim.
   tcu-native-can-lifecycle.txt. */

void CANTask_AdmitAndDispatch(void)

{
  if (DAT_ffff8003 == '\x01') {
    if (((*PTR_Startup_AdcBReadinessState_0001200c == '\x02') ||
        (*PTR_Startup_AdcBReadinessState_0001200c == '\x03')) &&
       ((*PTR_Startup_AdcAReadinessState_00012010 == '\x02' ||
        (*PTR_Startup_AdcAReadinessState_00012010 == '\x03')))) {
      DAT_ffff8003 = '\x03';
    }
  }
  else if ((DAT_ffff8003 == '\x03') && (*PTR_Startup_AdcAReadinessState_00012010 == '\x04')) {
    DAT_ffff8003 = '\x05';
  }
  (*(code *)PTR_FUN_00012014)();
  return;
}

