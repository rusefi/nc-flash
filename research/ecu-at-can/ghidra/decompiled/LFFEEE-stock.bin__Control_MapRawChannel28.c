/* Ghidra analysis output; verify against original SH instructions. */

/* 4040 ->filter2534 DC490=256 ->40F8 ->unsigned*5/65536 ->lookupA3A30 ->40F4. Board identity open.
   See control-raw-provenance.txt. */

void Control_MapRawChannel28(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined2 uVar3;
  undefined4 uVar4;
  
  puVar1 = PTR_DAT_00007094;
  uVar3 = (*(code *)PTR_FUN_0000709c)
                    (*(undefined2 *)PTR_DAT_00007090,*(undefined2 *)PTR_DAT_00007094,
                     (int)*(short *)PTR_DAT_00007098);
  puVar2 = PTR_FUN_000070a4;
  *(undefined2 *)puVar1 = uVar3;
  uVar4 = (*(code *)puVar2)(DAT_000070a0,0,(int)*(short *)puVar1);
  uVar4 = (*(code *)PTR_Lookup_FloatCurve_000070ac)(uVar4,PTR_DAT_000070a8);
  *DAT_000070b0 = uVar4;
  return;
}

