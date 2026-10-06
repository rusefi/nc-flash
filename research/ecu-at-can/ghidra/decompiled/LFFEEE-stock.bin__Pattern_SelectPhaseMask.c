/* Ghidra analysis output; verify against original SH instructions. */

/* Stock C4FB8 override disabled.74F0 level and74F2 phase select event mask;invalidphase/nonzero
   level ->FF.324 mask/count cases. */

uint Pattern_SelectPhaseMask(byte param_1)

{
  char cVar1;
  char *pcVar2;
  uint uVar3;
  
  pcVar2 = PTR_DAT_00046490;
  if (*PTR_DAT_0004648c != '\0') goto LAB_00046432;
  pcVar2 = PTR_DAT_00046494;
  if (param_1 != 0) {
    uVar3 = (uint)(byte)*PTR_Pattern_RotationPhase_00046488;
    if (3 < uVar3) {
      return (int)(char)*PTR_DAT_00046498;
    }
    if (param_1 < 3) {
      pcVar2 = PTR_DAT_0004649c;
      if (uVar3 == 0) {
LAB_000463f6:
        return (int)*pcVar2;
      }
      pcVar2 = PTR_DAT_000464a0;
      if (uVar3 != 1) {
        pcVar2 = PTR_DAT_000464a4;
        if (uVar3 != 2) {
          if (uVar3 != 3) {
            return uVar3;
          }
          return (int)(char)*PTR_DAT_000464a8;
        }
        goto LAB_000463f6;
      }
    }
    else {
      if (param_1 < 5) {
        pcVar2 = PTR_DAT_000464ac;
        if (uVar3 != 0) {
          pcVar2 = PTR_DAT_000464b0;
          if (uVar3 == 1) goto LAB_0004646e;
          pcVar2 = PTR_DAT_000464b4;
          if (uVar3 != 2) {
            if (uVar3 != 3) {
              return uVar3;
            }
            return (int)(char)*PTR_DAT_000464b8;
          }
        }
LAB_00046432:
        cVar1 = *pcVar2;
        goto LAB_00046482;
      }
      if (6 < param_1) {
        return (int)(char)*PTR_DAT_00046498;
      }
      if (uVar3 == 0) {
        return (int)(char)*PTR_DAT_000464bc;
      }
      pcVar2 = PTR_DAT_000464c0;
      if ((uVar3 != 1) && (pcVar2 = PTR_DAT_000464c4, uVar3 != 2)) {
        if (uVar3 != 3) {
          return uVar3;
        }
        return (int)(char)*PTR_DAT_000464c8;
      }
    }
  }
LAB_0004646e:
  cVar1 = *pcVar2;
LAB_00046482:
  return (int)cVar1;
}

