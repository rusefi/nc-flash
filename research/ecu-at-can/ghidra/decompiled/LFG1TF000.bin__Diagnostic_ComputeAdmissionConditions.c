/* Ghidra analysis output; verify against original SH instructions. */

/* UnsignedA518: A939 high>10200/low>9000; A938 also809E>400/A98Ebit0. A93A high>10500/low>10000
   plusdependency. Mode8006 mustequal3. Rawunits unproved. */

void Diagnostic_ComputeAdmissionConditions
               (undefined1 *param_1,undefined1 *param_2,undefined1 *param_3)

{
  ushort uVar1;
  undefined *puVar2;
  
  puVar2 = PTR_FUN_00056cbc;
  uVar1 = *(ushort *)PTR_DAT_00056cb8;
  (*(code *)PTR_FUN_00056cbc)(param_1,0,2);
  (*(code *)puVar2)(param_2,0,2);
  (*(code *)puVar2)(param_3,0,2);
  puVar2 = PTR_DAT_00056cc0;
  if (DAT_ffff8006 == '\x03') {
    if (*(ushort *)PTR_DAT_00056cc4 < uVar1) {
      param_2[1] = 1;
      if ((*(ushort *)puVar2 < CAN201_Word0Rescaled) &&
         ((*PTR_Diagnostic_CAN201CutAggregate_00056cc8 & 1) == 1)) {
        param_1[1] = 1;
      }
      if ((*(ushort *)PTR_DAT_00056ccc < uVar1) && (*param_2 = 1, param_1[1] != '\0')) {
        *param_1 = 1;
      }
    }
    if ((DAT_ffff8006 == '\x03') && (*(ushort *)PTR_DAT_00056cd0 < uVar1)) {
      if ((*(ushort *)puVar2 < CAN201_Word0Rescaled) &&
         ((*PTR_Diagnostic_CAN201CutAggregate_00056cc8 & 1) == 1)) {
        param_3[1] = 1;
      }
      if ((*(ushort *)PTR_DAT_00056cd4 < uVar1) && (param_3[1] != '\0')) {
        *param_3 = 1;
      }
    }
  }
  return;
}

