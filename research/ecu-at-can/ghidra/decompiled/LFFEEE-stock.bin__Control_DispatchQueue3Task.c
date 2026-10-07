/* Ghidra analysis output; verify against original SH instructions. */

/* Originaltask4 invokedthrough3B8A/RTE;F6A0copies45B8
   thenDCBAinvokestarget,args45BC,returnDCBE.120actualevent2
   plus19callbacks959F2/1callback95AFC;140consumerwholeRAM checks,ringwrap. Monitoredfields
   exactpriordirectevent2. ExplicitstackFFFED000/maskF0/1:1acquisitioninterleave.
   control-queued-event2.txt. */

undefined4 Control_DispatchQueue3Task(void)

{
  char cVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 *puVar7;
  int iVar8;
  undefined4 uStack_c;
  undefined4 *puStack_8;
  
  puVar4 = puRam0000dcf4;
  iVar3 = iRam0000dcf0;
  pcVar2 = pcRam0000dce0;
  iVar8 = (int)sRam0000dcd4;
  puStack_8 = puRam0000dcf4;
  puVar7 = puRam0000dcf4 + 1;
  do {
    (*pcVar2)(&uStack_c,iVar8);
    iVar5 = (*(code *)PTR_Control_DequeueCallbackRecord_0000dce4)(3,puVar4);
    cVar1 = *(char *)(iVar3 + 2);
    (*(code *)PTR_FUN_0000dce8)(uStack_c);
    if (iVar5 == 0) {
      (*(code *)*puStack_8)(puVar7);
    }
  } while (cVar1 != '\0');
  uVar6 = (*(code *)PTR_LAB_0000dcec)();
  return uVar6;
}

