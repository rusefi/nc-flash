/* Ghidra analysis output; verify against original SH instructions. */

/* Originalmode722A updates5664/5666 and566A>=6;1458 casesplus2514serialcycles. Inmode0
   blockedstatusholdscounter,notclear;control-timers.txt. */

uint Control_UpdateModeTimers(void)

{
  undefined *puVar1;
  uint uVar2;
  char cVar4;
  undefined2 uVar3;
  
  uVar2 = (*(code *)PTR_FUN_0002485c)(PTR_DAT_00024858);
  puVar1 = PTR_Control_ModeZeroTimer_00024860;
  uVar2 = uVar2 & 0xff;
  if (uVar2 == 0) {
    cVar4 = (*(code *)PTR_FUN_0002485c)(PTR_Control_FeedbackOverrideEnabled_0002484c);
    if (((cVar4 == '\x01') || (*PTR_DAT_00024864 == '\x01')) ||
       ((*PTR_DAT_00024868 == '\0' && (*PTR_DAT_0002486c == '\0')))) {
      uVar3 = (*(code *)PTR_FUN_00024870)((int)*(short *)puVar1,1);
      *(undefined2 *)puVar1 = uVar3;
    }
  }
  else {
    *(undefined2 *)PTR_Control_ModeZeroTimer_00024860 = 0;
  }
  if ((uVar2 == 0) && (*(ushort *)PTR_DAT_00024878 <= *(ushort *)PTR_Control_ModeZeroTimer_00024860)
     ) {
    *PTR_Control_ModeZeroTimerEligible_00024874 = 1;
  }
  else {
    *PTR_Control_ModeZeroTimerEligible_00024874 = 0;
  }
  puVar1 = PTR_Control_ModeOneTimer_000249c4;
  if (uVar2 == 1) {
    uVar2 = (*(code *)PTR_FUN_000249c8)((int)*(short *)PTR_Control_ModeOneTimer_000249c4,1);
    *(short *)puVar1 = (short)uVar2;
  }
  else {
    *(undefined2 *)PTR_Control_ModeOneTimer_000249c4 = 0;
  }
  return uVar2;
}

