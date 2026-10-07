/* Ghidra analysis output; verify against original SH instructions. */

/* 3584cases PASS:readF718word/clearbit80 then1062E unconditionally, including
   suppliedstatuswithout80. NotIRQadmissiongate/hardwarevectorproof.
   Full600originaltimer/schedulerdrains PASS; control-timer-event2.txt. */

void Control_Cmt1TimerCallback(void)

{
  *(ushort *)(int)DAT_0000f32e = *(ushort *)(int)DAT_0000f32e & (ushort)DAT_0000f348;
  (*(code *)PTR_Control_ScheduleTimerTasks_0000f350)();
  return;
}

