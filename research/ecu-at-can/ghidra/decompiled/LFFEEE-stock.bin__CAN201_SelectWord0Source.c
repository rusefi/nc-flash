/* Ghidra analysis output; verify against original SH instructions. */

/* 6DB4 ->6B34; direct-copy path6536=0 executed in11 round-trip cases. Alternate smoothing gates are
   not newly tested. */

uint CAN201_SelectWord0Source(void)

{
  undefined *puVar1;
  char cVar3;
  uint uVar2;
  byte bVar4;
  float fVar5;
  undefined4 extraout_fr0;
  float fVar6;
  
  fVar5 = (float)(*(code *)PTR_FUN_000367fc)(PTR_DAT_000367f8);
  fVar6 = *(float *)PTR_DAT_00036804 + *(float *)PTR_DAT_00036800;
  cVar3 = (*(code *)PTR_FUN_0003680c)(PTR_DAT_00036808);
  puVar1 = PTR_DAT_0003681c;
  bVar4 = *PTR_DAT_00036810;
  if ((((*PTR_DAT_00036814 == '\x01') && (cVar3 == '\x01')) && (*PTR_DAT_00036818 == '\0')) &&
     (fVar5 < fVar6)) {
    bVar4 = 1;
  }
  uVar2 = (uint)bVar4;
  if (uVar2 == 1) {
    uVar2 = (*(code *)PTR_FUN_00036828)
                      (fVar5,*(undefined4 *)PTR_DAT_0003681c,*(undefined4 *)PTR_DAT_00036824,
                       DAT_00036820);
    *(undefined4 *)puVar1 = extraout_fr0;
  }
  else {
    *(float *)PTR_DAT_0003681c = fVar5;
  }
  if ((cVar3 == '\0') && (*(float *)PTR_DAT_0003681c <= fVar5)) {
    bVar4 = 0;
  }
  *PTR_DAT_00036810 = bVar4;
  return uVar2;
}

