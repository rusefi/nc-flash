/* Ghidra analysis output; verify against original SH instructions. */

/* Mode0 defaults,1 normal,16 invalid. Normal word0=clamp(2*(2000-s16[FFFF941C]),0,8000). */

void CAN218_Build(ushort param_1)

{
  ushort uVar2;
  int iVar1;
  undefined1 *puVar3;
  undefined1 *puVar4;
  char *pcVar5;
  undefined *puVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 unaff_r8;
  undefined4 unaff_r9;
  undefined4 unaff_r10;
  undefined4 unaff_r11;
  undefined4 unaff_r12;
  int unaff_r13;
  undefined4 unaff_r14;
  undefined1 local_38;
  undefined1 uStack_34;
  undefined1 uStack_30;
  undefined1 uStack_2c;
  undefined1 uStack_28;
  undefined2 uStack_24;
  
  uVar8 = 1;
  uVar2 = param_1 & 0xff;
  uVar7 = 0;
  if (uVar2 == 0) {
    unaff_r13 = 0x46;
    puVar6 = (undefined *)(int)DAT_00019288;
    unaff_r14 = 0;
LAB_00019228:
    param_1 = (ushort)puVar6;
    unaff_r8 = 0;
    uStack_28 = '\0';
    uStack_24 = (short)PTR_DAT_00019298;
  }
  else {
    if (uVar2 == 0x10) {
      unaff_r13 = (int)DAT_00019280;
      unaff_r14 = 1;
      puVar6 = PTR_DAT_00019298;
      goto LAB_00019228;
    }
    if (uVar2 != 1) goto LAB_00019300;
    puVar6 = PTR_DAT_00019298;
    if ((*PTR_DAT_0001929c & 2) == 0) {
      puVar6 = (undefined *)
               (((int)DAT_0001928a - (int)*(short *)PTR_CAN218_Field0Source_000192a0) * 2);
      if ((int)puVar6 < 0) {
        puVar6 = (undefined *)0x0;
      }
      if ((int)DAT_0001928c < (int)puVar6) {
        puVar6 = (undefined *)(int)DAT_0001928c;
      }
    }
    param_1 = (ushort)puVar6;
    puVar6 = PTR_DAT_00019298;
    if (((int)(char)*PTR_ApplicationFaultFlags92C6_000192a4 & 0x80U) == 0) {
      iVar1 = (*(code *)PTR_FUN_000193d0)();
      unaff_r13 = iVar1 + 0x32;
    }
    else {
      unaff_r13 = (int)DAT_00019280;
    }
    if (((TransmissionStateClass != 6) || (((int)(char)*PTR_DAT_000193d4 & 0x80U) != 0)) ||
       (unaff_r14 = uVar7, *PTR_DAT_000193d8 == '\x01')) {
      unaff_r14 = uVar8;
    }
    uStack_28 = (char)uVar7;
    uStack_24 = (short)puVar6;
    unaff_r8 = uVar7;
  }
  uStack_34 = (char)unaff_r8;
  unaff_r9 = unaff_r8;
  unaff_r10 = unaff_r8;
  unaff_r11 = unaff_r8;
  unaff_r12 = unaff_r8;
  local_38 = uStack_28;
  uStack_30 = uStack_28;
  uStack_2c = uStack_28;
LAB_00019300:
  *(ushort *)(int)DAT_000193b4 = param_1;
  *(char *)(int)DAT_000193b6 = (char)unaff_r13;
  *(char *)(int)DAT_000193b8 = (char)unaff_r14;
  puVar3 = (undefined1 *)(int)DAT_000193be;
  *(char *)(int)DAT_000193ba = uStack_2c;
  puVar4 = (undefined1 *)(int)DAT_000193c0;
  *(char *)(int)DAT_000193bc = uStack_28;
  *puVar3 = (char)unaff_r11;
  *puVar4 = (char)unaff_r12;
  *(short *)(int)DAT_000193c2 = uStack_24;
  *(char *)(int)DAT_000193c4 = (char)unaff_r8;
  *(char *)(int)DAT_000193c6 = (char)unaff_r9;
  *(char *)(int)DAT_000193c8 = (char)unaff_r10;
  pcVar5 = (char *)(int)DAT_000193cc;
  *(char *)(int)DAT_000193ca = local_38;
  *pcVar5 = uStack_30;
  puVar6 = PTR_CAN218_SetWord0_000193dc;
  *(char *)(int)DAT_000193ce = uStack_34;
  (*(code *)puVar6)();
  (*(code *)PTR_CAN218_SetByte2_000193e0)(unaff_r13);
  (*(code *)PTR_FUN_000193e4)(unaff_r14);
  (*(code *)PTR_FUN_000193e8)((int)uStack_2c);
  (*(code *)PTR_FUN_000193ec)((int)uStack_28);
  (*(code *)PTR_FUN_000193f0)(unaff_r11);
  (*(code *)PTR_FUN_000193f4)(unaff_r12);
  (*(code *)PTR_CAN218_SetWord4_000193f8)((int)uStack_24);
  (*(code *)PTR_FUN_000193fc)(unaff_r8);
  (*(code *)PTR_FUN_00019400)(unaff_r9);
  (*(code *)PTR_FUN_00019404)(unaff_r10);
  (*(code *)PTR_FUN_00019408)((int)local_38);
  (*(code *)PTR_FUN_0001940c)((int)uStack_30);
                    /* WARNING: Could not recover jumptable at 0x000193b0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_00019410)((int)uStack_34);
  return;
}

