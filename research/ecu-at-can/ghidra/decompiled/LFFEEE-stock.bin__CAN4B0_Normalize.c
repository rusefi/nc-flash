/* Ghidra analysis output; verify against original SH instructions. */

/* Copies words; FFFF invalid flags6B01/02 only when7353=1; aggregate6B03 includes receipt
   fault6B00. */

void CAN4B0_Normalize(void)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  
  puVar4 = PTR_DAT_00035f34;
  puVar3 = PTR_DAT_00035f30;
  puVar2 = PTR_DAT_00035f28;
  cVar1 = *PTR_CAN4B0_SelectionEnabled_00035f24;
  *(undefined2 *)PTR_DAT_00035f28 = *(undefined2 *)PTR_DAT_00035f2c;
  *(undefined2 *)puVar3 = *(undefined2 *)puVar4;
  puVar4 = PTR_CAN4B0_Word4Invalid_00035f38;
  if ((*(ushort *)puVar2 == DAT_00035f3c) && (cVar1 == '\x01')) {
    *PTR_CAN4B0_Word4Invalid_00035f38 = 1;
  }
  else {
    *PTR_CAN4B0_Word4Invalid_00035f38 = 0;
  }
  if ((*(ushort *)puVar3 == DAT_00035ff8) && (cVar1 == '\x01')) {
    *PTR_CAN4B0_Word6Invalid_00035ffc = 1;
  }
  else {
    *PTR_CAN4B0_Word6Invalid_00035ffc = 0;
  }
  if (((*puVar4 == '\x01') && (*PTR_CAN4B0_Word6Invalid_00035ffc == '\x01')) ||
     ((*PTR_DAT_00036000 == '\x01' && (cVar1 == '\x01')))) {
    *PTR_CAN4B0_AggregateInvalid_00036004 = 1;
  }
  else {
    *PTR_CAN4B0_AggregateInvalid_00036004 = 0;
  }
  puVar4 = PTR_CAN4B0_WorkingWord6_0003600c;
  *(undefined2 *)PTR_CAN4B0_WorkingWord4_00036008 = *(undefined2 *)puVar2;
  *(undefined2 *)puVar4 = *(undefined2 *)puVar3;
  return;
}

