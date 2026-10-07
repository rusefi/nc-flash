/* Ghidra analysis output; verify against original SH instructions. */

/* Executed8192stockcases:8FD8 iff735Abit7,8FE0/8FDF/9125exact1 and9037Cmode0 indices2F/30/2D/2E
   allfalse. StockE0861FF skips1F/20/2A/2B;alternatecalibrationnotexecuted.
   Actualtaskconsumesfreshthresholdflags. */

undefined1 Control_PublishActivityTimerEnable(void)

{
  char cVar1;
  undefined1 uVar2;
  
  if (((((((((int)*DAT_0006f510 & 0x80U) == 0) ||
          (*PTR_Control_ActivityFirstThresholdFlag_0006f4ec != '\x01')) ||
         (*PTR_Control_ActivitySecondThresholdFlag_0006f4fc != '\x01')) ||
        ((cVar1 = (*pcRam0006f514)(0x2f,0), cVar1 != '\0' ||
         (cVar1 = (*pcRam0006f514)(0x30,0), cVar1 != '\0')))) ||
       ((cVar1 = (*pcRam0006f514)(0x2d,0), cVar1 != '\0' ||
        (cVar1 = (*pcRam0006f514)(0x2e,0), cVar1 != '\0')))) ||
      ((*pcRam0006f518 == '\0' &&
       (((cVar1 = (*pcRam0006f514)(0x1f,0), cVar1 != '\0' ||
         (cVar1 = (*pcRam0006f514)(0x20,0), cVar1 != '\0')) ||
        ((cVar1 = (*pcRam0006f514)(0x2a,0), cVar1 != '\0' ||
         (cVar1 = (*pcRam0006f514)(0x2b,0), cVar1 != '\0')))))))) || (*pcRam0006f51c != '\x01')) {
    uVar2 = 0;
    *PTR_Control_ActivityTimerEnable_0006f520 = 0;
  }
  else {
    *PTR_Control_ActivityTimerEnable_0006f520 = 1;
    uVar2 = 1;
  }
  return uVar2;
}

