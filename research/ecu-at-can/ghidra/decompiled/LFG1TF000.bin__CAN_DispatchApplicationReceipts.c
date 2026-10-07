/* Ghidra analysis output; verify against original SH instructions. */

/* Consumes8F71/pending8F4E bitmap using5C950/5C95C andcallbacks5CA10. Full126EC
   nowexecutes4EC/215/201 callbacks inlogicalorder1/6/8 afteroriginalISRprefixes;
   firstcomparisonusesold201.352tasks reachnumeric306/cleanup311. Not all10callbacks orhardware/RTE.
   See tcu-receive-admission.txt. */

void CAN_DispatchApplicationReceipts(void)

{
  byte bVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  ushort uVar7;
  
  puVar2 = PTR_DAT_0001bdbc;
  if ((*PTR_DAT_0001bdc0 != '\0') &&
     (*PTR_DAT_0001bdc0 = 0, puVar6 = PTR_DAT_0001bdd0, puVar5 = PTR_DAT_0001bdcc,
     puVar4 = PTR_FUN_0001bdc8, puVar3 = PTR_PTR_0001bdc4, (*puVar2 & 0xc) != 0)) {
    uVar7 = 0;
    do {
      if ((puVar6[uVar7] & PTR_DAT_0001bdd4[(byte)puVar5[uVar7]]) != 0) {
        (*(code *)PTR_FUN_0001bdd8)();
        bVar1 = puVar5[uVar7];
        PTR_DAT_0001bdd4[bVar1] = PTR_DAT_0001bdd4[bVar1] & ~puVar6[uVar7];
        (*(code *)puVar4)();
        (**(code **)(puVar3 + (uint)uVar7 * 4))();
      }
      uVar7 = uVar7 + 1;
    } while (uVar7 < 10);
  }
  return;
}

