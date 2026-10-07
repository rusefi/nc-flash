/* Ghidra analysis output; verify against original SH instructions. */

/* If88C4==1 and88C5==2: CAN4EC byte2 FF retainsold89B0/status1; otherwise raw*5, maxwith8808
   onlywhen880A==2, status2. Withoutadmission usesvalidCAN201 orhold/status880A.9216 cases. */

void Comparison_SelectCANSource(void)

{
  char cVar1;
  ushort uVar2;
  undefined *puVar3;
  ushort uVar4;
  char cVar5;
  
  uVar2 = *(ushort *)PTR_CAN201_Byte6Scaled_00017f04;
  cVar1 = *PTR_CAN201_Byte6Validity_00017f08;
  uVar4 = *(ushort *)PTR_Comparison_SelectedCANValue_00017efc;
  if ((*PTR_CAN4EC_ComparisonEnable_00017f0c == '\x01') &&
     (*PTR_CAN4EC_ComparisonEnableStatus_00017f10 == '\x02')) {
    cVar5 = '\x01';
    if ((uint)(byte)*PTR_DAT_00017f14 != (int)DAT_00017ef4) {
      puVar3 = (undefined *)
               (*(code *)PTR_FUN_00017f20)
                         ((uint)(byte)*PTR_DAT_00017f14,PTR_Comparison_CAN4ECInputScale_00017f1c,
                          PTR_Comparison_SelectedOutputScale_00017f18);
      if ((int)PTR_DAT_00017f24 < (int)puVar3) {
        puVar3 = PTR_DAT_00017f24;
      }
      if ((int)puVar3 < 0) {
        puVar3 = (undefined *)0x0;
      }
      if (((int)puVar3 < (int)(uint)uVar2) && (cVar1 == '\x02')) {
        puVar3 = (undefined *)(uint)uVar2;
      }
      cVar5 = '\x02';
      uVar4 = (ushort)puVar3;
    }
  }
  else {
    cVar5 = cVar1;
    if (cVar1 == '\x02') {
      uVar4 = uVar2;
    }
  }
  *(ushort *)PTR_Comparison_SelectedCANValue_00017efc = uVar4;
  *PTR_Comparison_SelectedCANStatus_00017f00 = cVar5;
  return;
}

