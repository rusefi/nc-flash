/* Ghidra analysis output; verify against original SH instructions. */

/* Executed stable-RAM predicate: NOT((u16(80A4)>=u16(B128) AND A962bit0) OR((u16(809E)>=u16(B12A)
   AND A98Ebit0) AND(A4E8 not0/2 AND A964bit0))). Physical units unproved. */

undefined4 PulseRequest_CheckQualifiedInputs(void)

{
  undefined4 uVar1;
  
  if ((((DAT_ffff80a4 < *(ushort *)PTR_PulseRequest_FirstInputThreshold_000535d4) ||
       ((PTR_DAT_000535cc[10] & 1) == 0)) &&
      ((CAN201_Word0Rescaled < *(ushort *)PTR_PulseRequest_SecondInputThreshold_000535d8 ||
       ((*PTR_Diagnostic_CAN201CutAggregate_000535d0 & 1) == 0)))) ||
     ((((DAT_ffff80a4 < *(ushort *)PTR_PulseRequest_FirstInputThreshold_000535d4 ||
        ((PTR_DAT_000535cc[10] & 1) == 0)) &&
       ((*(ushort *)PTR_PulseRequest_SecondInputThreshold_000535d8 <= CAN201_Word0Rescaled ||
        ((*PTR_Diagnostic_CAN201CutAggregate_000535d0 & 1) == 0)))) &&
      (((*PTR_DAT_000535c8 == '\0' || (*PTR_DAT_000535c8 == '\x02')) ||
       ((PTR_DAT_000535cc[0xc] & 1) == 0)))))) {
    uVar1 = 1;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

