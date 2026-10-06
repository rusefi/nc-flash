/* Ghidra analysis output; verify against original SH instructions. */

/* Tailcalls2F5FC withA2B8/5E3F8. Events0 initialize,1 create,2 update active rings,3 cancel;
   complete queue lifecycle verified. See tcu-request-dispatch.txt. */

void SparkRequest_DispatchManager(undefined4 param_1,undefined4 param_2)

{
  (*DAT_0004c590)(param_1,param_2,PTR_DAT_0004c58c,PTR_SparkRequest_ManagerDescriptor_0004c588);
  return;
}

