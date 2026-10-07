/* Ghidra analysis output; verify against original SH instructions. */

/* q/remainder fromunsignedwordinput/step; exactknot ornextFFFF returnscurrentword; otherwise
   signedtruncatedinterpolation.913validchannelrangechecks; notablelengthvalidation. */

int Lookup_UniformWordStep(int param_1,int param_2,uint param_3)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  short *psVar5;
  int iVar6;
  
  uVar1 = param_3 & 0xffff;
  uVar2 = (*(code *)PTR_FUN_0001075c)();
  iVar6 = (param_3 & 0xffff) * (uVar2 & 0xffff);
  uVar3 = param_1 - iVar6;
  psVar5 = (short *)((uVar2 & 0xffff) * 2 + param_2);
  if (((uVar3 & 0xffff) == 0) ||
     ((undefined *)(uint)*(ushort *)((uVar2 & 0xffff) * 2 + param_2 + 2) == PTR_DAT_00010760)) {
    iVar6 = (int)*psVar5;
  }
  else {
    iVar4 = (int)*psVar5;
    iVar6 = (*(code *)PTR_FUN_0001075c)(uVar3,iVar4,iVar6,uVar2,uVar1);
    iVar6 = iVar6 + iVar4;
  }
  return iVar6;
}

