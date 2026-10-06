/* Ghidra analysis output; verify against original SH instructions. */

/* STATIC: tests/clears bit7 ofFFFFF718 then12386, bounded by15B80/15BF0(13). ISR and hardware not
   executed by timing verifier. */

undefined8 Timer_CMT1InterruptLead(void)

{
  undefined *puVar1;
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar2;
  
  (*(code *)PTR_FUN_00016d4c)(0xd,0);
  puVar1 = PTR_Timer_PromoteAndServiceMode_00016d54;
  puVar2 = (ushort *)(int)DAT_00016d48;
  if ((*puVar2 & 0x80) != 0) {
    *puVar2 = *puVar2 & (ushort)PTR_DAT_00016d50;
    (*(code *)puVar1)();
  }
  (*(code *)PTR_FUN_00016d58)(0xd);
  return CONCAT44(in_r1,in_r0);
}

