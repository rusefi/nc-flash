/* Ghidra analysis output; verify against original SH instructions. */

/* Stock566E admissionrequires568A1,56771,protected20A8zero thenmode/timer/fault predicates.
   Writes5675 onlyonadmission;fullcallerstackarguments verified. */

undefined4
Control_AdmitFeedbackOverride
          (char param_1,ushort param_2,ushort param_3,char param_4,char param_5,char param_6,
          char param_7,char param_8,char param_9)

{
  char cVar1;
  undefined4 uVar2;
  
  if (((param_8 == '\x01') && (param_4 == '\x01')) && (param_5 == '\0')) {
    if ((((*PTR_DAT_00025380 == '\0') && (param_1 == '\0')) &&
        ((param_2 < *(ushort *)PTR_DAT_00025384 && ((param_9 == '\x01' && (param_6 == '\0')))))) &&
       (*PTR_Control_ThresholdState_568C_00025388 == '\0')) {
      uVar2 = 1;
      *PTR_Control_RetainedFeedbackAdmissionTag_0002538c = 0;
    }
    else {
      cVar1 = (*(code *)PTR_Protected_ReadByteOrDefault_00025554)(PTR_DAT_00025550,0);
      if ((((((cVar1 == '\0') && (*PTR_DAT_00025558 == '\0')) && (*PTR_DAT_0002555c == '\0')) &&
           (*PTR_Protected_InvalidReadPending_00025560 == '\0')) ||
          (((*PTR_DAT_00025564 == '\0' && (param_1 == '\x01')) &&
           (((*PTR_Control_ThresholdState_568D_00025568 == '\0' ||
             (*PTR_Control_ThresholdState_568E_0002556c == '\x01')) &&
            (((param_7 == '\0' &&
              (cVar1 = (*(code *)PTR_Protected_ReadByteOrDefault_00025554)(PTR_DAT_00025570,1),
              cVar1 == '\x01')) && (*PTR_Control_ThresholdState_568C_00025574 == '\0')))))))) &&
         ((param_1 == '\x01' && (param_3 < *(ushort *)PTR_DAT_00025578)))) {
        uVar2 = 1;
        *PTR_Control_RetainedFeedbackAdmissionTag_0002557c = 1;
      }
      else {
        uVar2 = 0;
      }
    }
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}

