/* Ghidra analysis output; verify against original SH instructions. */

/* Fiveconsecutive callswithoutcallback fromstale0 abortactiveexchange. Separate43AB/43AA
   saturation/threshold monitor. Physicaltimeunitsunproved. */

void SCI1_ServiceTimeoutAndMonitor(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  
  uVar2 = (*(code *)PTR_FUN_0000c03c)((int)DAT_0000c034);
  puVar1 = PTR_DAT_0000c044;
  if (*PTR_DAT_0000c040 != '\0') {
    if ((byte)*PTR_DAT_0000c048 <= (byte)*PTR_DAT_0000c044) {
      *PTR_DAT_0000c04c = 1;
    }
    if ((short)(ushort)(byte)*puVar1 < DAT_0000c036) {
      *puVar1 = *puVar1 + '\x01';
    }
  }
  (*(code *)PTR_FUN_0000c050)(uVar2);
  uVar2 = (*(code *)PTR_FUN_0000c03c)((int)DAT_0000c034);
  if (*PTR_SCI1_ExchangeActive_0000c054 == '\x01') {
    if ((byte)*PTR_DAT_0000c058 < 4) {
      *PTR_DAT_0000c058 = *PTR_DAT_0000c058 + '\x01';
    }
    else {
      SCI1_AbortCommandExchange();
    }
  }
  (*(code *)PTR_FUN_0000c050)(uVar2);
  return;
}

