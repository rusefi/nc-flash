/* Ghidra analysis output; verify against original SH instructions. */

/* Initialize five915C words7FFF, five9166 bytesFF,915A7FFF and80BE0. Original software-double
   helper executes; tcu-spark-requests.txt. */

void SparkRequest_InitializeRecords(void)

{
  (*(code *)PTR_FUN_0001fc08)((int)DAT_0001fc00,5,(int)DAT_0001fbfe);
  (*(code *)PTR_FUN_0001fc0c)((int)DAT_0001fc04,5,(int)DAT_0001fc02);
  SparkRequest_NegatedSelectedReduction = (*(code *)PTR_FUN_0001fc14)();
  *DAT_0001fc18 = DAT_0001fbfe;
  return;
}

