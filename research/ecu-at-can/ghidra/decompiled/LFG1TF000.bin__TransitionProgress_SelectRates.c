/* Ghidra analysis output; verify against original SH instructions. */

/* 8089 transition selects subsetof970C/9710/9714 updates; unselected rates
   retained.95AE/95C9/9410/99DC/99C4/99B0 branches,971Abit0 cap qualifier.16384
   directcasesallcodebytes/flagcombinations. */

uint TransitionProgress_SelectRates(void)

{
  bool bVar1;
  uint uVar2;
  uint uVar3;
  uint *puVar4;
  uint *puVar5;
  uint *puVar6;
  
  puVar4 = (uint *)(int)DAT_000329b2;
  uVar2 = (int)(char)*PTR_DAT_000329b8 & 1;
  puVar5 = (uint *)(int)DAT_000329b4;
  puVar6 = (uint *)(int)DAT_000329b6;
  bVar1 = (*PTR_DAT_000329bc & 2) == 0;
  uVar3 = (uint)DAT_ffff8089;
  if (uVar3 == 0) {
    uVar2 = TransitionProgress_PositiveRateA();
  }
  else {
    if (uVar3 != 1) {
      if ((uVar3 == 2) || (uVar3 == 3)) {
        uVar2 = TransitionProgress_PositiveRateB();
        *puVar6 = uVar2;
        return uVar2;
      }
      if (uVar3 == 4) {
        uVar2 = TransitionProgress_NegativeRateC();
      }
      else {
        if (uVar3 == 5) {
          uVar3 = TransitionProgress_NegativeRateA();
          *puVar4 = uVar3;
          uVar3 = TransitionProgress_MixedNegativeRateC();
          *puVar5 = uVar3;
          uVar3 = TransitionProgress_NegativeRateB();
          *puVar6 = uVar3;
          if (uVar2 != 1) {
            return uVar2;
          }
          uVar2 = TransitionProgress_AlternateNegativeRateB();
          *puVar6 = uVar2;
          return uVar2;
        }
        if (uVar3 == 6) {
          uVar3 = TransitionProgress_NegativeRateB();
          *puVar6 = uVar3;
          if (uVar2 == 1) {
            uVar2 = TransitionProgress_AlternateNegativeRateB();
            *puVar6 = uVar2;
          }
          uVar2 = TransitionProgress_MixedNegativeRateC();
        }
        else {
          if (uVar3 == 7) {
            uVar3 = TransitionProgress_NegativeRateB();
            *puVar6 = uVar3;
            if (uVar2 == 1) {
              uVar2 = TransitionProgress_AlternateNegativeRateB();
              *puVar6 = uVar2;
            }
          }
          else {
            if (uVar3 != 10) {
              if (uVar3 == 0xb) {
                uVar2 = TransitionProgress_PositiveRateC();
                *puVar5 = uVar2;
                uVar2 = -(((*PTR_Request_EnableFlags_00032adc & 2) == 0) - 1);
                if (uVar2 != 1) {
                  return uVar2;
                }
                uVar2 = TransitionProgress_AlternatePositiveRateC();
                *puVar5 = uVar2;
                if (((int)(char)*PTR_DAT_00032ae0 & 1U) != 1) {
                  return (int)(char)*PTR_DAT_00032ae0 & 1U;
                }
              }
              else {
                if (uVar3 != 9) {
                  return uVar3;
                }
                uVar2 = TransitionProgress_AlternatePositiveRateC();
                *puVar5 = uVar2;
                if (((*PTR_DAT_00032ae4 & 4) == 0) || (bVar1)) {
                  uVar2 = -(((*PTR_DAT_00032ae8 & 2) == 0) - 1);
                  if (uVar2 != 1) {
                    return uVar2;
                  }
                  if (!bVar1) {
                    return 1;
                  }
                }
              }
              uVar2 = (int)*(char *)(int)DAT_00032ad8 | 1;
              *(char *)(int)DAT_00032ad8 = (char)uVar2;
              return uVar2;
            }
            uVar2 = TransitionProgress_NegativeRateB();
            *puVar6 = uVar2;
          }
          uVar2 = TransitionProgress_PositiveRateC();
        }
      }
      *puVar5 = uVar2;
      return uVar2;
    }
    uVar2 = TransitionProgress_PositiveRateC();
    *puVar5 = uVar2;
    uVar2 = TransitionProgress_PositiveRateA();
  }
  *puVar4 = uVar2;
  return uVar2;
}

