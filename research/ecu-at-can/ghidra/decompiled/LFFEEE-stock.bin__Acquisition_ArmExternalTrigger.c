/* Ghidra analysis output; verify against original SH instructions. */

/* Argumentzero selects ADCSR0/1=0B/4B, nonzero0A/4A; enables external triggers, clears ADST and
   setsTRGE, then404B=1. AllSR masks execute with boundedlatches; no hardwareconversion/delivery
   model. */

void Acquisition_ArmExternalTrigger(int param_1)

{
  undefined *puVar1;
  undefined1 *puVar2;
  byte *pbVar3;
  undefined1 *puVar4;
  byte *pbVar5;
  byte *pbVar6;
  byte *pbVar7;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24 [2];
  
  puVar1 = PTR_FUN_000053a8;
  puVar2 = (undefined1 *)(int)DAT_0000539c;
  pbVar3 = (byte *)(int)DAT_0000539e;
  puVar4 = (undefined1 *)(int)DAT_000053a0;
  pbVar5 = (byte *)(int)DAT_000053a2;
  pbVar6 = (byte *)(int)DAT_000053a4;
  pbVar7 = pbVar6 + -0x20;
  if (param_1 == 0) {
    (*(code *)PTR_FUN_000053ac)(local_24,(int)DAT_00005398);
    *pbVar7 = *pbVar7 & 0xdf;
    *puVar4 = 0xb;
    *pbVar5 = *pbVar5 & 0x7f | 0x80;
    *pbVar7 = *pbVar7 & 0xaf | 0x80;
    (*(code *)puVar1)(local_24[0]);
    (*(code *)PTR_FUN_000053ac)(&local_28,(int)DAT_00005398);
    *pbVar6 = *pbVar6 & 0xdf;
    *puVar2 = 0x4b;
    *pbVar3 = *pbVar3 & 0x7f | 0x80;
    *pbVar6 = *pbVar6 & 0xaf | 0x80;
  }
  else {
    (*(code *)PTR_FUN_000054f4)(&local_2c,(int)DAT_000054ea);
    *pbVar7 = *pbVar7 & 0xdf;
    *puVar4 = 10;
    *pbVar5 = *pbVar5 & 0x7f | 0x80;
    *pbVar7 = *pbVar7 & 0xaf | 0x80;
    (*(code *)puVar1)(local_2c);
    (*(code *)PTR_FUN_000054f4)(&local_30,(int)DAT_000054ea);
    *pbVar6 = *pbVar6 & 0xdf;
    *puVar2 = 0x4a;
    *pbVar3 = *pbVar3 & 0x7f | 0x80;
    *pbVar6 = *pbVar6 & 0xaf | 0x80;
    local_28 = local_30;
  }
  (*(code *)puVar1)(local_28);
  *DAT_000054f8 = 1;
  return;
}

