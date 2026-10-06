/* Ghidra analysis output; verify against original SH instructions. */

/* Executed search of12-entry ring usingA2B8/5E3F8 descriptor,compare record+6 with event argument;
   returns matching ring index orFF.36 successful constructor fixtures; missing-event handling not
   verified. */

int CallbackQueue_FindEventIndex(int param_1,int *param_2,char param_3)

{
  char cVar1;
  int iVar2;
  
  iVar2 = 0;
  while( true ) {
    if ((int)(uint)*(byte *)(param_1 + 2) <= iVar2) {
      return -1;
    }
    cVar1 = (*(code *)PTR_FUN_0002fdd4)();
    if (*(char *)(cVar1 * 0xc + *param_2 + 6) == param_3) break;
    iVar2 = iVar2 + 1;
  }
  return (int)cVar1;
}

