/* Ghidra analysis output; verify against original SH instructions. */

/* Calls46284 to generate74F1. Force8 if73C4mask60 or73B8==1;elsepopcount74F1 if718C==1,else0.2160
   cases;54 feedback paths use produced count. */

uint Model_UpdatePatternCount(void)

{
  undefined *puVar1;
  char cVar3;
  uint uVar2;
  char extraout_r3;
  
  (*(code *)PTR_Pattern_BuildModelMask_00040724)();
  puVar1 = PTR_Model_PatternCount_00040728;
  if ((((*PTR_DAT_0004072c & 0x40) == 0) && ((*PTR_DAT_0004072c & 0x20) == 0)) &&
     (cVar3 = (*(code *)PTR_FUN_000406d8)(PTR_DAT_00040730), cVar3 != '\x01')) {
    uVar2 = (*(code *)PTR_FUN_00040838)(PTR_DAT_00040834);
    if ((uVar2 & 0xff) == 1) {
      uVar2 = (uint)(char)*PTR_Pattern_EventMask_0004083c;
      cVar3 = (*(code *)PTR_FUN_00040840)(*PTR_Pattern_EventMask_0004083c);
      *puVar1 = extraout_r3 + cVar3 + (char)(uVar2 & 1);
      return uVar2 & 1;
    }
    *puVar1 = 0;
    return uVar2 & 0xff;
  }
  *puVar1 = 8;
  return 1;
}

