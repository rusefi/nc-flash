/* Ghidra analysis output; verify against original SH instructions. */

/* Application state encoding; paired original-code tests cover six states. */

void CAN231_Build(char param_1)

{
  undefined *puVar1;
  undefined1 *puVar2;
  char *pcVar3;
  undefined4 unaff_r8;
  int unaff_r9;
  undefined4 unaff_r10;
  undefined4 unaff_r11;
  undefined4 unaff_r12;
  int unaff_r13;
  char local_48;
  char cStack_44;
  char cStack_40;
  char cStack_3c;
  char cStack_38;
  char cStack_34;
  short sStack_30;
  char cStack_2c;
  char cStack_28;
  char cStack_24;
  
  if (param_1 == '\0') {
    unaff_r12 = 0;
    local_48 = '\0';
    cStack_24 = '\0';
    unaff_r10 = 0;
    unaff_r9 = 0;
    unaff_r13 = 0;
    unaff_r8 = 0;
    cStack_28 = '\0';
    unaff_r11 = 0;
    cStack_2c = '\0';
    sStack_30 = (short)PTR_DAT_00019528;
    cStack_34 = '\0';
    cStack_38 = '\0';
    cStack_3c = '\0';
    cStack_44 = '\0';
    cStack_40 = '\0';
  }
  else if (param_1 == '\x10') {
    unaff_r12 = 0xf;
    unaff_r10 = 0xf;
    unaff_r9 = 0;
    unaff_r13 = 0;
    unaff_r8 = FUN_000197be();
    local_48 = '\0';
    unaff_r11 = 0;
    cStack_24 = '\0';
    cStack_28 = '\0';
    cStack_2c = '\0';
    sStack_30 = (short)PTR_DAT_00019528;
    cStack_3c = (char)DAT_00019526;
    cStack_44 = '\x0f';
    cStack_40 = '\x0f';
    cStack_38 = cStack_3c;
    cStack_34 = cStack_3c;
  }
  else if (param_1 == '\x01') {
    unaff_r12 = CAN231_EncodeSixState((int)(char)CAN231_SixStateSource);
    unaff_r10 = 0xf;
    if (((byte)((((*PTR_DAT_0001952c & 1) -
                 (((PTR_Selector_ApplicationFlags16_00019530[1] & 4) == 0) + -1)) -
                (((*PTR_DAT_0001952c & 2) == 0) + -1)) -
               (((*PTR_Selector_ApplicationFlags16_00019530 & 4) == 0) + -1)) < 2) &&
       ((*PTR_DAT_00019534 & 0x40) == 0)) {
      if ((*PTR_DAT_0001952c & 1) == 1) {
        unaff_r10 = 1;
      }
      else if ((PTR_Selector_ApplicationFlags16_00019530[1] & 4) == 0) {
        if ((*PTR_DAT_0001952c & 2) == 0) {
          if ((*PTR_Selector_ApplicationFlags16_00019530 & 4) == 0) {
            unaff_r10 = 0;
          }
          else {
            unaff_r10 = 4;
          }
        }
        else {
          unaff_r10 = 3;
        }
      }
      else {
        unaff_r10 = 2;
      }
    }
    unaff_r9 = (int)(char)*PTR_DAT_000196c4;
    unaff_r13 = (int)(char)*PTR_DAT_000196c8;
    unaff_r8 = FUN_000197be();
    local_48 = -(((*PTR_DAT_000196cc & 0x20) == 0) + -1);
    cStack_24 = *PTR_DAT_000196d0;
    unaff_r11 = 0;
    cStack_28 = '\0';
    cStack_2c = '\0';
    sStack_30 = CAN231_BuildWord2();
    cStack_34 = '\0';
    cStack_38 = '\0';
    cStack_3c = '\0';
    cStack_44 = '\0';
    cStack_40 = CAN231_EncodeSixState((int)(char)*PTR_DAT_000196d4);
  }
  *(char *)(int)DAT_000196a2 = (char)unaff_r12;
  *(char *)(int)DAT_000196a4 = (char)unaff_r10;
  *(char *)(int)DAT_000196a6 = (char)unaff_r9;
  *(char *)(int)DAT_000196a8 = (char)unaff_r13;
  *(char *)(int)DAT_000196aa = (char)unaff_r8;
  puVar2 = (undefined1 *)(int)DAT_000196b2;
  *(char *)(int)DAT_000196ac = local_48;
  *(char *)(int)DAT_000196ae = cStack_24;
  *(char *)(int)DAT_000196b0 = cStack_28;
  *puVar2 = (char)unaff_r11;
  *(char *)(int)DAT_000196b4 = cStack_2c;
  *(short *)(int)DAT_000196b6 = sStack_30;
  *(char *)(int)DAT_000196b8 = cStack_34;
  pcVar3 = (char *)(int)DAT_000196be;
  *(char *)(int)DAT_000196ba = cStack_38;
  *(char *)(int)DAT_000196bc = cStack_3c;
  *pcVar3 = cStack_44;
  puVar1 = PTR_CAN231_SetHighNibble_000196d8;
  *(char *)(int)DAT_000196c0 = cStack_40;
  (*(code *)puVar1)(unaff_r12);
  (*(code *)PTR_CAN231_SetLowNibble_000196dc)(unaff_r10);
  (*(code *)PTR_FUN_000196e0)(unaff_r9);
  (*(code *)PTR_FUN_000196e4)(unaff_r13);
  (*(code *)PTR_FUN_000196e8)(unaff_r8);
  (*(code *)PTR_FUN_000196ec)((int)local_48);
  (*(code *)PTR_FUN_000196f0)((int)cStack_24);
  (*(code *)PTR_FUN_000196f4)((int)cStack_28);
  (*(code *)PTR_FUN_000196f8)(unaff_r11);
  (*(code *)PTR_FUN_000196fc)((int)cStack_2c);
  (*(code *)PTR_CAN231_SetWord2_00019700)((int)sStack_30);
  (*(code *)PTR_FUN_00019704)((int)cStack_34);
  (*(code *)PTR_FUN_00019708)((int)cStack_38);
  (*(code *)PTR_FUN_0001970c)((int)cStack_3c);
  (*(code *)PTR_FUN_00019710)((int)cStack_44);
  (*(code *)PTR_FUN_00019714)((int)cStack_40);
  return;
}

