/* Ghidra analysis output; verify against original SH instructions. */

/* 7191: config734E=0 uses69E1; config1 uses7265/7266. 24 original-code combinations verified; stock
   config meaning unresolved. */

char CAN211_UpdateConfigInhibit(void)

{
  char cVar1;
  char cVar2;
  
  cVar2 = *PTR_DAT_0003fc44;
  if (((cVar2 == '\0') && (cVar1 = '\x01', *PTR_CAN_OtherReceiptFault_0003fc4c == '\x01')) ||
     ((cVar2 == '\x01' &&
      ((cVar1 = '\x01', *PTR_DAT_0003fc50 == '\x01' ||
       (cVar2 = *PTR_DAT_0003fc54, cVar1 = cVar2, cVar2 == '\x01')))))) {
    cVar2 = cVar1;
    *PTR_DAT_0003fc48 = 1;
  }
  else {
    *PTR_DAT_0003fc48 = 0;
  }
  return cVar2;
}

