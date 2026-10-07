/* Ghidra analysis output; verify against original SH instructions. */

/* Interleaveddescriptorreadback8A21 andexternalPADRfeedback8A26 forfivechannels;
   explicitread-onlysamples, noelectricalfeedbackproof. See tcu-source-inhibit.txt. */

void DiscreteOutput_ReadFeedback(void)

{
  undefined *puVar1;
  undefined1 uVar2;
  undefined1 *puVar3;
  undefined1 *puVar4;
  undefined1 *puVar5;
  undefined4 *puVar6;
  
  puVar1 = PTR_Input_ReadDigitalDescriptor_00018750;
  puVar5 = (undefined1 *)(int)DAT_00018740;
  puVar3 = (undefined1 *)(int)DAT_00018744;
  puVar4 = puVar3 + 5;
  puVar6 = (undefined4 *)PTR_DiscreteOutput_DescriptorTriples_00018748;
  do {
    uVar2 = (*(code *)puVar1)(*puVar6);
    *puVar3 = uVar2;
    uVar2 = (*(code *)puVar1)(puVar6[2]);
    puVar3 = puVar3 + 1;
    *puVar5 = uVar2;
    puVar5 = puVar5 + 1;
    puVar6 = puVar6 + 3;
  } while (puVar3 < puVar4);
  return;
}

