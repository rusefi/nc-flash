/* Ghidra analysis output; verify against original SH instructions. */

/* Originalpolicybody executedforB4 via285AE. StockE1E00=00800000 selects9A43A inverse mode match.
   Otherindices notindependentlymodeled here. */

bool Diagnostic_CheckIndexedPolicyInhibit(uint param_1)

{
  int iVar1;
  uint uVar2;
  bool local_c;
  
  iVar1 = (param_1 & 0xffff) * 4;
  local_c = (*(uint *)PTR_DAT_0009a480 & *(uint *)(PTR_LAB_0009a484 + iVar1) & 0xffff) != 0;
  if ((!local_c) &&
     (uVar2 = FUN_0009a2d0(param_1 & 0xffff),
     ((uint)PTR_DAT_0009a488 & uVar2 & *(uint *)(PTR_LAB_0009a484 + iVar1)) != 0)) {
    local_c = true;
  }
  return local_c;
}

