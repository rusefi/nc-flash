/* Ghidra analysis output; verify against original SH instructions. */

/* Executes492DE request,49162 hysteresis,491C4 inhibit,tail49212 combination before49260
   selects8086. Physical source roles unresolved; tcu-phase-mode.txt. */

void PhaseMode_UpdateLocalFlags(void)

{
  (*(code *)PTR_PhaseMode_UpdateRequest_00048e10)();
  PhaseMode_UpdateHysteresis();
  PhaseMode_UpdateInhibit();
  PhaseMode_CombineRequest();
  return;
}

