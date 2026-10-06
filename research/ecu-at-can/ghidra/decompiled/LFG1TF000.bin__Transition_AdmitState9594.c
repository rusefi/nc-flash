/* Ghidra analysis output; verify against original SH instructions. */

/* If2F0C2 reports1, set9594=2 and81CE=0; otherwise retain.1280 source cases paired with2F222. */

undefined * Transition_AdmitState9594(void)

{
  undefined *puVar1;
  uint uVar2;
  undefined *puVar3;
  
  uVar2 = Transition_CheckState9594Admission();
  puVar1 = PTR_DAT_0002f0f4;
  puVar3 = (undefined *)(uVar2 & 0xff);
  if ((undefined *)(uVar2 & 0xff) == (undefined *)0x1) {
    *(undefined1 *)(int)DAT_0002f0ee = 2;
    *puVar1 = 0;
    puVar3 = puVar1;
  }
  return puVar3;
}

