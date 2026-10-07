/* Ghidra analysis output; verify against original SH instructions. */

/* 256wholeRAM/exact18MMIO/registercases PASS.
   F401bit6start,F480bit10clear,F482bit10enable,F4EBmode1,F4E0=0,F4E2=625. Executedinsidefull11FA0.
   Original1669A IRQ/gate verified; conditional20000Pphi period fromPSCR1=1/TCR5=4. No hardware
   timing proof. tcu-hcan-startup.txt; tcu-can-task-interrupt.txt. */

void CANTimer_InitializeCompare(void)

{
  ushort *puVar1;
  byte *pbVar2;
  byte *pbVar3;
  
  pbVar3 = (byte *)(int)DAT_000166fe;
  *pbVar3 = *pbVar3 & 0xbf;
  puVar1 = (ushort *)(int)DAT_00016700;
  *puVar1 = *puVar1 & (ushort)PTR_DAT_0001670c;
  puVar1[1] = puVar1[1] | DAT_00016702;
  pbVar2 = (byte *)((int)puVar1 + 0x6b);
  *pbVar2 = *pbVar2 & 0xf7;
  *pbVar2 = *pbVar2 & 0xfb;
  *pbVar2 = *pbVar2 & 0xfd;
  *pbVar2 = *pbVar2 | 1;
  *(undefined2 *)(int)DAT_00016704 = 0;
  *(undefined2 *)(int)DAT_00016708 = DAT_00016706;
  *pbVar3 = *pbVar3 | 0x40;
  return;
}

