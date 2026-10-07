/* Ghidra analysis output; verify against original SH instructions. */

/* 4042 ->filter2534 DC474=256 ->40E4 -> unsigned*5/65536 ->lookupA3A24 ->40E0.2228 combined scale
   checks; board identity open. See control-raw-provenance.txt. */

void Control_MapRawChannel29(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined2 uVar3;
  undefined4 uVar4;
  
  puVar1 = PTR_DAT_000066e8;
  uVar3 = (*(code *)PTR_FUN_000066f0)
                    (*(undefined2 *)PTR_DAT_000066e4,*(undefined2 *)PTR_DAT_000066e8,
                     (int)*(short *)PTR_DAT_000066ec);
  puVar2 = PTR_FUN_000066f8;
  *(undefined2 *)puVar1 = uVar3;
  uVar4 = (*(code *)puVar2)(DAT_000066f4,0,(int)*(short *)puVar1);
  uVar4 = (*(code *)PTR_Lookup_FloatCurve_00006700)(uVar4,PTR_DAT_000066fc);
  *DAT_00006704 = uVar4;
  return;
}

