/* Ghidra analysis output; verify against original SH instructions. */

/* Reads list6188, codeBE16 at5EB80+16*group, filter58398; emits code high/low andFF. Executed
   group36 emitsC1 00 FF before and after active recovery; transport not emulated. */

uint Diagnostic_SerializeStoredList(int param_1)

{
  short sVar1;
  char cVar2;
  uint uVar3;
  undefined1 *puVar4;
  uint uVar5;
  byte *pbVar6;
  byte bVar7;
  uint uVar8;
  
  uVar8 = 0;
  (*(code *)PTR_FUN_00055900)(param_1,0,(int)DAT_000558f2);
  bVar7 = 0;
  do {
    if (0x48 < bVar7) {
      return uVar8;
    }
    sVar1 = *(short *)(PTR_DAT_00055a34 + (uint)*(byte *)((uint)bVar7 + DAT_00055a30) * 0x10);
    if (sVar1 == 0) {
      return uVar8;
    }
    cVar2 = (*(code *)PTR_FUN_00055a38)();
    if (cVar2 == '\x01') {
      uVar5 = uVar8 & 0xff;
      uVar3 = 0;
      if (uVar5 != 0) {
        do {
          pbVar6 = (byte *)(param_1 + (uVar3 & 0xff) * 3);
          if (sVar1 == (ushort)((ushort)*pbVar6 * 0x100 + (ushort)pbVar6[1])) break;
          uVar3 = uVar3 + 1;
        } while ((uVar3 & 0xff) < uVar5);
      }
      if ((uVar3 & 0xff) == uVar5) {
        puVar4 = (undefined1 *)(param_1 + (uVar8 & 0xff) * 3);
        *puVar4 = (char)((ushort)sVar1 >> 8);
        uVar8 = uVar8 + 1;
        puVar4[1] = (char)sVar1;
        puVar4[2] = (char)DAT_00055a2a;
      }
    }
    bVar7 = bVar7 + 1;
  } while( true );
}

