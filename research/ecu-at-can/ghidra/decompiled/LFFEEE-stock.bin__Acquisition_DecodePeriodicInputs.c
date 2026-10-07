/* Ghidra analysis output; verify against original SH instructions. */

/* Updates6C94/96/CAC/CA0/CA2/CA4/CA6 frombank4008;otherfieldsretain. Fullbody executed,
   allbytes6C90..6CAF compared. */

void Acquisition_DecodePeriodicInputs(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  
  puVar3 = PTR_DAT_0003997c;
  puVar1 = PTR_Acquisition_ADCResultBank_00039960;
  *(ushort *)PTR_DAT_00039978 = *(ushort *)(PTR_Acquisition_ADCResultBank_00039960 + 0xe) >> 6;
  puVar2 = PTR_Acquisition_Channel8HighByte_00039974;
  *(ushort *)puVar3 = *(ushort *)(puVar1 + 0x1c) >> 6;
  puVar3 = PTR_DAT_00039990;
  *puVar2 = (char)((ushort)*(undefined2 *)(puVar1 + 0x10) >> 8);
  *(ushort *)puVar3 = *(ushort *)(puVar1 + 0x22) >> 6;
  *(ushort *)PTR_DAT_00039994 = *(ushort *)(puVar1 + 0x24) >> 6;
  puVar2 = PTR_DAT_0003999c;
  *(ushort *)PTR_DAT_00039998 = *(ushort *)(puVar1 + 8) >> 6;
  *(ushort *)puVar2 = *(ushort *)(puVar1 + 10) >> 6;
  return;
}

