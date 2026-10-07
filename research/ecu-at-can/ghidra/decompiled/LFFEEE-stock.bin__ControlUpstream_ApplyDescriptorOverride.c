/* Ghidra analysis output; verify against original SH instructions. */

/* DescriptorAD4BC mask60 at966C; clears9611 when neither bit set. Mode0 encodes9642 at scale1/2048
   but returns input;5/7 decode; other modes passthrough.2112 direct cases. Operational access
   unproved. */

uint ControlUpstream_ApplyDescriptorOverride(undefined4 param_1)

{
  undefined *puVar1;
  uint uVar2;
  int iVar3;
  
  puVar1 = PTR_DAT_0008bc04;
  iVar3 = (int)DAT_0008bbf8;
  if ((*PTR_DAT_0008bc08 & PTR_DAT_0008bc04[iVar3 + 8]) == 0) {
    **(undefined1 **)(PTR_DAT_0008bc04 + iVar3 + 0xc) = 0;
  }
  uVar2 = (uint)**(byte **)(puVar1 + iVar3 + 0xc);
  if (uVar2 == 0) {
    uVar2 = (*(code *)PTR_FUN_0008bc10)(param_1,DAT_0008bc0c,0);
    puVar1 = PTR_ControlUpstream_EncodedValue_0008bc14;
    *PTR_ControlUpstream_EncodedValue_0008bc14 = (char)(uVar2 >> 8);
    puVar1[1] = (char)uVar2;
  }
  else if ((uVar2 == 5) || (uVar2 == 7)) {
    uVar2 = (*(code *)PTR_FUN_0008bc00)
                      (DAT_0008bc0c,0,*(undefined2 *)PTR_ControlUpstream_EncodedValue_0008bc14);
  }
  return uVar2;
}

