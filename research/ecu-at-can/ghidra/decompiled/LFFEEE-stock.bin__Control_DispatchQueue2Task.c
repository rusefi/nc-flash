/* Ghidra analysis output; verify against original SH instructions. */

/* Originaltask3priority2 invokedthrough3B8A/RTE. F6A0selector2 copiesfivewords45A4..45B4;
   returnsDC50 thenDC66callsE5FC. TwoactualconsumerwholeRAM returns in10tickprefix PASS,
   exactpreviousrecord. Full600earlierdrains120upstreamrequests; onlyqueue3RAMoracle
   inthatfullrecord. control-timer-event2.txt. */

undefined4 Control_DispatchQueue2Task(void)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  code *pcVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 *puVar7;
  int iVar8;
  undefined4 uStack_c;
  undefined4 *puStack_8;
  
  pcVar4 = pcRam0000dce0;
  puVar3 = puRam0000dcdc;
  iVar2 = iRam0000dcd8;
  iVar8 = (int)sRam0000dcd4;
  puStack_8 = puRam0000dcdc;
  puVar7 = puRam0000dcdc + 1;
  do {
    (*pcVar4)(&uStack_c,iVar8);
    iVar5 = (*(code *)PTR_Control_DequeueCallbackRecord_0000dce4)(2,puVar3);
    cVar1 = *(char *)(iVar2 + 2);
    (*(code *)PTR_FUN_0000dce8)(uStack_c);
    if (iVar5 == 0) {
      (*(code *)*puStack_8)(puVar7);
    }
  } while (cVar1 != '\0');
  uVar6 = (*(code *)PTR_LAB_0000dcec)();
  return uVar6;
}

