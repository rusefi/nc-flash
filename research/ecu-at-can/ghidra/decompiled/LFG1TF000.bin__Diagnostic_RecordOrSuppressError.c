/* Ghidra analysis output; verify against original SH instructions. */

/* Executed currentindex90A7 state=(byte90AC+2index>>3)&3. State2+error!=22hex
   clearsbit1,targetcurrentor0ifalternate==1,returns0;elsestorefirsterror90B4+target,return2.
   Return0notnecessarilyadmitted. */

undefined4 Diagnostic_RecordOrSuppressError(uint param_1,char param_2)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  
  cVar1 = (*(code *)PTR_Diagnostic_ReadResponseMode_00054224)();
  iVar2 = (int)(char)*PTR_Diagnostic_CurrentRecordIndex_00054228;
  if ((cVar1 == '\x02') && ((param_1 & 0xff) != 0x22)) {
    if (param_2 == '\x01') {
      iVar2 = 0;
    }
    (*(code *)PTR_Diagnostic_ClearResponsePending_0005422c)(iVar2);
    uVar3 = 0;
  }
  else {
    if (param_2 == '\x01') {
      iVar2 = 0;
    }
    (*(code *)PTR_Diagnostic_RecordFirstError_00054230)(iVar2,param_1);
    uVar3 = 2;
  }
  return uVar3;
}

