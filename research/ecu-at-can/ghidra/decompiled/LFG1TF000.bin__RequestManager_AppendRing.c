/* Ghidra analysis output; verify against original SH instructions. */

/* Executed twelve-entry manager ring atA2BC; pointer,group,event,code,active marker. General
   overflow not verified here. See tcu-request-dispatch.txt. */

uint RequestManager_AppendRing
               (int param_1,int *param_2,undefined1 param_3,undefined1 param_4,undefined2 param_5,
               undefined1 param_6,undefined4 param_7)

{
  uint uVar1;
  short sVar2;
  int iVar3;
  
  uVar1 = (uint)*(char *)(param_1 + 2);
  if (uVar1 < (uint)(int)*(char *)(param_2 + 7)) {
    sVar2 = (*(code *)PTR_FUN_0002fb18)();
    iVar3 = sVar2 * 0xc;
    *(undefined1 *)(*param_2 + iVar3 + 6) = param_3;
    *(undefined1 *)(*param_2 + iVar3 + 7) = param_4;
    *(undefined2 *)(*param_2 + iVar3 + 4) = param_5;
    *(undefined1 *)(*param_2 + iVar3 + 8) = param_6;
    *(undefined4 *)(iVar3 + *param_2) = param_7;
    uVar1 = (int)*(char *)(param_1 + 2) + 1;
    *(char *)(param_1 + 2) = (char)uVar1;
  }
  return uVar1;
}

