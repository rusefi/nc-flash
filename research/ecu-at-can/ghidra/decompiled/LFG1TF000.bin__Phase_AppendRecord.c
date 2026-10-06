/* Ghidra analysis output; verify against original SH instructions. */

/* 16-entry ring95D4 stride15; low bytes of three parameters at+10..12; state+13/+14=0, first10
   bytes cleared, timer8380 slot initialized. Empty head0/15 tested; capacity remains open. */

void Phase_AppendRecord(undefined1 param_1,undefined1 param_2,undefined1 param_3)

{
  int iVar1;
  undefined *puVar2;
  undefined2 uVar3;
  int extraout_r2;
  int iVar4;
  int iVar5;
  ushort uVar6;
  
  puVar2 = PTR_Phase_RecordRing_00031fbc;
  if ((byte)PTR_Phase_RecordRing_00031fbc[DAT_00031fb6] < 0x10) {
    uVar6 = (ushort)(byte)PTR_Phase_RecordRing_00031fbc[DAT_00031fb8] +
            (ushort)(byte)PTR_Phase_RecordRing_00031fbc[DAT_00031fb6] + 0x10 & 0xf;
    iVar1 = (short)uVar6 * 0xf;
    PTR_Phase_RecordRing_00031fbc[iVar1 + 10] = param_1;
    puVar2[iVar1 + 0xb] = param_2;
    iVar4 = 0;
    puVar2[iVar1 + 0xc] = param_3;
    puVar2[iVar1 + 0xd] = 0;
    puVar2[iVar1 + 0xe] = 0;
    uVar3 = (*(code *)PTR_FUN_00031fc4)();
    *(undefined2 *)(PTR_Phase_InitialTimers_00031fc8 + extraout_r2) = uVar3;
    iVar5 = iVar4;
    do {
      puVar2[(short)iVar5 + iVar1] = (char)iVar4;
      iVar5 = iVar5 + 1;
    } while ((short)iVar5 < 10);
    (*(code *)PTR_FUN_00031fcc)(uVar6);
    puVar2[DAT_00031fb6] = puVar2[DAT_00031fb6] + '\x01';
  }
  return;
}

