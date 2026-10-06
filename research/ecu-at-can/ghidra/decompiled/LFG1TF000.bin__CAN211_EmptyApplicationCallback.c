/* Ghidra analysis output; verify against original SH instructions. */

/* Exactly RTS;NOP. Receipt callback reaches this stub; this does not prove payload absence
   elsewhere. */

void CAN211_EmptyApplicationCallback(void)

{
  return;
}

