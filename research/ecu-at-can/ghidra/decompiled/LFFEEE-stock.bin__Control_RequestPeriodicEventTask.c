/* Ghidra analysis output; verify against original SH instructions. */

/* DAE8bank1/index10 row11344 selector2/zeroargs/targetE5FC ->queue2/task3/DC2C. Originaltimer calls
   everyfifth1062E invocation; 600drainsPASS,120event2requests.1488queue2producerwholeRAMcases
   include48emptyadmissions/48fullrejections; task3priority2. Fourunusedstackwords copied,
   R4argumentnotcopied. control-timer-event2.txt. */

undefined4 Control_RequestPeriodicEventTask(undefined4 param_1)

{
  undefined4 uVar1;
  undefined4 local_8 [2];
  
  local_8[0] = param_1;
  uVar1 = (*(code *)PTR_Control_DispatchDescriptorEvent_0000fcf0)(1,10,local_8);
  return uVar1;
}

