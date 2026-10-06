/* Ghidra analysis output; verify against original SH instructions. */

/* Stock7744C count3 dispatches5DEA0 entries44664/466B8/4662C onr4/r5 byte pointers.720 whole-call
   fixtures and6 paired ECU paths; entry order observed without hooks. */

void Selection_RunThreeStagePipeline(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  
  puVar2 = (undefined4 *)PTR_Selection_PipelineTable_0004546c;
  for (iVar1 = 0; iVar1 < *(short *)PTR_Selection_PipelineStageCount_00045470; iVar1 = iVar1 + 1) {
    (*(code *)*puVar2)(param_1,param_2);
    puVar2 = puVar2 + 1;
  }
  return;
}

