/* Ghidra analysis output; verify against original SH instructions. */

/* Builds five12-byte constant unsigned word curves at9C14+12*i:
   [count2,shift0,x0,x65535,value,value].125 arbitrary-word cases include signed-boundary/FFFF
   preservation. */

void Selection_BuildClassLimitCurves(void)

{
  undefined2 uVar1;
  undefined *puVar2;
  undefined2 *puVar3;
  undefined2 *puVar4;
  undefined2 *puVar5;
  undefined2 local_10 [4];
  undefined2 uStack_8;
  
  puVar2 = PTR_DAT_00047330;
  puVar4 = local_10;
  local_10[0] = *(undefined2 *)PTR_DAT_0004730c;
  local_10[1] = *(undefined2 *)PTR_DAT_00047314;
  local_10[2] = *(undefined2 *)PTR_DAT_0004731c;
  local_10[3] = *(undefined2 *)PTR_DAT_00047324;
  uStack_8 = *(undefined2 *)PTR_DAT_0004732c;
  puVar3 = (undefined2 *)(int)DAT_00047302;
  puVar5 = puVar3 + 0x1e;
  for (; puVar3 < puVar5; puVar3 = puVar3 + 6) {
    *puVar3 = 2;
    puVar3[1] = 0;
    puVar3[2] = 0;
    puVar3[3] = (short)puVar2;
    puVar3[4] = *puVar4;
    uVar1 = *puVar4;
    puVar4 = puVar4 + 1;
    puVar3[5] = uVar1;
  }
  return;
}

