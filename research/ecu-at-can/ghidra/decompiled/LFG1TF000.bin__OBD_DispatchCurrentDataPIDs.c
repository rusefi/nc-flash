/* Ghidra analysis output; verify against original SH instructions. */

/* Matches requested PIDs against13 eight-byte records5E778 and dispatches callback. PID01
   callback5434C. */

uint OBD_DispatchCurrentDataPIDs(int *param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  undefined1 *local_2c;
  int iStack_28;
  undefined2 uStack_24;
  
  puVar2 = PTR_DAT_00054300;
  puVar1 = PTR_FUN_000542fc;
  uVar5 = 0;
  uVar4 = 0;
  while ((uVar4 & 0xff) < (uint)*(ushort *)(param_1 + 2)) {
    local_2c = (undefined1 *)((uVar4 & 0xff) + *param_1);
    iStack_28 = (uVar5 & 0xffff) + param_1[1];
    uStack_24 = 1;
    uVar3 = (*(code *)puVar1)(*local_2c,puVar2,0xd,&local_2c);
    uVar4 = uVar4 + 1;
    if ((uVar3 & 0xffff) != 0) {
      uVar5 = uVar5 + uVar3;
    }
  }
  return uVar5;
}

