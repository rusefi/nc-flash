/* Ghidra analysis output; verify against original SH instructions. */

/* Executed rawFFFF retains old value with validity1; otherwise floor(raw/4) ->8814, validity2.
   Complete201 dispatch audit reads only0/1/6 in tested cases. */

void CAN201_ConvertWord0(void)

{
  undefined *puVar1;
  uint uVar2;
  undefined *puVar3;
  undefined2 uVar4;
  undefined1 uVar5;
  
  uVar2 = (*(code *)PTR_CAN201_GetWord0_0001721c)();
  puVar1 = PTR_DAT_00017220;
  uVar4 = *(undefined2 *)PTR_CAN201_Word0Quarter_00017214;
  uVar5 = 1;
  if ((undefined *)(uVar2 & 0xffff) != PTR_DAT_00017220) {
    puVar3 = (undefined *)(*(code *)PTR_FUN_0001722c)(uVar2,PTR_DAT_00017228,PTR_DAT_00017224);
    if ((int)puVar1 < (int)puVar3) {
      puVar3 = puVar1;
    }
    if ((int)puVar3 < 0) {
      puVar3 = (undefined *)0x0;
    }
    uVar4 = SUB42(puVar3,0);
    uVar5 = 2;
  }
  puVar1 = PTR_DAT_00017218;
  *(undefined2 *)PTR_CAN201_Word0Quarter_00017214 = uVar4;
  *puVar1 = uVar5;
  return;
}

