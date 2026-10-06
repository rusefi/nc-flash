/* Ghidra analysis output; verify against original SH instructions. */

/* Executed3054E ->A242/A244; value80E2,modeA200 and output pointers. Empty mode0; all-sentinel mode
   comes from last entry. */

void SparkRequest_SelectFirstList(undefined2 *param_1,undefined1 *param_2)

{
  ushort uVar1;
  
  (*(code *)PTR_RequestList_SelectCandidate_0004c86c)
            (PTR_DAT_0004c85c,PTR_SparkRequest_FirstListDescriptor_0004c858,PTR_DAT_0004c868,
             PTR_DAT_0004c864);
  uVar1 = DAT_0004c84a;
  *param_1 = *(undefined2 *)PTR_DAT_0004c868;
  if ((byte)*PTR_DAT_0004c864 == uVar1) {
    *param_2 = 0;
  }
  else {
    *param_2 = *(undefined1 *)((uint)(byte)*PTR_DAT_0004c864 + (int)DAT_0004c846);
  }
  *PTR_DAT_0004c870 = *param_2;
  DAT_ffff80e2 = *param_1;
  return;
}

