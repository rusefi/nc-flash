/* Ghidra analysis output; verify against original SH instructions. */

/* 9216cases/alllowbytes/ninehighmasks/fourchannels; acceptsnonbusyrecord, retainsbounds/offset,
   truncatesaccumulator/1000, signedwordclampsoutputA5DC. Busyrecordstillrecomputesoutput.
   tcu-output-service.txt. */

void OutputRecord_ServiceChannel(int param_1)

{
  undefined *puVar1;
  undefined2 uVar2;
  ushort *puVar3;
  ushort *puVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  
  puVar1 = PTR_DAT_00053190;
  iVar8 = param_1 * 2;
  puVar3 = (ushort *)(PTR_DAT_00053190 + iVar8);
  iVar5 = (int)DAT_0005317c;
  iVar6 = (int)DAT_0005317e;
  iVar7 = (int)DAT_00053180;
  if ((((uint)PTR_DAT_00053194 & (uint)*puVar3) == 0) && ((char)*puVar3 != '\0')) {
    if ((*(ushort *)(PTR_DAT_00053190 + iVar8) & 7) != 0) {
      uVar2 = (*(code *)PTR_FUN_000531a4)
                        ((int)*(short *)(PTR_DAT_000531a0 + iVar8),
                         (int)*(short *)(PTR_DAT_0005319c + iVar8),
                         (int)*(short *)(PTR_DAT_00053198 + iVar8));
      *(undefined2 *)(DAT_00053182 + iVar8) = uVar2;
    }
    if ((DAT_00053186 & *(ushort *)(puVar1 + iVar8)) == 0) {
      uVar2 = *(undefined2 *)(PTR_DAT_00053198 + iVar8);
      *(undefined2 *)(iVar8 + DAT_00053184) = uVar2;
      *(undefined2 *)(iVar8 + iVar7) = uVar2;
    }
    else if ((DAT_00053188 & *(ushort *)(puVar1 + iVar8)) != 0) {
      *(undefined2 *)(iVar7 + iVar8) = *(undefined2 *)(DAT_00053184 + iVar8);
    }
    if ((DAT_0005318c & *(ushort *)(puVar1 + iVar8)) == 0) {
      uVar2 = *(undefined2 *)(PTR_DAT_00053268 + iVar8);
      *(undefined2 *)(iVar8 + DAT_0005318a) = uVar2;
      *(undefined2 *)(iVar8 + iVar5) = uVar2;
    }
    else if ((DAT_0005318e & *(ushort *)(puVar1 + iVar8)) != 0) {
      *(undefined2 *)(iVar5 + iVar8) = *(undefined2 *)(DAT_0005318a + iVar8);
    }
    puVar4 = (ushort *)(puVar1 + iVar8);
    *puVar4 = *puVar4 & (ushort)PTR_DAT_0005326c;
    puVar3 = (ushort *)0x0;
    *(undefined2 *)(iVar6 + iVar8) = 0;
    if ((DAT_00053258 & *puVar4) == 0) {
      *(undefined2 *)(iVar8 + iVar6) =
           *(undefined2 *)(PTR_OutputRecord_ComputedWords_00053270 + iVar8);
    }
    if ((DAT_0005325a & *(ushort *)(puVar1 + iVar8)) == 0) {
      *(undefined4 *)(param_1 * 4 + (int)DAT_0005325c) = 0;
    }
  }
  iVar5 = (*(code *)PTR_FUN_00053274)
                    (puVar3,(int)*(short *)(iVar5 + iVar8),(int)*(short *)(iVar7 + iVar8));
  uVar2 = (*(code *)PTR_FUN_00053278)
                    (iVar5 + *(short *)(iVar8 + DAT_00053260) + (int)*(short *)(iVar6 + iVar8));
  *(undefined2 *)(PTR_OutputRecord_ComputedWords_00053270 + iVar8) = uVar2;
  return;
}

