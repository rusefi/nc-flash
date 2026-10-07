/* Ghidra analysis output; verify against original SH instructions. */

/* Partialexecutedevidence:81 state0cases set99FC1 andemitDAE8index9 ->6610++.100 state6cases
   transition12/clearworkingstate,emitindex10 ->6611++ iff660E<=660F;else restart1/noevent.100
   repeatedcalls checknoevent. Otherstates/remoteNVMsemantics unproved. control-activity-hooks.txt.
    */

uint Control_AdvanceSecondActivityState(void)

{
  bool bVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  undefined *puVar9;
  undefined *puVar10;
  undefined *puVar11;
  undefined *puVar12;
  int iVar13;
  undefined2 uVar15;
  undefined1 uVar16;
  byte bVar17;
  char cVar18;
  uint uVar14;
  short *psVar19;
  int iVar20;
  undefined4 uVar21;
  int iVar22;
  byte *pbVar23;
  uint local_20;
  
  puVar2 = PTR_Control_SecondActivityState_00090838;
  iVar13 = (int)DAT_0009082e;
  (&stack0x00000030)[iVar13] = *PTR_Control_SecondActivityState_00090838;
  (&stack0x00000034)[iVar13] = 0;
  if (*PTR_DAT_00090840 == '\x01') {
    uVar15 = (*(code *)PTR_FUN_00090848)((int)*(short *)PTR_DAT_00090844,1);
    *(undefined2 *)PTR_DAT_00090844 = uVar15;
  }
  else {
    *(undefined2 *)PTR_DAT_000908dc = 0;
  }
  if (*(ushort *)PTR_DAT_000908e0 <= *(ushort *)PTR_DAT_000908dc) {
    *puVar2 = 6;
  }
  uVar16 = (*(code *)PTR_FUN_000908e4)();
  (&stack0xfffffffc)[iVar13] = uVar16;
  bVar17 = (*(code *)PTR_FUN_000908e8)();
  puVar12 = PTR_DAT_000912cc;
  puVar11 = PTR_DAT_000910b4;
  puVar10 = PTR_DAT_00090cc8;
  puVar9 = PTR_FUN_00090a78;
  puVar8 = PTR_FUN_00090900;
  puVar7 = PTR_DAT_000908fc;
  puVar6 = PTR_DAT_000908f8;
  puVar5 = PTR_FUN_000908f4;
  puVar4 = PTR_DAT_000908f0;
  puVar3 = PTR_DAT_000908ec;
  (&stack0x00000000)[iVar13] = bVar17;
  *(uint *)(&stack0x00000028 + iVar13) = (uint)bVar17;
  *(uint *)(&stack0x0000002c + iVar13) = (uint)(byte)(&stack0xfffffffc)[iVar13];
  *(uint *)(&stack0xffffffe4 + iVar13) = (uint)(byte)*PTR_DAT_000908fc;
  *(uint *)((int)&local_20 + iVar13) = (uint)(byte)*PTR_DAT_00090904;
  cVar18 = *PTR_DAT_000908f8;
  *(uint *)(&stack0xffffffe8 + iVar13) = (uint)(byte)*PTR_DAT_00090908;
  *(undefined1 **)(&stack0xfffffff4 + iVar13) = &stack0x0000003c + iVar13;
  *(undefined **)(&stack0xfffffff0 + iVar13) = PTR_DAT_0009090c;
  switch(*puVar2) {
  case 0:
    *puVar2 = 1;
    (&stack0x00000034)[iVar13] = 1;
    break;
  case 1:
    if ((*(int *)(&stack0x00000028 + iVar13) <= *(int *)(&stack0x0000002c + iVar13)) ||
       (*PTR_DAT_00090a70 == '\x01')) {
      *PTR_DAT_00090a74 = 1;
      (*(code *)puVar9)();
      FUN_00091352();
      FUN_0009139c();
      cVar18 = (*(code *)PTR_FUN_00090a7c)((int)DAT_00090a62,&stack0x0000005c + iVar13,0x10);
      if (cVar18 == '\0') {
        if ((((&stack0x00000068)[iVar13] == '*') &&
            (*(short *)PTR_DAT_00090a80 ==
             (ushort)((ushort)(byte)(&stack0x00000066)[iVar13] * 0x100 +
                     (ushort)(byte)(&stack0x00000067)[iVar13]))) &&
           (*(short *)PTR_DAT_00090a84 ==
            (ushort)((ushort)(byte)(&stack0x0000006a)[iVar13] * 0x100 +
                    (ushort)(byte)(&stack0x0000006b)[iVar13]))) {
          bVar17 = *PTR_DAT_00090a88;
          if (bVar17 == (&stack0x00000069)[iVar13]) {
            *(ushort *)((int)&local_20 + DAT_00090a64 + iVar13) =
                 (ushort)(byte)(&stack0x0000005c)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x0000005d)[iVar13];
            *(ushort *)((int)&local_20 + DAT_00090a66 + iVar13) =
                 (ushort)(byte)(&stack0x0000005e)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x0000005f)[iVar13];
            *(ushort *)((int)&local_20 + DAT_00090a68 + iVar13) =
                 (ushort)(byte)(&stack0x00000060)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x00000061)[iVar13];
            *(ushort *)((int)&local_20 + DAT_00090a6a + iVar13) =
                 (ushort)(byte)(&stack0x00000062)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x00000063)[iVar13];
            *(ushort *)((int)&local_20 + DAT_00090a6c + iVar13) =
                 (ushort)(byte)(&stack0x00000064)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x00000065)[iVar13];
            for (iVar20 = 0; iVar20 < (int)(uint)bVar17; iVar20 = iVar20 + 1) {
              bVar1 = false;
              iVar22 = 0;
              *(undefined **)((int)&local_20 + iVar13) = PTR_DAT_00090a90 + iVar20 * 2;
              psVar19 = (short *)((int)&local_20 + DAT_00090a64 + iVar13);
              if (bVar17 != 0) {
                do {
                  if (**(short **)((int)&local_20 + iVar13) == *psVar19) {
                    bVar1 = true;
                    break;
                  }
                  iVar22 = iVar22 + 1;
                  psVar19 = psVar19 + 1;
                } while (iVar22 < (int)(uint)bVar17);
              }
              if (!bVar1) goto LAB_00090aa6;
            }
          }
          else {
            *PTR_DAT_00090a8c = 1;
          }
        }
        else {
LAB_00090aa6:
          *PTR_DAT_00090b30 = 1;
        }
        if (*PTR_DAT_00090b30 == '\x01') {
          (&stack0xffffffec)[iVar13] = 0;
          (*(code *)puVar8)((int)DAT_00090b2c,&stack0xffffffec + iVar13,1);
          (*(code *)puVar8)((int)DAT_00090b2e,&stack0xffffffec + iVar13,1);
          uVar16 = (*(code *)puVar5)((int)DAT_00090b2c,2,4);
          *puVar7 = uVar16;
          uVar16 = 2;
          goto LAB_000911d8;
        }
        *puVar2 = 3;
      }
    }
    break;
  case 2:
    if (*(int *)(&stack0xffffffe4 + iVar13) == 1) {
      iVar20 = (int)DAT_00090b2c;
      uVar21 = 2;
LAB_0009116c:
      uVar16 = (*(code *)PTR_FUN_000908f4)(iVar20,uVar21,4);
      *puVar7 = uVar16;
    }
    else if (*(int *)((int)&local_20 + iVar13) == 1) {
      if (cVar18 != '\0') {
        *PTR_DAT_00090b34 = 1;
        *puVar6 = 0;
        uVar16 = 7;
        goto LAB_000911d8;
      }
      uVar16 = (*(code *)PTR_FUN_00090b38)(0,1);
      iVar20 = (int)DAT_00090b2c;
      *puVar6 = uVar16;
      uVar16 = (*(code *)puVar5)(iVar20,2,4);
      *puVar7 = uVar16;
    }
    else if (*(int *)(&stack0xffffffe8 + iVar13) == 1) {
      **(undefined1 **)(&stack0xfffffff4 + iVar13) =
           (char)((ushort)**(undefined2 **)(&stack0xfffffff0 + iVar13) >> 8);
      *(undefined1 **)(&stack0xfffffffc + iVar13) = &stack0x0000003d + iVar13;
      (&stack0x0000003d)[iVar13] = *(undefined1 *)(*(int *)(&stack0xfffffff0 + iVar13) + 1);
      *(undefined1 **)(&stack0x00000000 + iVar13) = &stack0x0000003e + iVar13;
      (&stack0x0000003e)[iVar13] = (char)((ushort)*(undefined2 *)puVar10 >> 8);
      *(undefined1 **)(&stack0xfffffff0 + iVar13) = &stack0x0000003f + iVar13;
      (&stack0x0000003f)[iVar13] = puVar10[1];
      *(undefined1 **)(&stack0xffffffe8 + iVar13) = &stack0x00000040 + iVar13;
      (&stack0x00000040)[iVar13] = (char)((ushort)*(undefined2 *)(puVar10 + 2) >> 8);
      *(undefined1 **)(&stack0xffffffe4 + iVar13) = &stack0x00000041 + iVar13;
      (&stack0x00000041)[iVar13] = puVar10[3];
      *(undefined1 **)(&stack0x00000024 + iVar13) = &stack0x00000042 + iVar13;
      (&stack0x00000042)[iVar13] = (char)((ushort)*(undefined2 *)(puVar10 + 4) >> 8);
      *(undefined1 **)(&stack0x00000020 + iVar13) = &stack0x00000043 + iVar13;
      (&stack0x00000043)[iVar13] = puVar10[5];
      *(undefined1 **)(&stack0x0000001c + iVar13) = &stack0x00000044 + iVar13;
      (&stack0x00000044)[iVar13] = (char)((ushort)*(undefined2 *)(puVar10 + 6) >> 8);
      *(undefined1 **)(&stack0x00000018 + iVar13) = &stack0x00000045 + iVar13;
      (&stack0x00000045)[iVar13] = puVar10[7];
      *(undefined1 **)(&stack0x00000014 + iVar13) = &stack0x00000046 + iVar13;
      (&stack0x00000046)[iVar13] = (char)((ushort)*(undefined2 *)puVar4 >> 8);
      *(undefined1 **)(&stack0x00000010 + iVar13) = &stack0x00000047 + iVar13;
      (&stack0x00000047)[iVar13] = puVar4[1];
      *(undefined1 **)((int)&local_20 + iVar13) = &stack0x00000048 + iVar13;
      (&stack0x00000048)[iVar13] = 0x2a;
      *(undefined1 **)(&stack0x00000004 + iVar13) = &stack0x00000049 + iVar13;
      (&stack0x00000049)[iVar13] = *PTR_DAT_00090ccc;
      *(undefined1 **)(&stack0x00000008 + iVar13) = &stack0x0000004a + iVar13;
      (&stack0x0000004a)[iVar13] = (char)((ushort)*(undefined2 *)puVar3 >> 8);
      *(undefined1 **)(&stack0x0000000c + iVar13) = &stack0x0000004b + iVar13;
      (&stack0x0000004b)[iVar13] = puVar3[1];
      (*(code *)puVar8)((int)DAT_00090ca6,*(undefined4 *)(&stack0xfffffff4 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090ca8,*(undefined4 *)(&stack0xfffffffc + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090caa,*(undefined4 *)(&stack0x00000000 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cac,*(undefined4 *)(&stack0xfffffff0 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cae,*(undefined4 *)(&stack0xffffffe8 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cb0,*(undefined4 *)(&stack0xffffffe4 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cb2,*(undefined4 *)(&stack0x00000024 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cb4,*(undefined4 *)(&stack0x00000020 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cb6,*(undefined4 *)(&stack0x0000001c + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cb8,*(undefined4 *)(&stack0x00000018 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cba,*(undefined4 *)(&stack0x00000014 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cbc,*(undefined4 *)(&stack0x00000010 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cbe,*(undefined4 *)((int)&local_20 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cc0,*(undefined4 *)(&stack0x00000004 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cc2,*(undefined4 *)(&stack0x00000008 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00090cc4,*(undefined4 *)(&stack0x0000000c + iVar13),1);
      *puVar6 = 0;
      uVar16 = (*(code *)puVar5)((int)DAT_00090ca6,0x10,4);
      *puVar7 = uVar16;
      *puVar2 = 3;
    }
    break;
  case 3:
    if ((*(int *)(&stack0xffffffe4 + iVar13) == 1) && (*PTR_DAT_00090dc0 == '\x01')) {
      iVar20 = (int)DAT_00090dba;
      uVar21 = 0x10;
      goto LAB_0009116c;
    }
    if ((*(int *)((int)&local_20 + iVar13) == 1) && (*PTR_DAT_00090dc0 == '\x01')) {
      if (cVar18 != '\0') {
        *PTR_DAT_00090dc4 = 1;
        *puVar6 = 0;
        uVar16 = 7;
        goto LAB_00091116;
      }
      uVar16 = (*(code *)PTR_FUN_00090dc8)(0,1);
      *puVar6 = uVar16;
      uVar16 = (*(code *)puVar5)((int)DAT_00090dba,0x10,4);
      *puVar7 = uVar16;
    }
    else if ((*(int *)(&stack0xffffffe8 + iVar13) == 1) || (*PTR_DAT_00090dc0 == '\0')) {
      cVar18 = (*(code *)PTR_FUN_00090dcc)((int)DAT_00090dbc,&stack0x0000004c + iVar13,0x10);
      if (cVar18 == '\0') {
        if ((((&stack0x00000058)[iVar13] == '*') &&
            (*(short *)PTR_DAT_00090dd0 ==
             (ushort)((ushort)(byte)(&stack0x00000056)[iVar13] * 0x100 +
                     (ushort)(byte)(&stack0x00000057)[iVar13]))) &&
           (*(short *)PTR_DAT_00090dd4 ==
            (ushort)((ushort)(byte)(&stack0x0000005a)[iVar13] * 0x100 +
                    (ushort)(byte)(&stack0x0000005b)[iVar13]))) {
          uVar14 = (uint)(byte)*PTR_DAT_00090ddc;
          if (uVar14 == (byte)(&stack0x00000059)[iVar13]) {
            *(ushort *)((int)&local_20 + DAT_00090ef6 + iVar13) =
                 (ushort)(byte)(&stack0x0000004c)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x0000004d)[iVar13];
            *(ushort *)((int)&local_20 + DAT_00090ef8 + iVar13) =
                 (ushort)(byte)(&stack0x0000004e)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x0000004f)[iVar13];
            *(ushort *)((int)&local_20 + DAT_00090efa + iVar13) =
                 (ushort)(byte)(&stack0x00000050)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x00000051)[iVar13];
            *(ushort *)((int)&local_20 + DAT_00090efc + iVar13) =
                 (ushort)(byte)(&stack0x00000052)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x00000053)[iVar13];
            *(ushort *)((int)&local_20 + DAT_00090efe + iVar13) =
                 (ushort)(byte)(&stack0x00000054)[iVar13] * 0x100 +
                 (ushort)(byte)(&stack0x00000055)[iVar13];
            for (iVar20 = 0; iVar20 < (int)uVar14; iVar20 = iVar20 + 1) {
              *(undefined1 *)((int)&local_20 + iVar13) = 0;
              iVar22 = 0;
              psVar19 = (short *)((int)&local_20 + DAT_00090ef6 + iVar13);
              *(undefined **)(&stack0xffffffe4 + iVar13) = PTR_DAT_00090f04 + iVar20 * 2;
              if (uVar14 != 0) {
                do {
                  if (**(short **)(&stack0xffffffe4 + iVar13) == *psVar19) {
                    *(undefined1 *)((int)&local_20 + iVar13) = 1;
                    break;
                  }
                  iVar22 = iVar22 + 1;
                  psVar19 = psVar19 + 1;
                } while (iVar22 < (int)uVar14);
              }
              if (*(char *)((int)&local_20 + iVar13) == '\0') {
                *PTR_DAT_00090f08 = 1;
                break;
              }
            }
          }
          else {
            *PTR_DAT_00090dd8 = 1;
          }
        }
        else {
          *PTR_DAT_00090dd8 = 1;
        }
        if (*PTR_DAT_00090f08 == '\x01') {
          (&stack0xffffffec)[iVar13] = 0;
          (*(code *)puVar8)((int)DAT_00090f00,&stack0xffffffec + iVar13,1);
          (*(code *)puVar8)((int)DAT_00090f02,&stack0xffffffec + iVar13,1);
          uVar16 = (*(code *)puVar5)((int)DAT_00090f00,2,4);
          *puVar7 = uVar16;
          *puVar2 = 4;
        }
        else {
          *puVar2 = 7;
        }
      }
      *puVar6 = 0;
    }
    break;
  case 4:
    if (*(int *)(&stack0xffffffe4 + iVar13) == 1) {
      iVar20 = (int)DAT_00090f00;
      uVar21 = 2;
      goto LAB_0009116c;
    }
    if (*(int *)((int)&local_20 + iVar13) == 1) {
      if (cVar18 != '\0') {
        *PTR_DAT_00090f0c = 1;
        *puVar6 = 0;
        uVar16 = 7;
        goto LAB_000911d8;
      }
      uVar16 = (*(code *)PTR_FUN_000910b0)(0,1);
      iVar20 = (int)DAT_0009108e;
      *puVar6 = uVar16;
      uVar16 = (*(code *)puVar5)(iVar20,2,4);
      *puVar7 = uVar16;
    }
    else if (*(int *)(&stack0xffffffe8 + iVar13) == 1) {
      **(undefined1 **)(&stack0xfffffff4 + iVar13) =
           (char)((ushort)**(undefined2 **)(&stack0xfffffff0 + iVar13) >> 8);
      *(undefined1 **)(&stack0x00000010 + iVar13) = &stack0x0000003d + iVar13;
      (&stack0x0000003d)[iVar13] = *(undefined1 *)(*(int *)(&stack0xfffffff0 + iVar13) + 1);
      *(undefined1 **)(&stack0x00000014 + iVar13) = &stack0x0000003e + iVar13;
      (&stack0x0000003e)[iVar13] = (char)((ushort)*(undefined2 *)puVar11 >> 8);
      *(undefined1 **)(&stack0x00000018 + iVar13) = &stack0x0000003f + iVar13;
      (&stack0x0000003f)[iVar13] = puVar11[1];
      *(undefined1 **)(&stack0x0000001c + iVar13) = &stack0x00000040 + iVar13;
      (&stack0x00000040)[iVar13] = (char)((ushort)*(undefined2 *)(puVar11 + 2) >> 8);
      *(undefined1 **)((int)&local_20 + iVar13) = &stack0x00000041 + iVar13;
      (&stack0x00000041)[iVar13] = puVar11[3];
      *(undefined1 **)(&stack0xffffffe4 + iVar13) = &stack0x00000042 + iVar13;
      (&stack0x00000042)[iVar13] = (char)((ushort)*(undefined2 *)(puVar11 + 4) >> 8);
      *(undefined1 **)(&stack0xffffffe8 + iVar13) = &stack0x00000043 + iVar13;
      (&stack0x00000043)[iVar13] = puVar11[5];
      *(undefined1 **)(&stack0xfffffff0 + iVar13) = &stack0x00000044 + iVar13;
      (&stack0x00000044)[iVar13] = (char)((ushort)*(undefined2 *)(puVar11 + 6) >> 8);
      *(undefined1 **)(&stack0x00000000 + iVar13) = &stack0x00000045 + iVar13;
      (&stack0x00000045)[iVar13] = puVar11[7];
      *(undefined1 **)(&stack0xfffffffc + iVar13) = &stack0x00000046 + iVar13;
      (&stack0x00000046)[iVar13] = (char)((ushort)*(undefined2 *)puVar4 >> 8);
      *(undefined1 **)(&stack0x00000024 + iVar13) = &stack0x00000047 + iVar13;
      (&stack0x00000047)[iVar13] = puVar4[1];
      *(undefined1 **)(&stack0x00000020 + iVar13) = &stack0x00000048 + iVar13;
      (&stack0x00000048)[iVar13] = 0x2a;
      *(undefined1 **)(&stack0x00000004 + iVar13) = &stack0x00000049 + iVar13;
      (&stack0x00000049)[iVar13] = *PTR_DAT_000910b8;
      *(undefined1 **)(&stack0x00000008 + iVar13) = &stack0x0000004a + iVar13;
      (&stack0x0000004a)[iVar13] = (char)((ushort)*(undefined2 *)puVar3 >> 8);
      *(undefined1 **)(&stack0x0000000c + iVar13) = &stack0x0000004b + iVar13;
      (&stack0x0000004b)[iVar13] = puVar3[1];
      (*(code *)puVar8)((int)DAT_00091090,*(undefined4 *)(&stack0xfffffff4 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00091092,*(undefined4 *)(&stack0x00000010 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00091094,*(undefined4 *)(&stack0x00000014 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00091096,*(undefined4 *)(&stack0x00000018 + iVar13),1);
      (*(code *)puVar8)((int)DAT_00091098,*(undefined4 *)(&stack0x0000001c + iVar13),1);
      (*(code *)puVar8)((int)DAT_0009109a,*(undefined4 *)((int)&local_20 + iVar13),1);
      (*(code *)puVar8)((int)DAT_0009109c,*(undefined4 *)(&stack0xffffffe4 + iVar13),1);
      (*(code *)puVar8)((int)DAT_0009109e,*(undefined4 *)(&stack0xffffffe8 + iVar13),1);
      (*(code *)puVar8)((int)DAT_000910a0,*(undefined4 *)(&stack0xfffffff0 + iVar13),1);
      (*(code *)puVar8)((int)DAT_000910a2,*(undefined4 *)(&stack0x00000000 + iVar13),1);
      (*(code *)puVar8)((int)DAT_000910a4,*(undefined4 *)(&stack0xfffffffc + iVar13),1);
      (*(code *)puVar8)((int)DAT_000910a6,*(undefined4 *)(&stack0x00000024 + iVar13),1);
      (*(code *)puVar8)((int)DAT_0009108e,*(undefined4 *)(&stack0x00000020 + iVar13),1);
      (*(code *)puVar8)((int)DAT_000910a8,*(undefined4 *)(&stack0x00000004 + iVar13),1);
      (*(code *)puVar8)((int)DAT_000910aa,*(undefined4 *)(&stack0x00000008 + iVar13),1);
      (*(code *)puVar8)((int)DAT_000910ac,*(undefined4 *)(&stack0x0000000c + iVar13),1);
      *puVar6 = 0;
      uVar16 = (*(code *)puVar5)((int)DAT_00091090,0x10,4);
      *puVar7 = uVar16;
      *puVar2 = 5;
    }
    break;
  case 5:
    if (*(int *)(&stack0xffffffe4 + iVar13) == 1) {
      iVar20 = (int)DAT_000911b6;
      uVar21 = 0x10;
      goto LAB_0009116c;
    }
    if (*(int *)((int)&local_20 + iVar13) == 1) {
      if (cVar18 != '\0') {
        *PTR_DAT_000911bc = 1;
        *puVar6 = 0;
        uVar16 = 7;
        goto LAB_000911d8;
      }
      uVar16 = (*(code *)PTR_FUN_000911c0)(0,1);
      *puVar6 = uVar16;
      uVar16 = (*(code *)puVar5)((int)DAT_000911b6,0x10,4);
      *puVar7 = uVar16;
    }
    else if (*(int *)(&stack0xffffffe8 + iVar13) == 1) {
      *PTR_DAT_000908f8 = 0;
      *puVar2 = 7;
    }
    break;
  case 6:
    *puVar2 = 0xc;
    break;
  case 7:
    uVar16 = 8;
LAB_00091116:
    *puVar2 = uVar16;
    break;
  case 8:
    if (*PTR_DAT_000911c4 == '\x01') {
      pbVar23 = &stack0x00000038 + iVar13;
      bVar17 = FUN_0009157c();
      *pbVar23 = bVar17;
      *(undefined1 **)((int)&local_20 + iVar13) = &stack0x00000039 + iVar13;
      (&stack0x00000039)[iVar13] = ~*pbVar23;
      (*(code *)puVar8)((int)DAT_000911b8,pbVar23,1);
      (*(code *)puVar8)((int)DAT_000911ba,*(undefined4 *)((int)&local_20 + iVar13),1);
      uVar16 = (*(code *)puVar5)((int)DAT_000911b8,2,4);
      *puVar7 = uVar16;
      uVar16 = 9;
      goto LAB_000911d8;
    }
    *puVar2 = 10;
    break;
  case 9:
    if (*(int *)(&stack0xffffffe4 + iVar13) == 1) {
      iVar20 = (int)DAT_000911b8;
      uVar21 = 2;
      goto LAB_0009116c;
    }
    if (*(int *)((int)&local_20 + iVar13) == 1) {
      if (cVar18 != '\0') {
        *PTR_DAT_000911bc = 1;
        *puVar6 = 0;
        uVar16 = 10;
        goto LAB_000911d8;
      }
      uVar16 = (*(code *)PTR_FUN_000911c0)(0,1);
      *puVar6 = uVar16;
      uVar16 = (*(code *)puVar5)((int)DAT_000911b8,2,4);
      *puVar7 = uVar16;
    }
    else if (*(int *)(&stack0xffffffe8 + iVar13) == 1) {
      *PTR_DAT_000908f8 = 0;
      *PTR_DAT_000911c4 = 0;
      *puVar2 = 10;
    }
    break;
  case 10:
    if (*PTR_DAT_000912c0 == '\0') {
      *PTR_DAT_000912c4 = 1;
    }
    uVar16 = 0xb;
LAB_000911d8:
    *puVar2 = uVar16;
    break;
  case 0xb:
    if (*PTR_DAT_000912c8 == '\x01') {
      if (*PTR_DAT_000912d0 == '\0') {
        *PTR_DAT_000912cc = 0;
      }
      if (*puVar12 == '\x01') {
        *puVar2 = 0xc;
      }
    }
  }
  puVar3 = PTR_DAT_000912d8;
  if (((&stack0x00000030)[iVar13] != *puVar2) && (*puVar2 == '\f')) {
    *PTR_DAT_000912d4 = 0;
    *(undefined2 *)puVar3 = 0;
    puVar3 = PTR_DAT_000912e0;
    *PTR_DAT_000912dc = 0;
    *puVar3 = 0;
    *puVar7 = 0;
    *PTR_DAT_000912e4 = 0;
    if (*(int *)(&stack0x0000002c + iVar13) < *(int *)(&stack0x00000028 + iVar13)) {
      *puVar2 = 1;
      (&stack0x00000034)[iVar13] = 0;
    }
    else {
      (&stack0x00000034)[iVar13] = 2;
    }
  }
  *(undefined4 *)(&stack0xfffffff8 + iVar13) = 0;
  if ((&stack0x00000034)[iVar13] == '\x01') {
    uVar21 = 9;
  }
  else {
    if ((&stack0x00000034)[iVar13] != '\x02') goto LAB_00091282;
    uVar21 = 10;
  }
  (*(code *)PTR_Control_DispatchDescriptorEvent_000912e8)(0,uVar21,&stack0xfffffff8 + iVar13);
LAB_00091282:
  cVar18 = (*(code *)PTR_FUN_000912f0)(PTR_DAT_000912ec);
  puVar2 = PTR_DAT_000912c4;
  if (cVar18 == '\x01') {
    *PTR_DAT_000912c0 = 0;
    *puVar2 = 0;
    *PTR_DAT_000912f4 = 0;
  }
  else {
    *PTR_DAT_000912c0 = *PTR_DAT_000912f4;
  }
  if (*PTR_DAT_000912c0 == '\x01') {
    uVar14 = (*(code *)PTR_Diagnostic_ReportUntimedGroup_000912f8)(0x6d,1);
  }
  else {
    uVar14 = (uint)(byte)*PTR_DAT_00091410;
    if (uVar14 == 1) {
      uVar14 = (*(code *)PTR_Diagnostic_ReportUntimedGroup_00091414)(0x6d,2);
    }
  }
  *PTR_DAT_0009141c = *PTR_DAT_00091418;
  return uVar14;
}

