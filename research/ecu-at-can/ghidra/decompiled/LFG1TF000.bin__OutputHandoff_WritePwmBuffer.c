/* Ghidra analysis output; verify against original SH instructions. */

/* Original conversion and unsignedword clamp0..33313; A518zero selects33313. ROM5C588 maps channels
   toF510/F512/F516/F514: SH7055S-compatible BFR6A/B/D/C. Buffer write does not prove configured
   output waveform. */

void OutputHandoff_WritePwmBuffer(uint param_1,short param_2)

{
  int iVar1;
  undefined2 uVar2;
  undefined2 *puVar3;
  int iVar4;
  undefined *puVar5;
  
  puVar5 = PTR_DAT_000142e4;
  if (*(short *)PTR_DAT_000142e0 != 0) {
    iVar4 = (int)*(short *)((param_1 & 0xff) * 2 + (int)DAT_000142dc);
    iVar1 = (*(code *)PTR_FUN_000142ec)(param_1,(int)param_2,(int)*(short *)PTR_DAT_000142e0,iVar4);
    puVar5 = (undefined *)(iVar1 + iVar4);
  }
  puVar3 = *(undefined2 **)(PTR_OutputHandoff_PwmBufferPointers_000142f0 + (param_1 & 0xff) * 4);
  uVar2 = (*(code *)PTR_FUN_000142f4)(puVar5,0,PTR_DAT_000142e4);
  *puVar3 = uVar2;
  return;
}

