/* Ghidra analysis output; verify against original SH instructions. */

/* Original304C6 allocator on98B4/AE18. Priorities1/2/3/2 yieldhandles4/5/6/7; links checked.
   Invocation priorities are fixtures, notactual36704 caller proof. */

undefined4 ClassApplication_AllocateEntry(short param_1)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_RequestList_Allocate_00039c44)
                    ((int)param_1,PTR_ClassApplication_PriorityList_00039c3c,PTR_DAT_00039c38);
  return uVar1;
}

