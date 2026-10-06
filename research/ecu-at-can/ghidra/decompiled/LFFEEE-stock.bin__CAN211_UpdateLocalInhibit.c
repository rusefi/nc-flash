/* Ghidra analysis output; verify against original SH instructions. */

/* 7190 combines nine byte gates and float6A38/6A3C >65536;2048 Boolean combinations executed.
   Physical gate identities unresolved. */

undefined4 * CAN211_UpdateLocalInhibit(void)

{
  undefined *puVar1;
  char cVar4;
  undefined4 *puVar2;
  uint uVar3;
  
  puVar1 = PTR_FUN_0003fe48;
  cVar4 = (*(code *)PTR_FUN_0003fe48)(PTR_DAT_0003fe4c);
  puVar2 = (undefined4 *)0x1;
  if ((((((cVar4 != '\x01') && (puVar2 = (undefined4 *)0x1, *PTR_DAT_0003fe50 != '\x01')) &&
        (puVar2 = (undefined4 *)0x1, *PTR_DAT_0003fe54 != '\x01')) &&
       ((puVar2 = (undefined4 *)0x1, *PTR_DAT_0003fe58 != '\x01' &&
        (puVar2 = (undefined4 *)0x1, *PTR_DAT_0003fe5c != '\x01')))) &&
      ((puVar2 = (undefined4 *)0x1, *PTR_DAT_0003fe60 != '\x01' &&
       ((puVar2 = &DAT_0003fe64, *(float *)PTR_DAT_0003fe68 <= DAT_0003fe64 &&
        (puVar2 = &DAT_0003fe64, *(float *)PTR_DAT_0003fe6c <= DAT_0003fe64)))))) &&
     (puVar2 = (undefined4 *)0x1, *PTR_DAT_0003fe70 != '\x01')) {
    uVar3 = (*(code *)puVar1)(PTR_DAT_0003fe74);
    puVar2 = (undefined4 *)(uVar3 & 0xff);
    if (puVar2 == (undefined4 *)0x0) {
      cVar4 = (*(code *)puVar1)(PTR_DAT_0003fe78);
      puVar2 = (undefined4 *)0x1;
      if (cVar4 != '\x01') {
        *PTR_DAT_0003fe7c = 0;
        return (undefined4 *)0x0;
      }
    }
  }
  *PTR_DAT_0003fe7c = 1;
  return puVar2;
}

