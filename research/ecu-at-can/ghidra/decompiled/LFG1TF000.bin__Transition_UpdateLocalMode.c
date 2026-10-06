/* Ghidra analysis output; verify against original SH instructions. */

/* Executes policy helpers, calls2D1BC before saving new954D; saves8080 in954C.192 paired
   caller-to-CAN231/ECU cases and7 lifecycle steps; other policy details not exhaustive. See
   transition-gate.txt. */

uint Transition_UpdateLocalMode(void)

{
  undefined *puVar1;
  undefined1 *puVar2;
  byte bVar3;
  uint uVar4;
  char cVar5;
  char *pcVar6;
  uint uVar7;
  
  bVar3 = TransmissionStateClass;
  uVar4 = func_0x0002c892((int)(char)TransmissionStateClass,(int)*(char *)(int)sRam0002c810);
  func_0x0002caec(uVar4);
  func_0x0002cb90(uVar4);
  cVar5 = func_0x0002cc70(uVar4);
  if (cVar5 == '\x01') {
    uVar4 = (uint)DAT_0002c80c;
  }
  func_0x0002cef0(uVar4);
  func_0x0002cf0a();
  func_0x0002cf98();
  func_0x0002d090();
  func_0x0002d118(uVar4);
  func_0x0002d146(uVar4);
  puVar2 = puRam0002c92c;
  puVar1 = PTR_DAT_0002c828;
  uVar7 = uVar4 & 0xff;
  if (uVar7 == (int)DAT_0002c80c) {
    PTR_DAT_0002c828[1] = PTR_DAT_0002c828[1] | 2;
  }
  else {
    PTR_DAT_0002c828[1] = PTR_DAT_0002c828[1] & 0xfd;
    *puVar2 = 0;
  }
  Transition_UpdateAcceptanceBlock(uVar4);
  (*pcRam0002c930)(uVar4);
  pcVar6 = (char *)(int)sRam0002c926;
  cVar5 = *pcVar6;
  if (((cVar5 != '\0') && (uVar7 == 0)) || ((cVar5 != '\x05' && (uVar7 == 5)))) {
    *puVar1 = *puVar1 & 0xfe;
  }
  *(byte *)(int)sRam0002c928 = bVar3;
  *pcVar6 = (char)uVar4;
  return uVar4;
}

