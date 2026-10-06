/* Ghidra analysis output; verify against original SH instructions. */

/* Only mode40:6AC7 bit2 iff protected723A==1;bit1 iff protected723E==1;bit0 iff8EBC==1 OR8EBE==1.
   All other bits zero.1024 builder/packer cases. PRHT use unproved. */

uint CAN231_BuildMTDiscreteFlags(void)

{
  uint uVar1;
  char cVar2;
  byte bVar3;
  
  uVar1 = -(((*PTR_TransmissionModeFlags_00035cb8 & 0x40) == 0) - 1);
  if (uVar1 == 1) {
    bVar3 = 0;
    cVar2 = (*(code *)PTR_FUN_00035cc4)(PTR_Selector_CombinedFlag_00035cc0);
    if (cVar2 == '\x01') {
      bVar3 = 4;
    }
    cVar2 = (*(code *)PTR_FUN_00035cc4)(PTR_DAT_00035cc8);
    if (cVar2 == '\x01') {
      bVar3 = bVar3 | 2;
    }
    uVar1 = 1;
    if ((*PTR_LocalInputDiag_NeutralFault_00035ccc == '\x01') ||
       (uVar1 = (uint)(byte)*PTR_LocalInputDiag_ClutchFault_00035cd0, uVar1 == 1)) {
      bVar3 = bVar3 | 1;
    }
    *PTR_CAN231_WorkingDiscreteByte_00035cd4 = bVar3;
  }
  return uVar1;
}

