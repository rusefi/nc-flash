/* Ghidra analysis output; verify against original SH instructions. */

/* 8081 byte maps to three words96C8/CA/CC:0=000,1=100,2=101,3/4=111,other=110 where1=25600.256
   cases. Original startup1E15C calls48BC0 then32140; tcu-transition-progress.txt. */

byte TransitionProgress_InitializeFromAccepted(void)

{
  undefined *puVar1;
  byte bVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  undefined2 uVar5;
  
  puVar1 = PTR_TransitionProgress_AccumulatorB_0003223c;
  bVar2 = CAN231_SixStateSource;
  if (CAN231_SixStateSource == 0) {
    uVar3 = 0;
LAB_00032168:
    uVar4 = 0;
  }
  else {
    uVar3 = DAT_0003222e;
    if (CAN231_SixStateSource == 1) goto LAB_00032168;
    uVar5 = DAT_0003222e;
    if (CAN231_SixStateSource == 2) {
      uVar4 = 0;
      goto LAB_00032182;
    }
    uVar4 = DAT_0003222e;
    if ((CAN231_SixStateSource == 3) || (CAN231_SixStateSource == 4)) goto LAB_00032182;
  }
  uVar5 = 0;
LAB_00032182:
  *(undefined2 *)PTR_TransitionProgress_AccumulatorA_00032238 = uVar3;
  *(undefined2 *)puVar1 = uVar4;
  *(undefined2 *)PTR_TransitionProgress_AccumulatorC_00032240 = uVar5;
  return bVar2;
}

