/* Ghidra analysis output; verify against original SH instructions. */

/* Per-bitmajority ofnewrawR4,previousrawR5,previousfilteredatR6;storeviaextraargumentonstack.
   Calledsixchannelsby2291A. */

void SCI1_FilterReplyStatusByte
               (byte param_1,byte param_2,byte *param_3,undefined4 param_4,undefined1 *param_5)

{
  undefined *puVar1;
  
  puVar1 = PTR_DAT_0002355c;
  *PTR_DAT_0002355c = (*param_3 & (param_1 ^ param_2)) + (~(param_1 ^ param_2) & param_2);
  *param_5 = *puVar1;
  return;
}

