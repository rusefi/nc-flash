/* Ghidra analysis output; verify against original SH instructions. */

/* 735A bit7 selectsD9E8C~0.2;else6536zero selects8010;elsemin(23819,max(protected2310
   default0,8018)). Fullbody720 input cases; control-sources.txt. */

int Control_SelectOverrideInput(void)

{
  undefined *puVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 extraout_fr0;
  
  puVar1 = PTR_Control_SelectedOverrideInput_0005820c;
  iVar2 = -((((int)(char)*PTR_DAT_00058210 & 0x80U) == 0) - 1);
  puVar3 = (undefined4 *)PTR_DAT_00058214;
  if ((iVar2 == 1) ||
     (puVar3 = (undefined4 *)PTR_Control_MappedOverrideInput_00058208, *PTR_DAT_00058218 == '\0')) {
    *(undefined4 *)PTR_Control_SelectedOverrideInput_0005820c = *puVar3;
  }
  else {
    uVar4 = (*(code *)PTR_FUN_0005821c)
                      (*(undefined4 *)PTR_DAT_000581f0,PTR_Control_RetainedSourceFloor_000581e8);
    uVar4 = (*(code *)PTR_FUN_00058224)(*(undefined4 *)PTR_Control_SourceRemainder_00058220,uVar4);
    iVar2 = (*DAT_0005822c)(uVar4,*(undefined4 *)PTR_DAT_00058228);
    *(undefined4 *)puVar1 = extraout_fr0;
  }
  return iVar2;
}

