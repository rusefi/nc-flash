/* Ghidra analysis output; verify against original SH instructions. */

/* Tail30518 storeslowwordR5 at98B4+4*u8(R4)+2. Whole36704 andindependent selectiontests
   useoriginalallocatedhandles4..7; no link/modewrite. */

void ClassApplication_SetEntry(undefined4 param_1,undefined4 param_2)

{
  (*(code *)PTR_RequestList_SetValue_00039c48)
            (param_1,param_2,PTR_ClassApplication_PriorityList_00039c3c);
  return;
}

