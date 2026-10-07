/* Ghidra analysis output; verify against original SH instructions. */

/* 6810=clamp((6DB4-500)/300,1,1) in stock finite cases; alwaysone.32cases, stock constants only. */

uint Control_ProduceInputLimitFactor(void)

{
  undefined *puVar1;
  uint uVar2;
  float fVar3;
  undefined4 extraout_fr0;
  
  puVar1 = PTR_DAT_000314ec;
  uVar2 = (*(code *)PTR_FUN_000314d4)
                    (*(undefined4 *)PTR_DAT_000314f0,*(undefined4 *)PTR_DAT_000314ec,DAT_000314cc);
  if ((uVar2 & 0xff) != 0) {
    fVar3 = (float)(*(code *)PTR_FUN_00031494)(PTR_DAT_000314d8);
    uVar2 = (*(code *)PTR_FUN_00031478)
                      ((fVar3 - *(float *)puVar1) / (*(float *)PTR_DAT_000314f0 - *(float *)puVar1),
                       *(undefined4 *)PTR_DAT_000314f4,0x3f800000);
    *(undefined4 *)PTR_Control_InputLimitFactor_000314ac = extraout_fr0;
  }
  return uVar2;
}

