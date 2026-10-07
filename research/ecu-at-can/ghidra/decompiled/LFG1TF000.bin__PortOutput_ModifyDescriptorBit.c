/* Ghidra analysis output; verify against original SH instructions. */

/* Readsdescriptorwordtarget, calls1423E andwrites result. StockF74E bit14/polarity0
   independentlyverified. See tcu-output-pin-switch.txt. */

void PortOutput_ModifyDescriptorBit(undefined4 *param_1,uint param_2)

{
  undefined2 uVar1;
  
  uVar1 = PortOutput_SelectBitValue
                    ((int)*(short *)*param_1,(int)*(char *)(param_1 + 1),
                     (int)*(char *)((int)param_1 + 5),param_2 & 1);
  *(undefined2 *)*param_1 = uVar1;
  return;
}

