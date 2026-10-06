/* Ghidra analysis output; verify against original SH instructions. */

/* 65536 mode/configuration cases verify mode40 OR734C==0 packing. MT producer gives
   FF,flags,FF,FF,0,0,0,0 with flags bit2 from723A. Non-MT configuration0 can pack retained fields;
   not an unconditional MT conversion. See mt-can231.txt. */

void CAN231_PackWhenNonAT(void)

{
  undefined2 uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  char cVar4;
  
  uVar3 = (*(code *)PTR_FUN_00036e34)(0x10);
  if (((*PTR_TransmissionModeFlags_00036e1c & 0x40) != 0) ||
     (cVar4 = (*(code *)PTR_FUN_00036e24)(PTR_ATReceiveConfigurationGate_00036e20), cVar4 == '\0'))
  {
    puVar2 = PTR_DAT_00036e3c;
    uVar1 = *(undefined2 *)PTR_DAT_00036e38;
    *PTR_DAT_00036e3c = *PTR_DAT_00036e40;
    puVar2[1] = *PTR_CAN231_WorkingDiscreteByte_00036e44;
    puVar2[2] = (char)((ushort)uVar1 >> 8);
    puVar2[3] = (char)uVar1;
    puVar2[4] = 0;
    puVar2[5] = 0;
    puVar2[6] = 0;
    puVar2[7] = 0;
  }
  (*(code *)PTR_FUN_00036e48)(uVar3);
  return;
}

