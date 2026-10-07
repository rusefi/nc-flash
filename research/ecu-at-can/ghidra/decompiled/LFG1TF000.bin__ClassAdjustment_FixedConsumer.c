/* Ghidra analysis output; verify against original SH instructions. */

/* Stock77173=2 selectsword2,*16,signed16saturation via10DD2/10E80. Doesnotapply+/-80clamp.
   ExistingSHExtractneededat5B8AA;fullreturnverified. */

int ClassAdjustment_FixedConsumer(void)

{
  short sVar2;
  int iVar1;
  int iVar3;
  
  sVar2 = (*(code *)PTR_StoredWord_ReadSignedAdjustment_00036a60)
                    ((int)*(short *)(PTR_DAT_00036a5c + (uint)(byte)*PTR_DAT_00036a58 * 2));
  iVar3 = (int)sVar2 << 4;
  if (iVar3 < 0) {
    iVar1 = (*(code *)PTR_FUN_00036a68)(iVar3,DAT_00036a64);
    iVar3 = DAT_00036a64;
  }
  else {
    iVar1 = (*(code *)PTR_FUN_00036a6c)(iVar3,DAT_00036a64);
    iVar3 = DAT_00036a70;
  }
  return iVar3 + iVar1;
}

