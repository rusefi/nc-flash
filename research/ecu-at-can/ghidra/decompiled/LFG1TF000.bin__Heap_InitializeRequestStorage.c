/* Ghidra analysis output; verify against original SH instructions. */

/* Initialize9F3C free block with127 four-byte payload units andFF links; executed before request
   lifecycle. See tcu-request-dispatch.txt. */

void Heap_InitializeRequestStorage(void)

{
  undefined *puVar1;
  undefined1 *puVar2;
  undefined1 *puVar3;
  
  puVar1 = PTR_DAT_0004bff0;
  puVar3 = (undefined1 *)(int)DAT_0004bfea;
  puVar2 = (undefined1 *)(int)DAT_0004bfec;
  *PTR_DAT_0004bff0 = 0;
  puVar1[1] = 0x7f;
  puVar1[2] = 0xff;
  puVar1[3] = 0xff;
  *puVar3 = 0;
  *puVar2 = 0;
  return;
}

