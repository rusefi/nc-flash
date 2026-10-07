/* Ghidra analysis output; verify against original SH instructions. */

/* 6964=R(6CB4+DB1D4);6800=clamp(R(67FC-6964),-2.5,2.5). Executed control-normalized-inputs.txt;
   physical loop identity open. */

void Control_ProduceBoundedInputError(void)

{
  undefined4 uVar1;
  float fVar2;
  float fVar3;
  
  fVar3 = *(float *)PTR_DAT_00031468;
  fVar2 = *(float *)PTR_Control_LocalFilterInput_0003146c;
  *(float *)PTR_Control_OffsetInputTarget_00031464 = fVar2 + fVar3;
  uVar1 = (*(code *)PTR_FUN_00031478)
                    (*(float *)PTR_ControlUpstream_ProducedTarget_00031460 - (fVar2 + fVar3),
                     DAT_00031474,DAT_00031470);
  *(undefined4 *)PTR_Control_BoundedInputError_0003147c = uVar1;
  return;
}

