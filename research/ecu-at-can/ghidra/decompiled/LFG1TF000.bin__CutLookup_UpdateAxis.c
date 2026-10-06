/* Ghidra analysis output; verify against original SH instructions. */

/* 89A8<<7 or92C6bit6 substitute76DF4=10240 ->lowword80F2/9336;9334=2*(signedlowword+5120)
   modulo65536.30 source/fault cases ->lookup/cut/ECU commands. */

void CutLookup_UpdateAxis(void)

{
  undefined *puVar1;
  undefined2 uVar2;
  
  puVar1 = PTR_FUN_00022f24;
  DAT_ffff80f2 = *(short *)PTR_CutLookup_SourceValue_00022f14 << 7;
  if ((*PTR_ApplicationFaultFlags92C6_00022f18 & 0x40) != 0) {
    DAT_ffff80f2 = *(short *)PTR_DAT_00022f1c;
  }
  *(short *)PTR_CutLookup_Axis_00022f20 = (DAT_ffff80f2 + DAT_00022f10) * 2;
  (*(code *)puVar1)();
  uVar2 = (*(code *)PTR_FUN_00022f28)();
  *(undefined2 *)PTR_DAT_00022f2c = uVar2;
  return;
}

