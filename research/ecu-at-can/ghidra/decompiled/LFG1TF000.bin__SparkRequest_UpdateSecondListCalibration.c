/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004d9a4) */
/* Executed with valid allocated handle in synthetic callback record: stock773E8=0 publishes
   zero/mode0; physical entry conditions unproved. */

void SparkRequest_UpdateSecondListCalibration(undefined4 param_1,int param_2)

{
  undefined *UNRECOVERED_JUMPTABLE;
  short sVar1;
  byte bVar2;
  int iVar3;
  
  iVar3 = (int)*(short *)PTR_PTR_0004da38;
  sVar1 = (*(code *)PTR_FUN_0004da10)();
  if (sVar1 < iVar3) {
    bVar2 = *(byte *)(param_2 + 8) | 0x80;
  }
  else {
    sVar1 = (*(code *)PTR_FUN_0004da10)();
    iVar3 = (int)sVar1;
    bVar2 = *(byte *)(param_2 + 8) & 0x7f;
  }
  *(byte *)(param_2 + 8) = bVar2;
  UNRECOVERED_JUMPTABLE = PTR_SparkRequest_SetSecondListEntry_0004da34;
  *(short *)(param_2 + 2) = (short)iVar3;
                    /* WARNING: Could not recover jumptable at 0x0004da00. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)UNRECOVERED_JUMPTABLE)
            ((int)*(char *)(param_2 + 4),(int)*(short *)(param_2 + 2),
             -((((int)*(char *)(param_2 + 8) & 0x80U) == 0) - 1));
  return;
}

