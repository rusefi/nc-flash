/* Ghidra analysis output; verify against original SH instructions. */

/* Executed72FC clamp0..100 toprotected6CD4;A3A4==1 substitutes100.81 combinedconsumer
   cases;throttle-candidate.txt. */

void Control_PublishSelectedAuxiliaryValue(void)

{
  char cVar1;
  undefined4 uVar2;
  
  cVar1 = (*(code *)PTR_FUN_00039c9c)(PTR_DAT_00039c98);
  if (cVar1 == '\x01') {
    (*(code *)PTR_FUN_00039ca4)(*(undefined4 *)PTR_DAT_00039ca0,PTR_DAT_00039c48);
    return;
  }
  uVar2 = (*(code *)PTR_FUN_00039cb0)
                    (*(undefined4 *)PTR_Control_SelectedPublishedValue_00039cac,0,DAT_00039ca8);
  (*(code *)PTR_FUN_00039ca4)(uVar2,PTR_DAT_00039c48);
  return;
}

