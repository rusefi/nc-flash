/* Ghidra analysis output; verify against original SH instructions. */

/* Copies two caller bytes tostack, calls46DB6/46D34/46DE4/46CC8/46D30/46A34/46B00, writesfinal
   pairback. Verified within720 complete452DC fixtures. Other branch controls explicitlyzero. */

int Selection_ApplySevenRules(char *param_1,undefined1 *param_2)

{
  undefined1 auStack_14 [4];
  char acStack_10 [4];
  undefined1 *puStack_c;
  char *pcStack_8;
  
  acStack_10[0] = *param_1;
  auStack_14[0] = *param_2;
  puStack_c = param_2;
  pcStack_8 = param_1;
  (*(code *)PTR_FUN_0004669c)(acStack_10,auStack_14);
  (*(code *)PTR_FUN_000466a0)(acStack_10,auStack_14);
  (*(code *)PTR_FUN_000466a4)(acStack_10,auStack_14);
  (*(code *)PTR_Selection_ApplyChangeDependentFloor_000466a8)(acStack_10,auStack_14);
  (*(code *)PTR_FUN_000466ac)(acStack_10,auStack_14);
  (*(code *)PTR_FUN_000466b0)(acStack_10,auStack_14);
  (*(code *)PTR_FUN_000466b4)(acStack_10,auStack_14);
  *pcStack_8 = acStack_10[0];
  *puStack_c = auStack_14[0];
  return (int)acStack_10[0];
}

