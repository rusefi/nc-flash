/* Ghidra analysis output; verify against original SH instructions. */

/* Executed3054E ->A26E/A270 and output pointers; publishes wordA256/modeA254. */

void SparkRequest_SelectSecondList(undefined2 *param_1,undefined1 *param_2)

{
  ushort uVar1;
  
  (*(code *)PTR_RequestList_SelectCandidate_0004cb90)
            (PTR_DAT_0004cb78,PTR_SparkRequest_SecondListDescriptor_0004cb74,PTR_DAT_0004cb70,
             PTR_DAT_0004cb8c);
  uVar1 = DAT_0004cb6a;
  *param_1 = *(undefined2 *)PTR_DAT_0004cb70;
  if ((byte)*PTR_DAT_0004cb8c == uVar1) {
    *param_2 = 0;
  }
  else {
    *param_2 = *(undefined1 *)((uint)(byte)*PTR_DAT_0004cb8c + (int)DAT_0004cb66);
  }
  *PTR_DAT_0004cb94 = *param_2;
  *(undefined2 *)PTR_DAT_0004cb6c = *param_1;
  return;
}

