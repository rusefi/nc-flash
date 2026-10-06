/* Ghidra analysis output; verify against original SH instructions. */

/* Protected8248=clamp8250 betweenraw8254/825C via207C,lower comparisonfirst. Executed108
   directcases and180 serialcycles withoriginalmaps. */

void Control_ClampOverrideSource(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar1 = (*(code *)PTR_FUN_0005c57c)(PTR_Control_OverrideSourceUpperBound_0005c594);
  uVar2 = (*(code *)PTR_FUN_0005c57c)(PTR_Control_OverrideSourceLowerBound_0005c58c);
  uVar1 = (*(code *)PTR_FUN_0005c5a4)
                    (*(undefined4 *)PTR_Control_UnboundedOverrideSource_0005c5a0,uVar2,uVar1);
  (*(code *)PTR_FUN_0005c590)(uVar1,PTR_Control_BoundedOverrideSource_0005c5a8);
  return;
}

