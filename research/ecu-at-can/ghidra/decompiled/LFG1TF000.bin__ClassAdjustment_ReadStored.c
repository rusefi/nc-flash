/* Ghidra analysis output; verify against original SH instructions. */

/* Knownclass0..2 table5D7F8=[0,1,2] ->24584signedword.Usedby36A74/36B26;
   exactstoredproduction/consumptionverified. */

int ClassAdjustment_ReadStored(int param_1)

{
  short sVar1;
  
  sVar1 = (*(code *)PTR_StoredWord_ReadSignedAdjustment_00036e64)
                    ((int)*(short *)(PTR_DAT_00036e60 + param_1 * 2));
  return (int)sVar1;
}

