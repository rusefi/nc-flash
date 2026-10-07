/* Ghidra analysis output; verify against original SH instructions. */

/* Executed writesR5lowbyte to90B4+R4lowbyte onlyifoldbytezero;validindex0/1 tested. */

void Diagnostic_RecordFirstError(byte param_1,char param_2)

{
  if (PTR_Diagnostic_FirstErrorBytes_0001d334[param_1] == '\0') {
    PTR_Diagnostic_FirstErrorBytes_0001d334[param_1] = param_2;
  }
  return;
}

