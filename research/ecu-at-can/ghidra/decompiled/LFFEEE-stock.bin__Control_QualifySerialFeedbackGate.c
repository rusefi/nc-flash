/* Ghidra analysis output; verify against original SH instructions. */

/* Stock5677 requires56761,counter5668<=37or50..124,and536C/5550hysteresisstatesexact1.
   Fullbody/localgate cases andpairedserialreply5550. */

ushort Control_QualifySerialFeedbackGate(void)

{
  ushort uVar1;
  undefined *puVar2;
  ushort uVar3;
  float fVar4;
  float fVar5;
  
  fVar4 = *(float *)PTR_Control_FilteredLocalSource_00024d34;
  fVar5 = *(float *)PTR_DAT_00024d38;
  uVar1 = *(ushort *)PTR_Control_RelativeOverrideTimer_00024d3c;
  if (*PTR_DAT_00024d44 == '\x01') {
    if (*(ushort *)PTR_DAT_00024d48 < uVar1) {
      *PTR_DAT_00024d40 = 0;
      goto LAB_00024cf4;
    }
  }
  else {
    if (*PTR_DAT_00024d44 != '\0') goto LAB_00024cf4;
    if ((((*PTR_DAT_00024d4c != '\0') || (*PTR_DAT_00024d50 != '\0')) &&
        (*PTR_DAT_00024d54 != '\x01')) || (*(ushort *)PTR_DAT_00024d48 < uVar1)) {
      *PTR_DAT_00024d40 = 0;
      goto LAB_00024cf4;
    }
  }
  *PTR_DAT_00024d40 = 1;
LAB_00024cf4:
  puVar2 = PTR_DAT_00024d58;
  if (fVar4 < *(float *)PTR_DAT_00024d58) {
    if (fVar4 < *(float *)PTR_DAT_00024d60) {
      *PTR_DAT_00024d5c = 0;
    }
  }
  else {
    *PTR_DAT_00024d5c = 1;
  }
  if (fVar5 < *(float *)puVar2) {
    if (fVar5 < *(float *)PTR_DAT_00024f1c) {
      *PTR_DAT_00024f20 = 0;
    }
  }
  else {
    *PTR_DAT_00024d64 = 1;
  }
  uVar3 = (ushort)(byte)*PTR_Control_SerialEnableOutput_00024f28;
  if ((((uVar3 == 1) &&
       ((*PTR_DAT_00024f2c == '\x01' ||
        ((uVar3 = *(ushort *)PTR_DAT_00024f30, uVar3 <= uVar1 &&
         (uVar3 = *(ushort *)PTR_DAT_00024f34, uVar1 < uVar3)))))) &&
      (uVar3 = (ushort)(byte)*PTR_DAT_00024f38, uVar3 == 1)) &&
     (uVar3 = (ushort)(byte)*PTR_DAT_00024f20, uVar3 == 1)) {
    *PTR_Control_QualifiedSerialFeedback_00024f24 = 1;
  }
  else {
    *PTR_Control_QualifiedSerialFeedback_00024f24 = 0;
  }
  return uVar3;
}

