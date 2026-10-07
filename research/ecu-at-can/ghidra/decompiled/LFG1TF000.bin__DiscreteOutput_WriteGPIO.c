/* Ghidra analysis output; verify against original SH instructions. */

/* Fivechannels:exact8A1Cbyte1 setspositivepolaritydescriptorbit elseclears. PB6/PB7/PC4/PB5/PB4
   compatibleMCUmap; boardroleunknown. Exactorderedwordaccessesverified. See tcu-source-inhibit.txt.
    */

void DiscreteOutput_WriteGPIO(void)

{
  undefined *puVar1;
  char *pcVar2;
  char *pcVar3;
  undefined *puVar4;
  
  puVar1 = PTR_PortOutput_WriteDescriptor_0001874c;
  pcVar2 = (char *)(int)DAT_00018742;
  pcVar3 = pcVar2 + 5;
  puVar4 = PTR_DiscreteOutput_DescriptorTriples_00018748;
  do {
    (*(code *)puVar1)(*(undefined4 *)(puVar4 + 4),*pcVar2 == '\x01');
    pcVar2 = pcVar2 + 1;
    puVar4 = puVar4 + 0xc;
  } while (pcVar2 < pcVar3);
  return;
}

