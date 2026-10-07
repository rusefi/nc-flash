/* Ghidra analysis output; verify against original SH instructions. */

/* Entryflags6165/66/67 snapshot;marksselectedgroup1;zeroOTHERflags
   allowweightedtrunc(value*weight/128) lowwordstores. NO+/-80spreadclamp. Produced[103,91,80]
   verified. Nonzeroflagsinhibitotherwrites. */

undefined4
ClassAdjustment_SpreadUnmarked
          (undefined1 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined1 *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar6;
  char cVar7;
  char cVar8;
  undefined4 uVar4;
  undefined4 uVar5;
  char cVar9;
  undefined3 in_stack_ffffffdd;
  
  puVar2 = PTR_StateCache_ReadByte_00036f8c;
  uVar5 = CONCAT13(param_1,in_stack_ffffffdd);
  cVar6 = (*(code *)PTR_StateCache_ReadByte_00036f8c)((int)DAT_00036f86);
  cVar7 = (*(code *)puVar2)((int)DAT_00036f88);
  cVar8 = (*(code *)puVar2)((int)DAT_00036f8a);
  puVar3 = PTR_Arithmetic_SaturatingMultiplyShift_00036f98;
  puVar2 = PTR_StoredWord_WriteAdjustment_00036f94;
  cVar9 = (char)((uint)uVar5 >> 0x18);
  if (cVar9 == '\0') {
    uVar4 = (*(code *)PTR_StateCache_WriteByte_00036f90)((int)DAT_00036f86,1);
    puVar1 = PTR_DAT_00036fa0;
    if (cVar7 == '\0') {
      uVar5 = (*(code *)puVar3)(param_2,*PTR_DAT_00036f9c,7);
      uVar4 = (*(code *)puVar2)(1,uVar5);
      puVar1 = PTR_DAT_00036fa0;
    }
  }
  else {
    if (cVar9 != '\x01') {
      uVar4 = (*(code *)PTR_StateCache_WriteByte_00036f90)((int)DAT_00036f8a,1);
      if (cVar6 == '\0') {
        uVar5 = (*(code *)puVar3)(param_2,*PTR_DAT_00036fac,7);
        uVar4 = (*(code *)puVar2)(0,uVar5);
      }
      if (cVar7 != '\0') {
        return uVar4;
      }
      uVar5 = (*(code *)puVar3)(param_2,*PTR_DAT_00036fb0,7,param_4,uVar5);
      uVar5 = (*(code *)puVar2)(1,uVar5);
      return uVar5;
    }
    uVar4 = (*(code *)PTR_StateCache_WriteByte_00036f90)((int)DAT_00036f88,1);
    puVar1 = PTR_DAT_00036fa8;
    if (cVar6 == '\0') {
      uVar5 = (*(code *)puVar3)(param_2,*PTR_DAT_00036fa4,7);
      uVar4 = (*(code *)puVar2)(0,uVar5);
      puVar1 = PTR_DAT_00036fa8;
    }
  }
  if (cVar8 == '\0') {
    uVar5 = (*(code *)puVar3)(param_2,*puVar1,7,param_4,uVar5);
    uVar4 = (*(code *)puVar2)(2,uVar5);
  }
  return uVar4;
}

