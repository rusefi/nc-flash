/* Ghidra analysis output; verify against original SH instructions. */

/* Stock5C500 descriptor executes1421A/1423E withmask0; SRmasks0/3/15 preserved.
   Generalnonzerodescriptormask pathnotclaimed. See tcu-output-pin-switch.txt. */

void PortOutput_WriteDescriptor(int *param_1)

{
  if ((param_1 != (int *)0x0) && (*param_1 != 0)) {
    PortOutput_ModifyDescriptorBit(param_1);
  }
  return;
}

