/* Ghidra analysis output; verify against original SH instructions. */

/* Executed:constructA688/A68C pointer,A690 word;54AFC result->A694;tail1D94C. Stockrow3 header44.
   SAE04 diagnostic-clear interpretation, not operational shiftqueue. tcu-pulse-response.txt. */

void Diagnostic_WrapPulseClearRequest(undefined4 param_1,undefined2 param_2)

{
  undefined4 *puVar1;
  code *UNRECOVERED_JUMPTABLE;
  char *pcVar2;
  undefined4 uVar3;
  
  UNRECOVERED_JUMPTABLE = pcRam00053c9c;
  puVar1 = DAT_00053c98;
  *DAT_00053c98 = param_1;
  puVar1[1] = param_1;
  *(undefined2 *)(puVar1 + 2) = param_2;
  uVar3 = (*UNRECOVERED_JUMPTABLE)(puVar1);
  UNRECOVERED_JUMPTABLE = pcRam00053ca4;
  pcVar2 = pcRam00053ca0;
  *(short *)(int)DAT_00053c94 = (short)uVar3;
                    /* WARNING: Could not recover jumptable at 0x00053b7a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)((int)*pcVar2,uVar3);
  return;
}

