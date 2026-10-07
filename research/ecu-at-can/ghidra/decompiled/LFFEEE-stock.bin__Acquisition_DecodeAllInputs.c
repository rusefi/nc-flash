/* Ghidra analysis output; verify against original SH instructions. */

/* Original32word RAM4008 bank ->17fields6C90..6CAE;6CAC=wordchannel8>>8.1224decoder checks
   incontrol-acquisition.txt includespartial39894. ADCsourcecopyexecuted;physicalunitsunassigned. */

void Acquisition_DecodeAllInputs(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  
  puVar2 = PTR_DAT_00039968;
  puVar1 = PTR_Acquisition_ADCResultBank_00039960;
  *(ushort *)PTR_DAT_00039964 = *(ushort *)(PTR_Acquisition_ADCResultBank_00039960 + 6) >> 6;
  *(ushort *)puVar2 = *(ushort *)(puVar1 + 0x38) >> 6;
  *PTR_DAT_0003996c = (char)((ushort)*(undefined2 *)(puVar1 + 0x3a) >> 8);
  puVar2 = PTR_Acquisition_Channel8HighByte_00039974;
  *PTR_DAT_00039970 = (char)((ushort)*(undefined2 *)(puVar1 + 0x1a) >> 8);
  *puVar2 = (char)((ushort)*(undefined2 *)(puVar1 + 0x10) >> 8);
  puVar2 = PTR_DAT_0003997c;
  *(ushort *)PTR_DAT_00039978 = *(ushort *)(puVar1 + 0xe) >> 6;
  puVar3 = PTR_DAT_00039980;
  *(ushort *)puVar2 = *(ushort *)(puVar1 + 0x1c) >> 6;
  *(ushort *)puVar3 = *(ushort *)(puVar1 + 0x3c) >> 6;
  *(undefined2 *)PTR_DAT_00039984 = *(undefined2 *)(puVar1 + 0x3e);
  puVar2 = PTR_DAT_0003998c;
  *(ushort *)PTR_DAT_00039988 = *(ushort *)(puVar1 + 4) >> 6;
  puVar3 = PTR_DAT_00039990;
  *(ushort *)puVar2 = *(ushort *)(puVar1 + 4) >> 6;
  *(ushort *)puVar3 = *(ushort *)(puVar1 + 0x22) >> 6;
  *(ushort *)PTR_DAT_00039994 = *(ushort *)(puVar1 + 0x24) >> 6;
  puVar2 = PTR_DAT_0003999c;
  *(ushort *)PTR_DAT_00039998 = *(ushort *)(puVar1 + 8) >> 6;
  puVar3 = PTR_DAT_000399a0;
  *(ushort *)puVar2 = *(ushort *)(puVar1 + 10) >> 6;
  *(ushort *)puVar3 = *(ushort *)(puVar1 + 0x26) >> 6;
  *DAT_000399a4 = *(ushort *)(puVar1 + 0x20) >> 6;
  return;
}

