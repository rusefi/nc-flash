/* Ghidra analysis output; verify against original SH instructions. */

/* Executed body to16A04 beforeRTE. F522bit0 gatesack,F600=0,F604=4166,87F4=0 and11F7C;
   originalprofiling/registerrestore executes.150cases,80retainedcycles. See tcu-cycle-callback.txt.
    */

undefined8 OutputCycle_Timer6Callback(void)

{
  undefined *puVar1;
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar2;
  
  (*(code *)PTR_OutputTask_RecordInterruptEntry_00016a24)
            (0xb,PTR_DAT_00016a34 + *(short *)(int)DAT_00016a1c);
  puVar2 = (ushort *)(int)DAT_00016a1e;
  if ((*puVar2 & 1) != 0) {
    *puVar2 = *puVar2 & (ushort)PTR_DAT_00016a28;
    *(undefined2 *)(int)DAT_00016a12 = 0;
    *(undefined2 *)(int)DAT_00016a16 = DAT_00016a14;
    puVar1 = PTR_OutputCycle_ModeCallback_00016a38;
    *(undefined1 *)(int)DAT_00016a18 = 0;
    (*(code *)puVar1)();
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_00016a30)(0xb);
  return CONCAT44(in_r1,in_r0);
}

