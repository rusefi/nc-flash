/* Ghidra analysis output; verify against original SH instructions. */

/* Drains queue0 including messages enqueued bycallbacks; dispatch table5E20C[group] with operation
   andpayloadpointer. Complete creation/update/cancel/free paths verified. See
   tcu-request-dispatch.txt. */

void EventQueue_Drain(uint param_1)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  ushort *puVar4;
  char *pcVar5;
  byte bVar6;
  
  puVar3 = PTR_PTR_ARRAY_0004c3b8;
  puVar2 = PTR_DAT_0004c3b0;
  pcVar5 = PTR_DAT_0004c3ac + (param_1 & 0xff) * 3;
  bVar6 = pcVar5[1];
  uVar1 = (uint)DAT_0004c3aa;
  while (*pcVar5 != '\0') {
    puVar4 = (ushort *)(puVar2 + (uint)bVar6 * 8 + (param_1 & 0xff) * 0x50);
    (**(code **)(puVar3 + (uint)*puVar4 * 4 + (param_1 & 0xff) * uVar1))
              ((int)(short)puVar4[1],*(undefined4 *)(puVar4 + 2));
    bVar6 = bVar6 + 1;
    *pcVar5 = *pcVar5 + -1;
    if (bVar6 == 10) {
      bVar6 = 0;
    }
  }
  PTR_DAT_0004c3bc[(param_1 & 0xff) * 3] = bVar6;
  return;
}

