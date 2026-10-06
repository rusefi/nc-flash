/* Ghidra analysis output; verify against original SH instructions. */

/* Clear if722E zero or7974 zero; set if6E57/6A20/797A exactly1 or historical7987bit7/timer75B0
   plus7985==0/current797B==1 and6DB4<900; else hold. Always update7985/7987 history;
   traction-flags.txt. */

void Control_UpdateRetainedLatch7978(void)

{
  char cVar1;
  undefined *puVar2;
  char cVar3;
  byte bVar4;
  float fVar5;
  
  cVar1 = *PTR_DAT_0004ea08;
  bVar4 = *PTR_DAT_0004ea0c;
  cVar3 = (*(code *)PTR_FUN_0004e9f8)(PTR_DAT_0004e9f4);
  if ((cVar3 == '\0') || (*(short *)PTR_Control_Latch7978CountGate_0004ea10 == 0)) {
    (*(code *)PTR_FUN_0004ea04)(PTR_Control_RetainedLatch7978_0004ea00,0);
  }
  else if (((*PTR_CAN216_Bit7ControlRequest_0004ea14 == '\x01') ||
           ((*PTR_DAT_0004ea18 == '\x01' || (*PTR_DAT_0004ea1c == '\x01')))) ||
          (((((int)(char)*PTR_Control_Latch7978HistoryBits_0004ea20 & 0x80U) != 0 ||
            (*PTR_DAT_0004ea24 != '\0')) &&
           (((*PTR_Control_Latch7978PreviousState_0004ea28 == '\0' && (cVar1 == '\x01')) &&
            (fVar5 = (float)(*(code *)PTR_FUN_0004ea30)(PTR_DAT_0004ea2c),
            fVar5 < *(float *)PTR_DAT_0004ea34)))))) {
    (*(code *)PTR_FUN_0004ea04)(PTR_Control_RetainedLatch7978_0004ea00,1);
  }
  puVar2 = PTR_Control_Latch7978HistoryBits_0004ea20;
  *PTR_Control_Latch7978PreviousState_0004ea28 = cVar1;
  if ((bVar4 & 0x10) == 0) {
    bVar4 = *puVar2 & 0x7f;
  }
  else {
    bVar4 = *puVar2 | 0x80;
  }
  *puVar2 = bVar4;
  return;
}

