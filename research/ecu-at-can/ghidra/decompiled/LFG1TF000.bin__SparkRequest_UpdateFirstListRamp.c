/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004d1d4) */
/* WARNING: Removing unreachable block (ram,0x0004d178) */
/* WARNING: Removing unreachable block (ram,0x0004d1f8) */
/* Executed unsigned16record+6*(duration-timer)/duration iftimer<duration,elsezero;then
   signed16lower clamp andsame92D5/9410gates. Positive mode1;7FFF is list sentinel. See
   tcu-request-maps.txt. */

void SparkRequest_UpdateFirstListRamp(undefined4 param_1,int param_2)

{
  byte bVar1;
  int iVar2;
  short sVar3;
  short sVar4;
  uint uVar5;
  undefined4 *puVar6;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  undefined4 uStack_24;
  int iStack_20;
  
  bVar1 = PTR_Request_RampTimerSlots_0004d268[*(byte *)(param_2 + 0xc)];
  iStack_20 = param_2;
  iVar2 = (*(code *)PTR_SparkRequest_SelectFirstListRampDuration_0004d26c)(param_2);
  uStack_24 = 0;
  uStack_28 = DAT_0004d24c;
  puVar6 = &uStack_28;
  sVar3 = (*(code *)PTR_FUN_0004d254)();
  uVar5 = (uint)sVar3;
  if ((int)(uint)bVar1 < iVar2) {
    uVar5 = (*(code *)PTR_FUN_0004d270)
                      ((iVar2 - (uint)bVar1 & 0xffff) * (uint)*(ushort *)(param_2 + 6),iVar2);
    uVar5 = uVar5 & 0xffff;
  }
  sVar3 = SparkRequest_ClampSignedNonnegative(uVar5);
  if (((*PTR_ApplicationFaultFlags92D5_0004d25c & 4) != 0) ||
     ((*PTR_Request_EnableFlags_0004d260 & 2) == 0)) {
    uStack_2c = 0;
    uStack_30 = DAT_0004d24c;
    puVar6 = &uStack_30;
    sVar3 = (*(code *)PTR_FUN_0004d254)();
  }
  *(short *)(param_2 + 4) = sVar3;
  *(undefined4 *)((int)puVar6 + -4) = 0;
  *(undefined4 *)((int)puVar6 + -8) = DAT_0004d24c;
  sVar4 = (*(code *)PTR_FUN_0004d254)();
  if (sVar4 < *(short *)(param_2 + 4)) {
    *(byte *)(param_2 + 0x12) = *(byte *)(param_2 + 0x12) | 0x80;
  }
  else {
    *(byte *)(param_2 + 0x12) = *(byte *)(param_2 + 0x12) & 0x7f;
  }
  (*(code *)PTR_SparkRequest_SetFirstListEntry_0004d264)
            ((int)*(char *)(param_2 + 2),(int)sVar3,
             -((((int)*(char *)(param_2 + 0x12) & 0x80U) == 0) - 1));
  return;
}

