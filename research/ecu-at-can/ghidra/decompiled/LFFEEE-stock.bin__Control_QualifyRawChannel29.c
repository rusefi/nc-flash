/* Ghidra analysis output; verify against original SH instructions. */

/* 6CAE<8 or>248 with914B exact1 sets low/high flags8F31/32.9462 exact1 clears8F37; else
   inclusive8..248 sets8F37/38=1 independent914B.4096 cases. See control-raw-provenance.txt. */

char Control_QualifyRawChannel29(void)

{
  byte bVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar4;
  
  bVar1 = *PTR_DAT_0006d960;
  cVar4 = *PTR_DAT_0006d964;
  if ((bVar1 < (byte)*PTR_DAT_0006d96c) && (cVar4 == '\x01')) {
    *PTR_DAT_0006d968 = 1;
  }
  else {
    *PTR_DAT_0006d968 = 0;
  }
  if (((byte)*PTR_DAT_0006d974 < bVar1) && (cVar4 == '\x01')) {
    *PTR_DAT_0006d970 = 1;
  }
  else {
    *PTR_DAT_0006d970 = 0;
  }
  puVar3 = PTR_FUN_0006d980;
  puVar2 = PTR_DAT_0006d97c;
  *PTR_DAT_0006d978 = 0;
  cVar4 = (*(code *)puVar3)(puVar2);
  puVar2 = PTR_DAT_0006d978;
  if (cVar4 == '\x01') {
    *PTR_DAT_0006d984 = 0;
  }
  else if (((byte)*PTR_DAT_0006d96c <= bVar1) && (bVar1 <= (byte)*PTR_DAT_0006d974)) {
    *PTR_DAT_0006d984 = 1;
    *puVar2 = 1;
  }
  return cVar4;
}

