/* Ghidra analysis output; verify against original SH instructions. */

/* CompleteRAMoracle directandactualphase3/7.9C58bit0 forcesA5A2=1 andfivezeros; clearsA5A2
   onlyif9415==1 andbitclear. Lasteligible slot->70014row;910Cbit0 mirrors9AE8bit6. See
   tcu-source-inhibit.txt. */

void DiscreteOutput_SelectAndInhibit(void)

{
  bool bVar1;
  undefined *puVar2;
  char cVar3;
  uint uVar4;
  int iVar5;
  char cVar6;
  char cVar7;
  char cVar8;
  int iVar9;
  char cStack_30;
  undefined1 local_2c [16];
  
  bVar1 = (*PTR_DAT_0001f484 & 0x40) == 0;
  cVar3 = (*(code *)PTR_FUN_0001f488)();
  if ((cVar3 == '\x01') && ((*PTR_Selection_InhibitFlags_0001f48c & 1) == 0)) {
    (*(code *)PTR_OutputPins_SetSource_0001f490)(1,0);
  }
  puVar2 = PTR_DiscreteOutput_SlotEnableMask_0001f494;
  cVar3 = '\0';
  if ((*PTR_Selection_InhibitFlags_0001f48c & 1) == 1) {
    cVar8 = '\0';
    cStack_30 = '\0';
    cVar7 = '\0';
    cVar6 = '\0';
    DiscreteOutput_SelectedKey = '\x04';
    (*(code *)PTR_OutputPins_SetSource_0001f490)(1);
  }
  else {
    iVar5 = (int)DAT_0001f476;
    for (iVar9 = 0; iVar9 < 0xb; iVar9 = iVar9 + 1) {
      if (puVar2[iVar9] == '\0') {
        DiscreteOutput_ClearSlot(iVar9);
      }
      local_2c[iVar9] = *(undefined1 *)(iVar5 + iVar9);
    }
    DiscreteOutput_SelectedKey = (*(code *)PTR_Request_SelectLastByte_0001f498)(local_2c,0xb,4);
    uVar4 = 0;
    while (DiscreteOutput_SelectedKey != PTR_DiscreteOutput_CommandRows_0001f49c[(uVar4 & 0xff) * 6]
          ) {
      uVar4 = uVar4 + 1;
    }
    uVar4 = uVar4 & 0xff;
    cStack_30 = PTR_DiscreteOutput_CommandRows_0001f49c[uVar4 * 6 + 1];
    cVar8 = PTR_DiscreteOutput_CommandRows_0001f49c[uVar4 * 6 + 2];
    cVar7 = PTR_DiscreteOutput_CommandRows_0001f49c[uVar4 * 6 + 3];
    cVar6 = PTR_DiscreteOutput_CommandRows_0001f49c[uVar4 * 6 + 4];
    cVar3 = PTR_DiscreteOutput_CommandRows_0001f49c[uVar4 * 6 + 5];
  }
  puVar2 = PTR_DiscreteOutput_SetCommand_0001f5b0;
  if (bVar1) {
    (*(code *)PTR_DiscreteOutput_SetCommand_0001f5b0)(0,cStack_30 == '\x01');
    (*(code *)puVar2)(1,cVar8 == '\x01');
    (*(code *)puVar2)(2,cVar7 == '\x01');
    (*(code *)puVar2)(3,cVar6 == '\x01');
  }
  else {
    (*(code *)PTR_DiscreteOutput_SetCommand_0001f5b0)(0,cStack_30 == '\x01');
    (*(code *)puVar2)(1,cVar8 == '\x01');
    (*(code *)puVar2)(2,cVar7 == '\x01');
    (*(code *)puVar2)(3,cVar6 == '\x01');
  }
  (*(code *)puVar2)(4,cVar3 == '\x01');
  if (bVar1) {
    *(byte *)(int)DAT_0001f5ac = *(byte *)(int)DAT_0001f5ac & 0xfe;
  }
  else {
    *(byte *)(int)DAT_0001f5e6 = *(byte *)(int)DAT_0001f5e6 | 1;
  }
  return;
}

