/* Ghidra analysis output; verify against original SH instructions. */

/* Queue3 count0..100/head0or99/SR0,70,F0:606wholeRAM cases PASS. Copiesfivewords tocallerR5,
   decrements45DB/advances45DAmod100, emptyreturns3.140actualconsumerreturns checked
   in120eventcycles;298 in600timerdrains. Additionalqueue2:186isolatedwholeRAMcases
   and2actualDC50returns in10tickprefix PASS; control-timer-event2.txt. control-queued-event2.txt.
    */

undefined4 Control_DequeueCallbackRecord(uint param_1,undefined4 *param_2)

{
  undefined *puVar1;
  uint uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 uStack_1c;
  byte bStack_18;
  
  uVar4 = 0;
  iVar5 = *(int *)(PTR_PTR_0000f748 + (param_1 & 0xffff) * 8);
  bStack_18 = *(byte *)((int)(PTR_PTR_0000f748 + (param_1 & 0xffff) * 8) + 6);
  (*(code *)PTR_FUN_0000f74c)(&uStack_1c,(int)DAT_0000f744);
  puVar1 = PTR_DAT_0000f750;
  uVar2 = param_1 & 0xffff;
  if (PTR_DAT_0000f750[uVar2 * 3 + 2] == '\0') {
    uVar4 = 3;
  }
  else {
    PTR_DAT_0000f750[uVar2 * 3 + 2] = PTR_DAT_0000f750[uVar2 * 3 + 2] + -1;
    puVar6 = (undefined4 *)(iVar5 + (uint)(byte)puVar1[uVar2 * 3 + 1] * 0x14);
    iVar5 = 5;
    do {
      iVar5 = iVar5 + -1;
      uVar3 = *puVar6;
      puVar6 = puVar6 + 1;
      *param_2 = uVar3;
      param_2 = param_2 + 1;
    } while (iVar5 != 0);
    uVar2 = param_1 & 0xffff;
    puVar1[uVar2 * 3 + 1] = puVar1[uVar2 * 3 + 1] + '\x01';
    if (bStack_18 <= (byte)puVar1[uVar2 * 3 + 1]) {
      puVar1[(param_1 & 0xffff) * 3 + 1] = 0;
    }
  }
  (*(code *)PTR_FUN_0000f754)(uStack_1c);
  return uVar4;
}

