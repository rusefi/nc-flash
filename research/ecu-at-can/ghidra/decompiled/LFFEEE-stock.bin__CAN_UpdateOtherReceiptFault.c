/* Ghidra analysis output; verify against original SH instructions. */

/* Updates69E1 only if722A==1; any expired6B04/6A1E/6AB4 with7353==1 sets fault, else clears.
   Executed64 cases. */

undefined * CAN_UpdateOtherReceiptFault(void)

{
  uint uVar1;
  undefined *puVar2;
  
  uVar1 = (*(code *)PTR_FUN_0003487c)(PTR_DAT_00034878);
  puVar2 = (undefined *)(uVar1 & 0xff);
  if (puVar2 == (undefined *)0x1) {
    if ((((*PTR_DAT_00034884 == '\0') || (*PTR_DAT_00034888 == '\0')) ||
        (puVar2 = PTR_CAN21A_ReceiptCounter_0003488c, *PTR_CAN21A_ReceiptCounter_0003488c == '\0'))
       && (puVar2 = (undefined *)(uint)(byte)*PTR_CAN4B0_SelectionEnabled_00034890,
          puVar2 == (undefined *)0x1)) {
      *PTR_CAN_OtherReceiptFault_00034880 = 1;
    }
    else {
      *PTR_CAN_OtherReceiptFault_00034880 = 0;
    }
  }
  return puVar2;
}

