/* Ghidra analysis output; verify against original SH instructions. */

/* Original3DD8-selectedtask17 reaches105FC CMT1init/4ACC ADCinit/CA94.
   FiniteexternalADCstatus/results andstrictlatches; continuation stopsA46F6
   unsupportedwordwriteFFFFEC62 after388indirectcalls. Not completeboot.
   control-scheduler-start.txt. */

undefined4 Startup_Task17(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined4 uVar5;
  byte *pbVar6;
  int iVar7;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  undefined4 uStack_18;
  undefined4 uStack_14;
  undefined4 uStack_10;
  undefined4 uStack_c;
  undefined4 auStack_8 [2];
  
  puVar1 = PTR_FUN_0000de5c;
  (*(code *)PTR_FUN_0000de5c)();
  (*(code *)PTR_LAB_0000de60)();
  (*(code *)PTR_Control_InitializeCmt1_0000de64)();
  (*(code *)PTR_LAB_0000de68)();
  (*(code *)PTR_LAB_0000de6c)();
  (*(code *)puVar1)();
  (*(code *)PTR_LAB_0000de70)();
  (*(code *)puVar1)();
  (*(code *)PTR_LAB_0000de74)();
  (*(code *)PTR_LAB_0000de78)();
  (*(code *)PTR_Acquisition_InitializeAndPollAdcBanks_0000de7c)();
  (*(code *)PTR_Input_InitializeLocalFilters_0000de80)();
  (*(code *)PTR_LAB_0000de84)();
  (*(code *)PTR_PTR_0000de88)();
  puVar2 = PTR_FUN_0000de8c;
  iVar7 = (int)sRam0000de46;
  (*(code *)PTR_FUN_0000de8c)(auStack_8,iVar7);
  *(byte *)(int)sRam0000de48 = *(byte *)(int)sRam0000de48 & 0xf8 | 5;
  puVar3 = PTR_FUN_0000de90;
  (*(code *)PTR_FUN_0000de90)(auStack_8[0]);
  *(undefined2 *)(int)sRam0000de4a = 0;
  (*(code *)puVar2)(&uStack_c,iVar7);
  *(byte *)(int)sRam0000de4c = *(byte *)(int)sRam0000de4c & 0xfc | 1;
  (*(code *)puVar3)(uStack_c);
  *(undefined1 *)(int)sRam0000de4e = 0;
  (*(code *)puVar2)(&uStack_10,iVar7);
  pbVar6 = (byte *)(int)sRam0000de50;
  *pbVar6 = *pbVar6 & 0xf8 | 6;
  (*(code *)puVar3)(uStack_10);
  *(undefined2 *)(int)sRam0000de52 = 0;
  (*(code *)puVar2)(&uStack_14,iVar7);
  *pbVar6 = *pbVar6 & 0x8f | 0x60;
  (*(code *)puVar3)(uStack_14);
  *(undefined2 *)(int)sRam0000de54 = 0;
  (*(code *)puVar2)(&uStack_18,iVar7);
  pbVar6 = (byte *)(int)sRam0000de56;
  *pbVar6 = *pbVar6 & 0xf8 | 6;
  (*(code *)puVar3)(uStack_18);
  *(undefined2 *)(int)sRam0000de58 = 0;
  (*(code *)puVar2)(&uStack_1c,iVar7);
  *pbVar6 = *pbVar6 & 0x8f | 0x60;
  (*(code *)puVar3)(uStack_1c);
  puVar4 = PTR_PTR_0000de94;
  *(undefined2 *)(int)sRam0000de5a = 0;
  (*(code *)puVar4)();
  (*(code *)PTR_LAB_0000de98)();
  (*(code *)PTR_Acquisition_InitChannel1History_0000de9c)();
  (*(code *)PTR_LAB_0000dea0)();
  func_0x0000e258();
  (*(code *)PTR_LAB_0000dea4)();
  (*(code *)PTR_LAB_0000dea8)();
  (*(code *)PTR_LAB_0000deac)();
  (*(code *)PTR_Control_InitRawChannel29_0000deb0)();
  (*(code *)PTR_Control_InitRawChannel28_0000deb4)();
  (*(code *)PTR_LAB_0000deb8)();
  (*(code *)PTR_LAB_0000debc)();
  (*(code *)PTR_LAB_0000dec0)();
  (*(code *)PTR_LAB_0000dfb4)();
  (*(code *)PTR_LAB_0000dfb8)();
  (*(code *)PTR_LAB_0000dfbc)();
  (*(code *)PTR_LAB_0000dfc0)();
  (*(code *)PTR_LAB_0000dfc4)();
  (*(code *)puVar2)(&uStack_20,iVar7);
  *(byte *)(int)sRam0000dfae = *(byte *)(int)sRam0000dfae & 0xcf | 0x30;
  (*(code *)puVar3)(uStack_20);
  (*(code *)PTR_Register_UpdateMaskedWord_0000dfc8)((int)sRam0000dfb0,4,1);
  (*(code *)PTR_LAB_0000dfcc)();
  (*(code *)PTR_LAB_0000dfd0)();
  (*(code *)PTR_LAB_0000dfd4)();
  (*(code *)PTR_LAB_0000dfd8)();
  (*(code *)PTR_LAB_0000dfdc)();
  (*(code *)PTR_LAB_0000dfe0)();
  (*(code *)PTR_LAB_0000dfe4)();
  (*(code *)PTR_LAB_0000dfe8)();
  (*(code *)PTR_LAB_0000dfec)();
  (*(code *)PTR_LAB_0000dff0)();
  (*(code *)PTR_LAB_0000dff4)();
  (*(code *)PTR_LAB_0000dff8)();
  (*pcRam0000dffc)();
  (*(code *)PTR_LAB_0000e000)();
  (*(code *)PTR_LAB_0000e004)();
  (*(code *)puVar1)();
  (*(code *)PTR_LAB_0000e008)();
  (*(code *)PTR_LAB_0000e00c)();
  (*(code *)puVar1)();
  (*(code *)PTR_LAB_0000e010)();
  (*(code *)PTR_LAB_0000e014)();
  (*(code *)PTR_LAB_0000e018)();
  (*(code *)PTR_LAB_0000e01c)();
  (*(code *)PTR_LAB_0000e020)();
  (*(code *)PTR_LAB_0000e024)();
  (*(code *)PTR_LAB_0000e028)(1);
  uVar5 = (*(code *)PTR_LAB_0000e02c)();
  return uVar5;
}

