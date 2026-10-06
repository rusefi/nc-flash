/* Ghidra analysis output; verify against original SH instructions. */

/* Searches95D4 fifteen-byte records with96C4 head/96C5 count,codefield+10. Executed matching
   phasefixtures; complete producer lifecycle open. See tcu-request-dispatch.txt. */

int ApplicationPhase_FindCode(ushort param_1)

{
  int iVar1;
  ushort uVar2;
  
  iVar1 = 0;
  while( true ) {
    if ((int)(uint)(byte)PTR_Phase_RecordRing_000320c0[DAT_000320b6] <= iVar1) {
      return -1;
    }
    uVar2 = (ushort)(byte)PTR_Phase_RecordRing_000320c0[DAT_000320b4] + (short)iVar1 + 0x10 & 0xf;
    if ((byte)PTR_Phase_RecordRing_000320c0[(short)uVar2 * 0xf + 10] == param_1) break;
    iVar1 = iVar1 + 1;
  }
  return (int)(short)uVar2;
}

