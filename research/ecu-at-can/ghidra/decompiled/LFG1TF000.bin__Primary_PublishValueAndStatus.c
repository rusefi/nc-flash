/* Ghidra analysis output; verify against original SH instructions. */

/* A500=floor(809A*10/256) over produced0..25600;A5024 if92D5bit7,else1 if880E2,else2. Modeled
   insidewhole22F46. */

uint Primary_PublishValueAndStatus(void)

{
  char cVar1;
  byte bVar2;
  undefined2 uVar3;
  
  uVar3 = (*(code *)PTR_FUN_00050fc8)();
  *(undefined2 *)PTR_Primary_PublishedValue_00050fc0 = uVar3;
  cVar1 = *PTR_ApplicationFaultFlags92D5_00050fcc;
  if (((int)cVar1 & 0x80U) != 0) {
    *PTR_Primary_PublishedStatus_00050fc4 = 4;
    return (int)cVar1;
  }
  bVar2 = *PTR_CAN215_PrimaryValidity_00050fd0;
  if (bVar2 == 2) {
    *PTR_Primary_PublishedStatus_00050fc4 = 1;
    return 1;
  }
  *PTR_Primary_PublishedStatus_00050fc4 = 2;
  return (uint)bVar2;
}

