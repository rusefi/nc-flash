/* Ghidra analysis output; verify against original SH instructions. */

/* Per-record duration+22/count+24 or second duration interval+8 times multiplier+25. State2 arms;
   unsigned deadline equality qualifies. RecordFF alternative not tested; tick units unresolved. */

bool CAN_UpdateQualificationTimer
               (char param_1,char param_2,char *param_3,uint *param_4,ushort *param_5,byte param_6,
               char param_7,byte param_8)

{
  ushort uVar1;
  uint uVar2;
  byte bVar3;
  uint uVar4;
  ushort uVar5;
  bool bVar6;
  
  uVar2 = (*(code *)PTR_Tick_Read_0001aa70)();
  uVar5 = DAT_0001aa6e;
  bVar6 = false;
  if (param_7 == '\x01') {
    if (param_8 == DAT_0001aa6e) {
      bVar3 = FUN_0001a4b2((int)(char)PTR_Diagnostic_GroupConfiguration_0001aa78
                                      [(uint)param_6 * 0x10 + 0xc]);
      if (bVar3 == uVar5) {
        uVar4 = 0;
        uVar5 = 0;
        *param_3 = '\x02';
        *param_5 = 0;
      }
      else {
        uVar4 = (uint)*(ushort *)
                       (PTR_Diagnostic_HealthyConfiguration_0001aa7c + (uint)bVar3 * 8 + 4);
        uVar5 = *(ushort *)(PTR_Diagnostic_HealthyConfiguration_0001aa7c + (uint)bVar3 * 8 + 6);
      }
    }
    else {
      uVar4 = (uint)*(ushort *)(PTR_CAN_RecordConfiguration_0001aa74 + (uint)param_8 * 0x1c + 8) *
              (uint)(byte)PTR_CAN_RecordConfiguration_0001aa74[(uint)param_8 * 0x1c + 0x19];
      uVar5 = 1;
    }
  }
  else if (param_8 == DAT_0001aa6e) {
    uVar4 = (uint)*(ushort *)(PTR_Diagnostic_GroupConfiguration_0001aa78 + (uint)param_6 * 0x10 + 2)
    ;
    uVar5 = *(ushort *)(PTR_Diagnostic_GroupConfiguration_0001aa78 + (uint)param_6 * 0x10 + 4);
  }
  else {
    uVar4 = (uint)*(ushort *)(PTR_CAN_RecordConfiguration_0001aa74 + (uint)param_8 * 0x1c + 0x16);
    uVar5 = (ushort)(byte)PTR_CAN_RecordConfiguration_0001aa74[(uint)param_8 * 0x1c + 0x18];
  }
  if ((param_1 == '\0') || (param_2 == '\0')) {
    *param_3 = '\x02';
    *param_5 = 0;
  }
  else {
    if (*param_3 == '\x02') {
      *param_3 = '\x01';
      *param_4 = uVar2 + uVar4;
    }
    if (((*param_3 == '\x01') && (*param_4 <= uVar2)) || (*param_3 == '\0')) {
      uVar1 = *param_5;
      if (uVar1 < uVar5) {
        *param_5 = *param_5 + 1;
        *param_3 = '\x01';
        *param_4 = *param_4 + uVar4;
      }
      if (*param_5 < uVar5) {
        return uVar1 < uVar5;
      }
      *param_3 = '\0';
    }
    else if (*param_5 == 0) {
      return false;
    }
    bVar6 = true;
  }
  return bVar6;
}

