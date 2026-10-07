/* Ghidra analysis output; verify against original SH instructions. */

/* 8088 must equal2. Head phase0/1/2 returns1 even count0; otherwise anyzero ack in
   requiredgroups1..7 across count records. RequiredROM5D3BC+2 equals0.10336 directcases and actual
   native-task predicates/cache linkage; tcu-recovery-reference.txt. */

undefined4 Phase_HasPendingWork(void)

{
  char cVar1;
  bool bVar2;
  short sVar3;
  int iVar4;
  undefined4 uVar5;
  
  uVar5 = 0;
  if (Phase_DispatchState == '\x02') {
    cVar1 = PTR_Phase_RecordRing_000317dc
            [(short)(ushort)(byte)PTR_Phase_RecordRing_000317dc[DAT_000317d8] * 0xf + 0xd];
    if (((cVar1 == '\0') || (cVar1 == '\x01')) || (cVar1 == '\x02')) {
      uVar5 = 1;
    }
    else {
      bVar2 = false;
      iVar4 = 0;
      while ((iVar4 < (int)(uint)(byte)PTR_Phase_RecordRing_000317dc[DAT_000317da] && (!bVar2))) {
        sVar3 = 0;
        do {
          if ((PTR_Request_PeriodicGroupRecords_000317e0[sVar3 * 4 + 2] == '\0') &&
             (PTR_Phase_RecordRing_000317dc
              [(int)sVar3 +
               (short)((ushort)(byte)PTR_Phase_RecordRing_000317dc[DAT_000317d8] + (short)iVar4 +
                       0x10 & 0xf) * 0xf] == '\0')) {
            bVar2 = true;
            break;
          }
          sVar3 = sVar3 + 1;
        } while (sVar3 < 10);
        iVar4 = iVar4 + 1;
      }
      if (bVar2) {
        uVar5 = 1;
      }
    }
  }
  return uVar5;
}

