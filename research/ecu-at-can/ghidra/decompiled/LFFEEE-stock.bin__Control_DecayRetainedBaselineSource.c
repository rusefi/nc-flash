/* Ghidra analysis output; verify against original SH instructions. */

/* If734A bit40 clear andold809C<stockDA040=0,clear. Elsemax(RTZ(old809C-80A4),7346exact1?0:80A0).
   Separate caller1B868; production rate remains open. */

uint Control_DecayRetainedBaselineSource(void)

{
  undefined *puVar1;
  uint uVar2;
  char cVar3;
  undefined4 extraout_fr0;
  undefined4 uVar4;
  float fVar5;
  
  puVar1 = PTR_Control_RetainedBaselineSource_00058ef8;
  fVar5 = *(float *)PTR_Control_RetainedBaselineSource_00058ef8;
  uVar2 = (uint)(char)*PTR_TransmissionModeFlags_00058efc;
  uVar4 = 0;
  if (((uVar2 & 0x40) != 0) || (*(float *)PTR_DAT_00058f00 <= fVar5)) {
    cVar3 = (*(code *)PTR_FUN_00058ed8)(PTR_DAT_00058f04);
    if (cVar3 != '\x01') {
      uVar4 = *(undefined4 *)PTR_Control_BaselineSourceTarget_00058f08;
    }
    uVar2 = (*(code *)PTR_FUN_00058f0c)
                      (fVar5 - *(float *)PTR_Control_BaselineSourceDecayStep_00058ec8,uVar4);
    *(undefined4 *)puVar1 = extraout_fr0;
  }
  else {
    *(undefined4 *)PTR_Control_RetainedBaselineSource_00058ef8 = 0;
  }
  return uVar2;
}

