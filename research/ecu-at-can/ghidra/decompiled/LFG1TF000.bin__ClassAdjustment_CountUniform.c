/* Ghidra analysis output; verify against original SH instructions. */

/* Nonzero9870 andu16(985A)<65535 increments985A and writes24562 cacheindex3/6170. Saturates65535.
   Originalgetter371EA executes. */

void ClassAdjustment_CountUniform(void)

{
  undefined *puVar1;
  char cVar2;
  ushort *puVar3;
  
  cVar2 = (*(code *)PTR_FUN_000368f0)();
  puVar1 = PTR_StoredWord_WriteIndexedValue_000368f8;
  if ((cVar2 != '\0') &&
     (puVar3 = (ushort *)(int)DAT_000368de, (int)(uint)*puVar3 < (int)PTR_DAT_000368f4)) {
    *puVar3 = *puVar3 + 1;
    (*(code *)puVar1)(3,(int)(short)*puVar3);
  }
  return;
}

