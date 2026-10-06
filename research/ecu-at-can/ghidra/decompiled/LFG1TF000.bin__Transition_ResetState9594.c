/* Ghidra analysis output; verify against original SH instructions. */

/* Set9594=1 and tailcall2D354 withindex4. Explicit reset in tested lifecycle; normal scheduling
   condition unproved. */

void Transition_ResetState9594(void)

{
  *(undefined1 *)(int)DAT_0002f0ee = 1;
                    /* WARNING: Could not recover jumptable at 0x0002f0b8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_0002f10c)(4);
  return;
}

