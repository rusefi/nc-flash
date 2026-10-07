/* Ghidra analysis output; verify against original SH instructions. */

/* Stock5FD18 word0 ->880C;880E=0. Executed initialization. */

void CAN215_InitializePrimaryInput(void)

{
  *(undefined2 *)PTR_CAN215_PrimaryDecodedValue_0001712c = *(undefined2 *)PTR_PTR_00017128;
  *PTR_CAN215_PrimaryValidity_00017130 = 0;
  return;
}

