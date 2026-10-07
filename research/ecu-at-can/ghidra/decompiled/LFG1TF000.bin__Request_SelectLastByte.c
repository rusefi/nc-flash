/* Ghidra analysis output; verify against original SH instructions. */

/* Walk signed-byte countR5; returnLAST nonFF byte ordefaultR6. Also executed1F3CE count11/default4
   afterdisabledslots4/6clear. See tcu-source-inhibit.txt andprior1FB8C count5. */

int Request_SelectLastByte(byte *param_1,char param_2,int param_3)

{
  byte *pbVar1;
  int iVar2;
  
  iVar2 = 0;
  pbVar1 = param_1;
  if (0 < param_2) {
    do {
      iVar2 = iVar2 + 1;
      if (*pbVar1 != DAT_0003070c) {
        param_3 = (int)(char)*param_1;
      }
      param_1 = param_1 + 1;
      pbVar1 = pbVar1 + 1;
    } while (iVar2 < param_2);
  }
  return param_3;
}

