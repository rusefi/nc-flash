/* Ghidra analysis output; verify against original SH instructions. */

/* 8ACA/8ACC MOV.W signextend thenunsigned32comparison gates eight-slot5C5EC dispatch; phases0..3
   gain,4..7 offset. Old8AD0>3000 sets interval15/errorbounds+-5. Counterswrap16bit.1728 cases/3040
   retainedcalls; no physicaltimeclaim. */

void OutputAdaptation_Dispatch(void)

{
  byte bVar1;
  ushort *puVar2;
  int iVar3;
  ushort *puVar4;
  byte *pbVar5;
  
  puVar4 = (ushort *)(int)DAT_00018880;
  if (*(ushort *)(int)DAT_00018882 < *puVar4) {
    pbVar5 = (byte *)(int)DAT_00018884;
    *puVar4 = 0;
    bVar1 = *pbVar5;
    iVar3 = (int)(char)bVar1;
    if (3 < bVar1) {
      iVar3 = DAT_00018888 + iVar3;
    }
    if (*(int *)(PTR_PTR_000189c0 + (uint)bVar1 * 4) != 0) {
      (**(code **)(PTR_PTR_000189c0 + (uint)bVar1 * 4))(iVar3);
    }
    *pbVar5 = *pbVar5 + 1;
    if (7 < *pbVar5) {
      *pbVar5 = 0;
    }
  }
  puVar2 = (ushort *)(int)DAT_000189a6;
  if ((int)DAT_000189a8 < (int)(uint)*puVar2) {
    *(undefined2 *)(int)DAT_000189aa = 0xf;
    *(undefined2 *)(int)DAT_000189ac = 5;
    *(undefined2 *)(int)DAT_000189ae = 0xfffb;
  }
  *puVar2 = *puVar2 + 1;
  *puVar4 = *puVar4 + 1;
  return;
}

