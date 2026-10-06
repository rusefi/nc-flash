/* Ghidra analysis output; verify against original SH instructions. */

/* ED1A read/writeBF then tailcallBFB4. Executedexplicitly;interruptsource scheduling/pins
   remainunverified. */

void SCI1_ByteCallbackInterruptStub(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_SCI1_ServiceCommandByte_0000e90c;
  *(undefined2 *)(int)DAT_0000e8e8 = DAT_0000e8ea;
  (*(code *)puVar1)();
  return;
}

