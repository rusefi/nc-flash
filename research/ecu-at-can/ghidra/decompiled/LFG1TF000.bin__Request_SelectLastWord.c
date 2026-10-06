/* Ghidra analysis output; verify against original SH instructions. */

/* Walk signed-byte count r5, overwrite default r6 with each signed word !=7FFF. Returns LAST
   nonsentinel. Called1FB8C withcount5. */

int Request_SelectLastWord(short *param_1,char param_2,int param_3)

{
  short *psVar1;
  int iVar2;
  
  iVar2 = 0;
  psVar1 = param_1;
  if (0 < param_2) {
    do {
      iVar2 = iVar2 + 1;
      if (*psVar1 != DAT_0003070e) {
        param_3 = (int)*param_1;
      }
      param_1 = param_1 + 1;
      psVar1 = psVar1 + 1;
    } while (iVar2 < param_2);
  }
  return param_3;
}

