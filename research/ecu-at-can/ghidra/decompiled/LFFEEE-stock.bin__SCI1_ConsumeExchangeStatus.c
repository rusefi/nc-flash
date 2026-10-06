/* Ghidra analysis output; verify against original SH instructions. */

/* Returns43A7 thenzeroesit undercriticalmask.1valid,2checksumfailure/abort,0nostatus. */

int SCI1_ConsumeExchangeStatus(void)

{
  undefined4 local_c;
  char cStack_8;
  
  (*(code *)PTR_FUN_0000c258)(&local_c,(int)DAT_0000c248);
  cStack_8 = *PTR_SCI1_ExchangeCompletion_0000c24c;
  *PTR_SCI1_ExchangeCompletion_0000c24c = 0;
  (*(code *)PTR_FUN_0000c25c)(local_c);
  return (int)cStack_8;
}

