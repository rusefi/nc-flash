/* Ghidra analysis output; verify against original SH instructions. */

/* Executed buffers5CC20:8FA8/90B8. Pendingerror
   builds7F/oldfirstbyte/error,length3;elseheader5CA3C+16row,lengtharg+1 wrap16.
   Setsstatusbit7,zeros90C0/C2/C4/C6. Trailingbytesretain; noactualtransmitproof. */

undefined * Diagnostic_ConstructResponseBuffer(uint param_1,short param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  byte *pbVar4;
  int iVar5;
  undefined1 *puVar6;
  
  puVar2 = PTR_DAT_0001d8f0;
  puVar1 = PTR_DAT_0001d8ec;
  puVar3 = PTR_DAT_0001d8d0;
  iVar5 = (param_1 & 0xff) * 2;
  puVar6 = *(undefined1 **)(PTR_Diagnostic_ResponseBufferPointers_0001d8e8 + (param_1 & 0xff) * 4);
  *(undefined2 *)PTR_DAT_0001d8e4 = 0;
  *(undefined2 *)puVar3 = 0;
  if (PTR_Diagnostic_FirstErrorBytes_0001d8f4[param_1 & 0xff] != '\0') {
    *(undefined2 *)puVar2 = 0;
    puVar3 = PTR_FUN_0001d8f8;
    *(undefined2 *)puVar1 = 0;
    (*(code *)puVar3)();
    puVar3 = PTR_FUN_0001d900;
    PTR_Diagnostic_ResponseRecordFlags_0001d8fc[iVar5] =
         PTR_Diagnostic_ResponseRecordFlags_0001d8fc[iVar5] | 0x80;
    (*(code *)puVar3)();
    puVar6[1] = *puVar6;
    *puVar6 = 0x7f;
    puVar3 = PTR_Diagnostic_ResponseLengthWords_0001d904;
    puVar6[2] = PTR_Diagnostic_FirstErrorBytes_0001d8f4[param_1 & 0xff];
    *(undefined2 *)(puVar3 + iVar5) = 3;
    return puVar3;
  }
  *(short *)(PTR_Diagnostic_ResponseLengthWords_0001da7c + iVar5) = param_2 + 1;
  puVar3 = PTR_FUN_0001da88;
  pbVar4 = PTR_DAT_0001da80 + iVar5;
  *puVar6 = PTR_Diagnostic_ServiceRecords_0001da84[(uint)*pbVar4 * 0x10];
  *(undefined2 *)puVar2 = 0;
  *(undefined2 *)puVar1 = 0;
  (*(code *)puVar3)();
  pbVar4[1] = pbVar4[1] | 0x80;
  puVar3 = (undefined *)(*(code *)PTR_FUN_0001da8c)();
  return puVar3;
}

