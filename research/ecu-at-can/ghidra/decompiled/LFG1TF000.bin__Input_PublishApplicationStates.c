/* Ghidra analysis output; verify against original SH instructions. */

/* Copies channels0..8 to FFFF88B4..BC; computes88BD aggregate status. First four feed CAN231
   selector flags. */

void Input_PublishApplicationStates(void)

{
  bool bVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined1 uVar4;
  char cVar5;
  undefined1 uVar6;
  uint uVar7;
  
  puVar2 = PTR_Input_GetFilteredState_00017590;
  uVar4 = (*(code *)PTR_Input_GetFilteredState_00017590)(0);
  *PTR_Selector_FilteredInputZero_00017548 = uVar4;
  uVar4 = (*(code *)puVar2)(1);
  *PTR_DAT_00017550 = uVar4;
  uVar4 = (*(code *)puVar2)(2);
  *PTR_Selector_FilteredInputTwo_00017558 = uVar4;
  uVar4 = (*(code *)puVar2)(3);
  *PTR_DAT_00017560 = uVar4;
  uVar4 = (*(code *)puVar2)(4);
  *PTR_DAT_00017568 = uVar4;
  uVar4 = (*(code *)puVar2)(5);
  *PTR_DAT_00017570 = uVar4;
  uVar4 = (*(code *)puVar2)(6);
  *PTR_DAT_00017578 = uVar4;
  uVar4 = (*(code *)puVar2)(7);
  *PTR_DAT_00017580 = uVar4;
  uVar4 = (*(code *)puVar2)(8);
  puVar3 = PTR_FUN_00017598;
  puVar2 = PTR_DAT_00017594;
  uVar6 = 3;
  bVar1 = true;
  *PTR_DAT_00017588 = uVar4;
  uVar7 = 0;
  while ((uVar7 < 9 && (bVar1))) {
    cVar5 = (*(code *)puVar3)((int)(char)puVar2[uVar7]);
    uVar7 = uVar7 + 1;
    if (cVar5 != '\x02') {
      bVar1 = false;
    }
  }
  if (bVar1) {
    uVar6 = 2;
  }
  *PTR_DAT_0001758c = uVar6;
  return;
}

