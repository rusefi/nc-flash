/* Ghidra analysis output; verify against original SH instructions. */

/* Fulloriginalinitializer returnsunderboundedHCAN/timerfixtures:124F8/19EC4 then8003=1
   and16650;8F6C0A producednatively.
   Whole11FA0coverage/selectedstatechecks,notcompleteindependentRAMoracle.
   Components256HCAN+256timer wholeRAM/MMIO PASS. tcu-hcan-startup.txt; nofullboot/hardwareproof. */

void CANTask_InitializeModeAndTimer(void)

{
  (*(code *)PTR_FUN_00012004)();
  DAT_ffff8003 = 1;
  (*DAT_00012008)();
  return;
}

