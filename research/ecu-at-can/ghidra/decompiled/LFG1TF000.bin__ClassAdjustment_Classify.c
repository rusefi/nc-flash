/* Ghidra analysis output; verify against original SH instructions. */

/* SIGNED80EE arithmetic>>7;24..31->0,32..39->1,40..48->2,else127.1536boundarycases.
   Units/naturalproductionnotinferred. */

undefined4 ClassAdjustment_Classify(void)

{
  int iVar1;
  undefined4 uVar2;
  
  iVar1 = (*(code *)PTR_FUN_00036e7c)();
  if ((iVar1 < (int)(uint)(byte)*PTR_DAT_00036e80) || ((int)(uint)(byte)*PTR_DAT_00036e84 < iVar1))
  {
    uVar2 = 0x7f;
  }
  else {
    uVar2 = 2;
    if (iVar1 < (int)(uint)(byte)*PTR_DAT_00036e88) {
      uVar2 = 1;
    }
    if (iVar1 < (int)(uint)(byte)*PTR_DAT_00036e8c) {
      uVar2 = 0;
    }
  }
  return uVar2;
}

