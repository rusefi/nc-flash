/* Ghidra analysis output; verify against original SH instructions. */

/* 768group36 state/input cases verifyreturn andunchangedwholeRAM. Requiresactivebit80
   and((state&6)==2 OR configbit0clear OR80A4==0). Nativehealthyreceiptsready116 but80A4nonzero
   retainsactive84. See tcu-receive-recovery.txt. */

undefined4 Diagnostic_CheckActiveRecoveryPermission(uint param_1)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if (((DAT_00056abc & (byte)PTR_DAT_00056acc[param_1 & 0xff]) == DAT_00056abc) &&
     (((((byte)PTR_DAT_00056acc[param_1 & 0xff] & 6) == 2 ||
       ((PTR_Diagnostic_GroupConfiguration_00056ac8[(param_1 & 0xff) * 0x10 + 6] & 1) != 1)) ||
      (DAT_ffff80a4 == 0)))) {
    uVar1 = 1;
  }
  return uVar1;
}

