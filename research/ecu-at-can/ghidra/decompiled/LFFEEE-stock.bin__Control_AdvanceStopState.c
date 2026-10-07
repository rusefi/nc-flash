/* Ghidra analysis output; verify against original SH instructions. */

/* Executed900 corestateoracles:735Cexact1/state0 resets; absenthold state0 uses8-callwarmup;
   activestateage incrementsaturated,at72000 or>=8 withbothpairscaughtup entersF8D6.
   Reassertedholdwithactivestate routesF972. Terminalcasesstopatentry,notcompletereturns.
   AA590auxeffectsoutsidecoreoracle. control-task-stop.txt. */

void Control_AdvanceStopState(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined4 uVar4;
  uint uVar5;
  
  uVar4 = (*(code *)PTR_FUN_0002c64c)(0x10);
  puVar3 = PTR_DAT_0002c67c;
  puVar2 = PTR_DAT_0002c664;
  puVar1 = PTR_Control_StopState_0002c638;
  if (*PTR_Control_ModeHoldFlag_0002c668 == '\x01') {
    if (*PTR_Control_StopState_0002c638 == '\0') {
      *PTR_DAT_0002c66c = 0x5a;
      *(undefined2 *)puVar2 = 0;
      *PTR_DAT_0002c63c = 1;
    }
    else {
      (*(code *)PTR_FUN_0002c644)(PTR_DAT_0002c640,0);
      (*(code *)PTR_FUN_0002c670)();
      (*(code *)PTR_FUN_0002c674)();
      (*(code *)PTR_FUN_0002c678)();
    }
  }
  else if (*PTR_Control_StopState_0002c638 == '\0') {
    if (*(ushort *)PTR_DAT_0002c680 <= *(ushort *)PTR_DAT_0002c664) {
      *PTR_Control_StopState_0002c638 = 1;
      *(undefined4 *)puVar3 = 0;
      *PTR_DAT_0002c684 = 1;
    }
    *(short *)puVar2 = *(short *)puVar2 + 1;
  }
  else {
    if (*(int *)PTR_DAT_0002c67c != -1) {
      *(int *)PTR_DAT_0002c67c = *(int *)PTR_DAT_0002c67c + 1;
    }
    uVar5 = *(uint *)puVar3;
    if ((*(uint *)PTR_DAT_0002c688 <= uVar5) ||
       (((7 < uVar5 && ((byte)*PTR_DAT_0002c650 <= (byte)*PTR_DAT_0002c65c)) &&
        ((byte)*PTR_DAT_0002c658 <= (byte)*PTR_DAT_0002c660)))) {
      (*(code *)PTR_FUN_0002c674)();
      puVar2 = PTR_DAT_0002c640;
      *puVar1 = 2;
      (*(code *)PTR_FUN_0002c644)(puVar2,1);
      puVar1 = PTR_DAT_0002c66c;
      *PTR_DAT_0002c63c = 0;
      puVar2 = PTR_FUN_0002c68c;
      *puVar1 = 0;
      (*(code *)puVar2)();
    }
  }
  (*(code *)PTR_FUN_0002c654)(uVar4);
  return;
}

