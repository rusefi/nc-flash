/* Ghidra analysis output; verify against original SH instructions. */

/* Executed per-bit two-consistent-sample filter; serial bank1 feeds MT CAN231 bits2/1
   via411F0/412A2. CBC8 channel only sampled on4004 change. */

undefined4 Input_UpdateLocalFilters(void)

{
  char cVar1;
  ushort uVar2;
  undefined *puVar3;
  undefined *puVar4;
  byte bVar6;
  undefined4 uVar5;
  
  puVar3 = PTR_DAT_0000cb94;
  uVar2 = *(ushort *)(int)DAT_0000cb8c;
  *(ushort *)PTR_DAT_0000cb90 =
       (*(ushort *)PTR_DAT_0000cb94 | uVar2) & *(ushort *)PTR_DAT_0000cb90 |
       *(ushort *)PTR_DAT_0000cb94 & uVar2;
  *(ushort *)puVar3 = uVar2;
  puVar3 = PTR_DAT_0000cb9c;
  uVar2 = *(ushort *)(int)DAT_0000cb8e;
  *(ushort *)PTR_DAT_0000cb98 =
       (*(ushort *)PTR_DAT_0000cb9c | uVar2) & *(ushort *)PTR_DAT_0000cb98 |
       *(ushort *)PTR_DAT_0000cb9c & uVar2;
  *(ushort *)puVar3 = uVar2;
  bVar6 = (*(code *)PTR_Input_ReadSerialBank_0000cba0)(1);
  puVar3 = PTR_Input_PreviousSerialBankOne_0000cba8;
  *PTR_Input_FilteredSerialBankOne_0000cba4 =
       (*PTR_Input_PreviousSerialBankOne_0000cba8 | bVar6) &
       *PTR_Input_FilteredSerialBankOne_0000cba4 | *PTR_Input_PreviousSerialBankOne_0000cba8 & bVar6
  ;
  *puVar3 = bVar6;
  uVar5 = (*(code *)PTR_Input_ReadSerialBank_0000cba0)(2);
  puVar4 = PTR_DAT_0000cbc0;
  puVar3 = PTR_DAT_0000cbb0;
  bVar6 = (byte)uVar5;
  *PTR_DAT_0000cbac = (*PTR_DAT_0000cbb0 | bVar6) & *PTR_DAT_0000cbac | *PTR_DAT_0000cbb0 & bVar6;
  *puVar3 = bVar6;
  cVar1 = *puVar4;
  if (*PTR_DAT_0000cbc4 != cVar1) {
    uVar5 = (*(code *)PTR_Input_ReadThresholdBoolean_0000cbb4)();
    puVar3 = PTR_DAT_0000cbbc;
    uVar2 = (ushort)uVar5;
    *(ushort *)PTR_DAT_0000cbb8 =
         (*(ushort *)PTR_DAT_0000cbbc | uVar2) & *(ushort *)PTR_DAT_0000cbb8 |
         *(ushort *)PTR_DAT_0000cbbc & uVar2;
    *(ushort *)puVar3 = uVar2;
    *PTR_DAT_0000cbc4 = cVar1;
  }
  return uVar5;
}

