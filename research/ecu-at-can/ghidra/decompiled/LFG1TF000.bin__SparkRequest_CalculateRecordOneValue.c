/* Ghidra analysis output; verify against original SH instructions. */

/* Phase953F3: signed953C*(953E-8170)/953E via saturating10D0C. Positive duration10/elapsed0..10
   tested through fullcaller. Phases1/2 and physical role unresolved. */

uint SparkRequest_CalculateRecordOneValue(void)

{
  undefined *puVar1;
  short sVar2;
  int extraout_r2;
  uint uVar3;
  char *pcVar4;
  short *psVar5;
  undefined4 local_1c;
  undefined4 local_18;
  short local_14 [6];
  
  psVar5 = local_14;
  puVar1 = (undefined *)(int)Primary_ApplicationInput;
  if ((int)puVar1 < 0) {
    puVar1 = (undefined *)0x0;
  }
  if ((int)PTR_DAT_0002c4dc < (int)puVar1) {
    puVar1 = PTR_DAT_0002c4dc;
  }
  pcVar4 = (char *)(int)DAT_0002c4c2;
  if (*pcVar4 == '\x01') {
    FUN_0002c534(puVar1);
  }
  if (*pcVar4 == '\x02') {
    FUN_0002c5ec(puVar1);
  }
  if (*pcVar4 == '\x02') {
    uVar3 = (*(code *)PTR_Lookup_ByteGrid2D_Q8_0002c4e4)
                      ((int)*(short *)(int)DAT_0002c4c6,puVar1,
                       PTR_DAT_0002c4e0 + (uint)CAN231_SixStateSource * 0x25);
    uVar3 = (uVar3 & 0xffff) >> 2;
  }
  else if (*pcVar4 == '\x03') {
    local_14[0] = (ushort)*(byte *)(int)DAT_0002c4c8 - (ushort)(byte)*PTR_DAT_0002c4e8;
    uVar3 = (*(code *)PTR_FixedPoint_DivideToSignedWord_0002c4ec)
                      ((int)*(short *)(int)DAT_0002c4ca * (int)local_14[0]);
    psVar5 = local_14;
  }
  else {
    local_18 = 0;
    local_1c = DAT_0002c5cc;
    sVar2 = (*(code *)PTR_FUN_0002c5d0)();
    uVar3 = (uint)sVar2;
    psVar5 = (short *)&local_1c;
  }
  if (*pcVar4 == '\x02') {
    *(undefined4 *)((int)psVar5 + -4) = 0;
    *(undefined4 *)((int)psVar5 + -8) = DAT_0002c5cc;
    sVar2 = (*(code *)PTR_FUN_0002c5d0)();
    if (extraout_r2 != sVar2) {
      *(byte *)(int)DAT_0002c5c4 = *(byte *)(int)DAT_0002c5c4 | 1;
    }
  }
  return uVar3;
}

