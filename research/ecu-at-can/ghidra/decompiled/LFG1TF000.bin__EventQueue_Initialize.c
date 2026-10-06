/* Ghidra analysis output; verify against original SH instructions. */

/* Initializes count/head/tail of queueA1AC+3*index. Executed queue0. See tcu-request-dispatch.txt.
    */

void EventQueue_Initialize(byte param_1)

{
  undefined1 *puVar1;
  
  puVar1 = PTR_DAT_0004c3ac + (uint)param_1 * 3;
  *puVar1 = 0;
  puVar1[1] = 0;
  puVar1[2] = 0;
  return;
}

