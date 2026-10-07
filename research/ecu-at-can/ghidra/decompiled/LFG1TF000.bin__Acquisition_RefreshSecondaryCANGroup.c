/* Ghidra analysis output; verify against original SH instructions. */

/* Originalwrappercalls177A0,18258,1821C,181E0,181A4,175EC,17E74,1850C,1857C,185B8. Native1BD10
   logical1->1C10E->thiswrapper nowexecuted afteroriginalHCANISRprefix. Itusespreceding201 value
   when201 also pending. PhysicalCAN/ISR-RTE unproved; tcu-receive-admission.txt. */

void Acquisition_RefreshSecondaryCANGroup(void)

{
  (*(code *)PTR_FUN_0001ae14)();
  (*(code *)PTR_FUN_0001ae18)();
  (*(code *)PTR_FUN_0001ae1c)();
  (*(code *)PTR_FUN_0001ae20)();
  (*(code *)PTR_FUN_0001ae24)();
  (*(code *)PTR_CAN4EC_PublishComparisonEnable_0001ae28)();
  (*(code *)PTR_Comparison_SelectCANSource_0001ae2c)();
  (*(code *)PTR_FUN_0001ae30)();
  (*(code *)PTR_FUN_0001ae34)();
                    /* WARNING: Could not recover jumptable at 0x0001ae0a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_0001ae38)();
  return;
}

