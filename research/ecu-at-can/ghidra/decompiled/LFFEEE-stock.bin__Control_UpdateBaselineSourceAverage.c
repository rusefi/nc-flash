/* Ghidra analysis output; verify against original SH instructions. */

/* 73C4bit80 resets80D8=FFFF,80D4=0,80D0=6D20; otherwise while count>0 decrement,add6D20
   tosum,mean=sum/(65535-count). At0 holdsall. Original body plus512 retained updates;
   control-contributions.txt. */

uint Control_UpdateBaselineSourceAverage(void)

{
  undefined *puVar1;
  int iVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  uint uVar6;
  undefined4 extraout_fr0;
  float extraout_fr0_00;
  
  puVar5 = PTR_DAT_00059150;
  puVar4 = PTR_Control_BaselineAverageRemaining_0005914c;
  puVar3 = PTR_Control_BaselineAverageSum_00059148;
  iVar2 = DAT_00059144;
  puVar1 = PTR_FUN_00059120;
  uVar6 = -((((int)(char)*PTR_DAT_00059140 & 0x80U) == 0) - 1) & 0xff;
  if (uVar6 == 1) {
    *(short *)PTR_Control_BaselineAverageRemaining_0005914c = (short)DAT_00059144;
    puVar1 = PTR_FUN_00059120;
    *(undefined4 *)puVar3 = 0;
    uVar6 = (*(code *)puVar1)(puVar5);
    *(undefined4 *)PTR_Control_RetainedBaselineAverage_00059134 = extraout_fr0;
  }
  else if (*(short *)PTR_Control_BaselineAverageRemaining_0005914c != 0) {
    *(short *)PTR_Control_BaselineAverageRemaining_0005914c =
         *(short *)PTR_Control_BaselineAverageRemaining_0005914c + (short)DAT_00059144;
    uVar6 = (*(code *)puVar1)(PTR_DAT_00059150);
    *(float *)puVar3 = *(float *)puVar3 + extraout_fr0_00;
    *(float *)PTR_Control_RetainedBaselineAverage_00059134 =
         *(float *)puVar3 / (float)(int)(iVar2 - (uint)*(ushort *)puVar4);
  }
  return uVar6;
}

