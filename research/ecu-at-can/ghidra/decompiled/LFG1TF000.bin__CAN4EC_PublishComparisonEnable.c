/* Ghidra analysis output; verify against original SH instructions. */

/* Raw buffer8F0D byte0bit2 ->88C4 Boolean;88C5=2 unconditionally.256 byte cases. Sender/physical
   role/transport admission unproved; tcu-comparison-input.txt. */

void CAN4EC_PublishComparisonEnable(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_CAN4EC_ComparisonEnableStatus_00017614;
  *PTR_CAN4EC_ComparisonEnable_00017610 = (*PTR_DAT_00017618 & 4) != 0;
  *puVar1 = 2;
  return;
}

