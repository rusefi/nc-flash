/* Ghidra analysis output; verify against original SH instructions. */

/* MAX(decoded6B3A,6718), re-encode then cap200;A3A4==1 ->FF.392 paired encoder cases; see
   can201-byte6.txt. */

char CAN201_SelectByte6(void)

{
  undefined *puVar1;
  byte bVar2;
  char cVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  
  uVar5 = 0;
  uVar6 = DAT_00036918;
  uVar4 = (*(code *)PTR_FUN_00036920)(DAT_00036918,0,(int)(char)*PTR_DAT_0003691c);
  uVar4 = (*(code *)PTR_FUN_00036928)(uVar4,*(undefined4 *)PTR_DAT_00036924);
  bVar2 = (*(code *)PTR_FUN_0003692c)(uVar4,uVar6,uVar5);
  puVar1 = PTR_DAT_00036930;
  cVar3 = (*(code *)PTR_FUN_00036938)(PTR_DAT_00036934);
  if (cVar3 == '\x01') {
    *puVar1 = (char)DAT_00036910;
  }
  else if (DAT_00036912 < (short)(ushort)bVar2) {
    *puVar1 = (char)DAT_00036912;
  }
  else {
    *puVar1 = bVar2;
  }
  return cVar3;
}

