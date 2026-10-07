/* Ghidra analysis output; verify against original SH instructions. */

/* 8EF8 zero copies40F4 to protected6D20/6D28;6565 exact1 floors6D38 at90. Nonzero8EF8
   selects40/80/80.7016 zero snapshots6D20 into protected6D30; else retains.576 cases plus320
   retained cycles; physical units open. */

uint Control_PublishRawFirstInput(void)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  undefined4 uVar4;
  
  puVar2 = PTR_FUN_00039f14;
  puVar1 = PTR_FUN_00039f10;
  if (*PTR_DAT_00039f18 == '\0') {
    uVar4 = *(undefined4 *)PTR_DAT_00039f1c;
    (*(code *)PTR_FUN_00039f10)(uVar4,PTR_Control_RawFirstPublished_00039f20);
    (*(code *)puVar1)(uVar4,PTR_Control_RawFirstAlternate_00039f24);
    if (*PTR_DAT_00039f28 == '\x01') {
      uVar4 = (*(code *)puVar2)(PTR_Control_RawFirstPublished_00039f20);
      uVar4 = (*(code *)PTR_FUN_00039f30)(uVar4,*(undefined4 *)PTR_DAT_00039f2c);
    }
    else {
      uVar4 = (*(code *)puVar2)(PTR_Control_RawFirstPublished_00039f20);
    }
  }
  else {
    (*(code *)PTR_FUN_00039f10)
              (*(undefined4 *)PTR_DAT_00039f34,PTR_Control_RawFirstPublished_00039f20);
    (*(code *)puVar1)(*(undefined4 *)PTR_DAT_00039f38,PTR_Control_RawFirstAlternate_00039f24);
    uVar4 = *(undefined4 *)PTR_DAT_00039f38;
  }
  (*(code *)puVar1)(uVar4,PTR_Control_RawFirstFloored_00039f3c);
  uVar3 = (*(code *)PTR_FUN_00039f44)(PTR_DAT_00039f40);
  uVar3 = uVar3 & 0xff;
  if (uVar3 == 0) {
    uVar4 = (*(code *)puVar2)(PTR_Control_RawFirstPublished_00039f20);
    uVar3 = (*(code *)puVar1)(uVar4,PTR_Control_RawFirstSnapshot_00039f0c);
  }
  return uVar3;
}

