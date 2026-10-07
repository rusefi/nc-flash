/* Ghidra analysis output; verify against original SH instructions. */

/* 7016exact1 clears6910;else73C4bit7 reloads wordcurveA37D4(6D20),else
   saturatingdecrement.3904direct and802retainedcalls; stockaxis80reload800. Earliercaller18770;
   nohardwareperiod claim. */

int ControlInput_UpdateLimitCountdown(void)

{
  undefined *puVar1;
  char cVar3;
  int iVar2;
  undefined4 uVar4;
  
  puVar1 = PTR_ControlInput_LimitCountdown_000318c8;
  cVar3 = (*(code *)PTR_FUN_000318d0)(PTR_DAT_000318cc);
  if (cVar3 == '\x01') {
    *(undefined2 *)puVar1 = 0;
    iVar2 = 1;
  }
  else {
    iVar2 = -((((int)(char)*PTR_DAT_000318d4 & 0x80U) == 0) - 1);
    if (iVar2 == 1) {
      uVar4 = (*(code *)PTR_FUN_00031878)(PTR_Control_RawFirstPublished_00031874);
      iVar2 = (*(code *)PTR_FUN_000318dc)(uVar4,PTR_PTR_000318d8);
      *(short *)puVar1 = (short)iVar2;
    }
    else if (*(short *)puVar1 != 0) {
      *(short *)puVar1 = *(short *)puVar1 + (short)DAT_000318e0;
    }
  }
  return iVar2;
}

