/* Ghidra analysis output; verify against original SH instructions. */

/* Updates69E2 only if722A==1; any expired216/218/231/4C1 counter with734C==1 sets fault.
   Executed128 cases. */

char CAN_UpdateATReceiptFault(void)

{
  char cVar1;
  
  cVar1 = (*(code *)PTR_FUN_0003487c)(PTR_Control_FilteredModeInput_00034878);
  if (cVar1 == '\x01') {
    if (((((*PTR_CAN216_ReceiptCounter_00034894 == '\0') ||
          (*PTR_CAN218_ReceiptCounter_00034898 == '\0')) ||
         (*PTR_CAN231_ReceiptCounter_0003489c == '\0')) || (*PTR_DAT_000348a0 == '\0')) &&
       (cVar1 = (*(code *)PTR_FUN_0003487c)(PTR_ATReceiveConfigurationGate_000348a4),
       cVar1 == '\x01')) {
      *PTR_DAT_000348a8 = 1;
      return '\x01';
    }
    cVar1 = '\0';
    *PTR_DAT_000348a8 = 0;
  }
  return cVar1;
}

