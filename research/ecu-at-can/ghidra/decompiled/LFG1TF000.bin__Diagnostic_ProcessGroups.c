/* Ghidra analysis output; verify against original SH instructions. */

/* RequiresA936==1; groups1..48(hex) choose callback5EB5C from record5EB78 byte0. Group36 callback1
   is56908. */

void Diagnostic_ProcessGroups(void)

{
  byte *pbVar1;
  undefined *puVar2;
  byte *pbVar3;
  int iVar4;
  
  puVar2 = PTR_PTR_000566dc;
  if (*(char *)(int)DAT_000566be == '\x01') {
    iVar4 = 1;
    pbVar3 = PTR_Diagnostic_GroupConfiguration_000566d8 + DAT_000566c8;
    pbVar1 = PTR_Diagnostic_GroupConfiguration_000566d8;
    while (pbVar1 = pbVar1 + 0x10, pbVar1 <= pbVar3) {
      if (*pbVar1 < 2) {
        (**(code **)(puVar2 + (uint)*pbVar1 * 4))(iVar4);
      }
      iVar4 = iVar4 + 1;
    }
  }
  return;
}

