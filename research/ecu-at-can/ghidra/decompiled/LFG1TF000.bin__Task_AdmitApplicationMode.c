/* Ghidra analysis output; verify against original SH instructions. */

/* STATIC:8007==1 promotes3 if84A0/84D8/84EC all3 via126DA; tails126EC. Full admitted probe
   stops1412A onFFFFF810. */

void Task_AdmitApplicationMode(void)

{
  if ((((DAT_ffff8007 == '\x01') && (*PTR_DAT_00012258 == '\x03')) && (*PTR_DAT_0001225c == '\x03'))
     && (*PTR_DAT_00012260 == '\x03')) {
    (*(code *)PTR_FUN_00012264)();
    DAT_ffff8007 = '\x03';
  }
  (*(code *)PTR_Task_ServiceApplicationMode_00012268)();
  return;
}

