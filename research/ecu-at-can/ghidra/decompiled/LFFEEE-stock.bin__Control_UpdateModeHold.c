/* Ghidra analysis output; verify against original SH instructions. */

/* Executed1024cases:722Aexact1 reloads7358=stock2,otherwise
   decrementpositivebyte;735C=(counter!=0). Plain154B0read doesnotvalidatecomplement.
   control-task-stop.txt. */

char Control_UpdateModeHold(void)

{
  undefined *puVar1;
  char cVar2;
  
  puVar1 = PTR_DAT_00042b64;
  cVar2 = (*(code *)PTR_FUN_00042b74)(PTR_Control_FilteredModeInput_00042b70);
  if (cVar2 == '\x01') {
    *puVar1 = *PTR_DAT_00042b60;
    cVar2 = '\x01';
  }
  else {
    cVar2 = *puVar1;
    if (cVar2 != '\0') {
      *puVar1 = *puVar1 + (char)DAT_00042b50;
    }
  }
  if (*puVar1 == '\0') {
    *PTR_Control_ModeHoldFlag_00042b58 = 0;
  }
  else {
    *PTR_Control_ModeHoldFlag_00042b58 = 1;
  }
  return cVar2;
}

