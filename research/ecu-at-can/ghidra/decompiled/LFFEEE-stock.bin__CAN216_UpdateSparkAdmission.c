/* Ghidra analysis output; verify against original SH instructions. */

/* 6E2F requires6566=65DD=6530=protected700E=1,6531=8EF8=8F30=protectedA3A4=8F4B=0.512 combinations;
   physical gate identities open. */

uint CAN216_UpdateSparkAdmission(void)

{
  uint uVar1;
  
  uVar1 = (uint)(byte)*PTR_DAT_0003b038;
  if ((((uVar1 == 1) && (uVar1 = (uint)(byte)*PTR_DAT_0003b03c, uVar1 == 1)) &&
      (uVar1 = (uint)(byte)*PTR_DAT_0003b040, uVar1 == 1)) &&
     (uVar1 = (uint)(char)*PTR_DAT_0003b044, uVar1 == 0)) {
    uVar1 = (*(code *)PTR_FUN_0003b04c)(PTR_DAT_0003b048);
    uVar1 = uVar1 & 0xff;
    if (((uVar1 == 1) && (*PTR_DAT_0003b050 == '\0')) &&
       (uVar1 = (uint)(char)*PTR_DAT_0003b054, uVar1 == 0)) {
      uVar1 = (*(code *)PTR_FUN_0003b04c)(PTR_DAT_0003b058);
      uVar1 = uVar1 & 0xff;
      if ((uVar1 == 0) && (*PTR_DAT_0003b05c == '\0')) {
        *PTR_CAN216_SparkAdmission_0003b060 = 1;
        return 1;
      }
    }
  }
  *PTR_CAN216_SparkAdmission_0003b060 = 0;
  return uVar1;
}

