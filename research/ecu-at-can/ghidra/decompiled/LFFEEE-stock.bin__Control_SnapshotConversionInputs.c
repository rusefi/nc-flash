/* Ghidra analysis output; verify against original SH instructions. */

/* Protected6DB4*1 toA5A0;72F8 toA5A4;6D00 toA5A8. Called byA477E. */

void Control_SnapshotConversionInputs(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  float fVar4;
  float fVar5;
  
  puVar1 = PTR_DAT_000a6224;
  fVar5 = 1.0;
  fVar4 = (float)(*(code *)PTR_FUN_000a622c)(PTR_DAT_000a6228);
  puVar3 = PTR_Control_NormalCommandOffset_000a6234;
  puVar2 = PTR_DAT_000a6230;
  *(float *)puVar1 = fVar4 * fVar5;
  *(float *)(puVar1 + 4) = *(float *)puVar2 * fVar5;
  *(float *)(puVar1 + 8) = *(float *)puVar3 * fVar5;
  return;
}

