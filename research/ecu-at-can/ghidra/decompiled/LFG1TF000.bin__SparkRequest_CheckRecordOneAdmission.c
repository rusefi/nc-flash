/* Ghidra analysis output; verify against original SH instructions. */

/* Class8080 not0/FF,916Fbit0clear,9B40 not0A/11 AND either accepted8081=0 withclass!=1 oraccepted=1
   withclassnot1/2.512 cases, high-bit classes included. */

undefined4 SparkRequest_CheckRecordOneAdmission(void)

{
  char cVar1;
  undefined4 uVar2;
  
  uVar2 = 0;
  cVar1 = *PTR_Selection_SourceCode_0002c3e0;
  if ((((((CAN231_SixStateSource == 0) && (TransmissionStateClass != 1)) && (cVar1 != '\n')) &&
       (cVar1 != '\x11')) ||
      (((CAN231_SixStateSource == 1 && (TransmissionStateClass != 1)) &&
       ((TransmissionStateClass != 2 && ((cVar1 != '\n' && (cVar1 != '\x11')))))))) &&
     ((TransmissionStateClass != 0 &&
      ((TransmissionStateClass != 0xff && ((*PTR_Request_CancellationFlags_0002c3e4 & 1) == 0))))))
  {
    uVar2 = 1;
  }
  return uVar2;
}

