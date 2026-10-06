/* Ghidra analysis output; verify against original SH instructions. */

/* Accepted==proposed returnsFF; otherwise row476A4 then5E1AC[row*6+proposed].2016 cases,
   proposed0..5. Table code is context-dependent, not solely numeric state direction. */

uint Transition_LookupQualifiedCode(undefined4 param_1,uint param_2,uint param_3)

{
  uint uVar1;
  
  uVar1 = (uint)DAT_000476cc;
  if ((param_2 & 0xff) != (param_3 & 0xff)) {
    uVar1 = Transition_SelectQualifiedRow(param_1,param_3);
    uVar1 = (uint)(byte)PTR_Transition_QualifiedCodeTable_000476e4
                        [(param_3 & 0xff) + (uVar1 & 0xff) * 6];
  }
  return uVar1;
}

