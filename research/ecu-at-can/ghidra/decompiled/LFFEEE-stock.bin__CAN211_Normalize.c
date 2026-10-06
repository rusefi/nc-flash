/* Ghidra analysis output; verify against original SH instructions. */

/* BE word0 to6A1C while fresh, elseFFFF; word4 validity/request flag pairs suppressed by69E1. 2048
   synthetic cases. */

undefined * CAN211_Normalize(void)

{
  char cVar1;
  ushort uVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined2 uVar6;
  
  puVar5 = PTR_DAT_00034a54;
  puVar4 = PTR_DAT_00034a50;
  puVar3 = PTR_DAT_00034a3c;
  *(undefined2 *)PTR_DAT_00034a3c = *(undefined2 *)PTR_DAT_00034a40;
  *(undefined2 *)puVar4 = *(undefined2 *)puVar5;
  puVar5 = PTR_CAN_OtherReceiptFault_00034a58;
  cVar1 = *PTR_CAN_OtherReceiptFault_00034a58;
  if (*PTR_DAT_00034a24 == '\0') {
    uVar6 = (undefined2)DAT_00034a5c;
  }
  else {
    uVar6 = *(undefined2 *)puVar3;
  }
  *(undefined2 *)PTR_CAN211_FreshWord0_00034a44 = uVar6;
  uVar2 = *(ushort *)puVar4;
  if ((uVar2 & DAT_00034a0e) == 0) {
    *PTR_DAT_00034b3c = 0;
  }
  else {
    *PTR_DAT_00034a60 = 1;
  }
  if (((((uVar2 & DAT_00034b36) == 0) || (cVar1 != '\0')) || (*PTR_DAT_00034b3c != '\0')) ||
     (puVar5 = (undefined *)(uint)(byte)*PTR_DAT_00034b40, puVar5 != (undefined *)0x1)) {
    *PTR_DAT_00034b44 = 0;
  }
  else {
    *PTR_DAT_00034b44 = 1;
  }
  if ((uVar2 & DAT_00034b38) == 0) {
    *PTR_DAT_00034b48 = 0;
  }
  else {
    *PTR_DAT_00034b48 = 1;
  }
  puVar3 = PTR_DAT_00034b4c;
  if ((((uVar2 & DAT_00034b3a) == 0) || (cVar1 != '\0')) || (*PTR_DAT_00034b48 != '\0')) {
    *PTR_DAT_00034b4c = 0;
  }
  else {
    *PTR_DAT_00034b4c = 1;
    puVar5 = puVar3;
  }
  if ((uVar2 & 0x10) == 0) {
    *PTR_DAT_00034b50 = 0;
  }
  else {
    *PTR_DAT_00034b50 = 1;
  }
  puVar3 = PTR_DAT_00034b54;
  if ((((uVar2 & 0x20) == 0) || (cVar1 != '\0')) || (*PTR_DAT_00034b50 != '\0')) {
    *PTR_DAT_00034b54 = 0;
  }
  else {
    *PTR_DAT_00034b54 = 1;
    puVar5 = puVar3;
  }
  if ((uVar2 & 1) == 0) {
    *PTR_DAT_00034b58 = 0;
  }
  else {
    *PTR_DAT_00034b58 = 1;
  }
  puVar3 = PTR_DAT_00034b5c;
  if ((((uVar2 & 4) == 0) || (cVar1 != '\0')) || (*PTR_DAT_00034b58 != '\0')) {
    *PTR_DAT_00034bd8 = 0;
  }
  else {
    *PTR_DAT_00034b5c = 1;
    puVar5 = puVar3;
  }
  if ((((uVar2 & 2) == 0) || (cVar1 != '\0')) || (*PTR_DAT_00034bdc != '\0')) {
    *PTR_DAT_00034be0 = 0;
  }
  else {
    *PTR_DAT_00034be0 = 1;
  }
  return puVar5;
}

