/* Ghidra analysis output; verify against original SH instructions. */

/* OriginalwordF712=41,F718=41 at15610call. CompatibleSH7055S CMIE=1/CKS=1=Pphi/32 bothchannels.
   Compare624/1279 impliesconditional256:125 eventrate, notfixture100:8;
   noabsoluteclock/physicalchip/startphase/taskcadence proof.96component/32caller/32startchain cases
   PASS; tcu-cmt-configuration.txt. */

void CMT_ConfigureBothChannels(void)

{
  *(undefined2 *)(int)DAT_00014708 = 0x41;
  *(undefined2 *)(int)DAT_0001470a = 0x41;
  return;
}

