/* Ghidra analysis output; verify against original SH instructions. */

/* Executed initialized lists ->mode-sensitive signed merge ->record2 setter/reset ->80E4.841 merge
   cases,600 queue operations,60 CAN216/ECU paths. */

void SparkRequest_UpdateRecordTwo(void)

{
  short sVar1;
  short *psVar2;
  char *pcVar3;
  short local_18 [2];
  char acStack_14 [4];
  char acStack_10 [4];
  short asStack_c [4];
  
  sVar1 = DAT_0004c84c;
  local_18[0] = DAT_0004c84c;
  asStack_c[0] = DAT_0004c84c;
  acStack_14[0] = '\0';
  acStack_10[0] = '\0';
  SparkRequest_SelectFirstList(local_18,acStack_14);
  (*(code *)PTR_SparkRequest_SelectSecondList_0004c874)(asStack_c,acStack_10);
  psVar2 = (short *)(int)DAT_0004c850;
  *(short *)(int)DAT_0004c84e = local_18[0];
  *psVar2 = asStack_c[0];
  pcVar3 = (char *)(int)DAT_0004c854;
  *(char *)(int)DAT_0004c852 = acStack_14[0];
  *pcVar3 = acStack_10[0];
  if (acStack_14[0] == acStack_10[0]) {
    if ((asStack_c[0] <= local_18[0]) || (asStack_c[0] == DAT_0004c84c)) goto LAB_0004c81e;
  }
  else {
    if (acStack_10[0] != '\x01') goto LAB_0004c81e;
    acStack_14[0] = '\x01';
  }
  local_18[0] = asStack_c[0];
LAB_0004c81e:
  if (local_18[0] == sVar1) {
    (*(code *)PTR_SparkRequest_ResetRecord_0004c87c)(2);
  }
  else {
    (*(code *)PTR_SparkRequest_SetRecord_0004c878)(2,(int)local_18[0],(int)acStack_14[0]);
  }
  SparkRequest_RecordTwoSelectedValue = local_18[0];
  return;
}

