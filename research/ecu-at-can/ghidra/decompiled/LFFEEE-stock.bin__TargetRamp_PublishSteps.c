/* Ghidra analysis output; verify against original SH instructions. */

/* 67CCexact1 OR7247exact1 chooses stock0.03 up/down; else0.2.6956exact1 selectsDB230 vsDB228
   (equalstockvalues); actualbranchPCobserved.154B0rawbyte getter,not protected. */

char TargetRamp_PublishSteps(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  undefined4 uVar4;
  
  puVar2 = PTR_FUN_00033c7c;
  puVar1 = PTR_TargetRamp_FallStep_00033c60;
  if ((*PTR_DAT_00033c64 == '\x01') || (*PTR_DAT_00033c68 == '\x01')) {
    cVar3 = '\x01';
    *(undefined4 *)PTR_TargetRamp_RiseStep_00033c5c = *(undefined4 *)PTR_DAT_00033c6c;
    *(undefined4 *)puVar1 = *(undefined4 *)PTR_DAT_00033c70;
  }
  else {
    *(undefined4 *)PTR_TargetRamp_RiseStep_00033c5c = *(undefined4 *)PTR_DAT_00033c74;
    cVar3 = (*(code *)puVar2)(PTR_TargetRamp_FallSelector_00033c78);
    if (cVar3 == '\x01') {
      uVar4 = *(undefined4 *)PTR_DAT_00033c80;
    }
    else {
      uVar4 = *(undefined4 *)PTR_DAT_00033c84;
    }
    *(undefined4 *)puVar1 = uVar4;
  }
  return cVar3;
}

