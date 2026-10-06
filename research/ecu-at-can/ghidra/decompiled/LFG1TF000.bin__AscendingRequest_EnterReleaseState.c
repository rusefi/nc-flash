/* Ghidra analysis output; verify against original SH instructions. */

/* Copies currentword+4 into+6, ORs record+8bit20, returns4. Preservesbit40 andotherflags.1280
   allflag/value cases. Runsagain onsecondrelease; captured+6 isrefreshed evenwhenbit40alreadyset.
    */

undefined4 AscendingRequest_EnterReleaseState(undefined4 param_1,int param_2)

{
  *(undefined2 *)(param_2 + 6) = *(undefined2 *)(param_2 + 4);
  *(byte *)(param_2 + 8) = *(byte *)(param_2 + 8) | 0x20;
  return 4;
}

