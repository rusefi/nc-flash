/* Ghidra analysis output; verify against original SH instructions. */

/* Executed with explicit peripheral samples: PGDR bit0 strobe, TDR write, unbounded SSR bit40 poll,
   RDR read, strobe release. Not a full peripheral model. */

int Input_TransferSerialByte(undefined1 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  int iVar4;
  byte *pbVar5;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  char cStack_1c;
  
  puVar3 = PTR_FUN_00007948;
  cStack_1c = param_1;
  (*(code *)PTR_FUN_00007948)();
  (*(code *)PTR_Register_UpdateMaskedWord_00007934)((int)DAT_0000791e,1,0);
  (*(code *)puVar3)();
  puVar1 = PTR_FUN_0000792c;
  iVar4 = (int)DAT_0000790e;
  (*(code *)PTR_FUN_0000792c)(&local_20,iVar4);
  pbVar5 = (byte *)(int)DAT_00007920;
  *pbVar5 = *pbVar5 & 0x87 | 0x80;
  puVar2 = PTR_FUN_00007930;
  (*(code *)PTR_FUN_00007930)(local_20);
  (*(code *)puVar1)(&local_24,iVar4);
  *(char *)(int)DAT_00007922 = cStack_1c;
  *pbVar5 = *pbVar5 & 0x7f | 0x78;
  (*(code *)puVar2)(local_24);
  do {
  } while ((*pbVar5 & 0x40) == 0);
  (*(code *)puVar1)(&local_28,iVar4);
  cStack_1c = *(char *)(int)DAT_00007924;
  *pbVar5 = *pbVar5 & 0xbf | 0xb8;
  (*(code *)puVar2)(local_28);
  (*(code *)puVar3)();
  (*(code *)PTR_Register_UpdateMaskedWord_00007934)((int)DAT_0000791e,1);
  return (int)cStack_1c;
}

