/* Ghidra analysis output; verify against original SH instructions. */

/* Ordered control8083 adjustment,9C92 latch/timer,lower/upper fallback,92C5 edge multistep and
   cache116h low-measurement override. Six original word-curve wrappers execute;2112 complete policy
   cases. tcu-source-selection.txt. */

void SourcePolicy_ApplyThresholdRules(uint param_1,undefined1 *param_2,undefined1 *param_3)

{
  undefined *puVar1;
  ushort uVar2;
  char cVar4;
  ushort uVar3;
  uint uVar5;
  undefined1 *puVar6;
  int iVar7;
  uint local_28;
  
  uVar2 = DAT_ffff80ea;
  local_28._0_1_ = 0;
  cVar4 = -(((*PTR_DAT_000497c4 & 2) == 0) + -1);
  if (DAT_ffff8083 == '\x01') {
    if (((param_1 & 0xff) < 5) &&
       (uVar3 = SourcePolicy_LookupIncrementThreshold(param_1), uVar3 <= uVar2)) {
      param_1 = param_1 + 1;
      *param_2 = 1;
      *param_3 = 10;
      uVar3 = SourcePolicy_LookupLatchThreshold(param_1);
      if (uVar2 < uVar3) {
        *(undefined1 *)(int)DAT_000497c0 = 1;
      }
    }
  }
  else if ((DAT_ffff8083 == '\x02') && ((param_1 & 0xff) != 0)) {
    uVar3 = SourcePolicy_LookupDecrementThreshold(param_1);
    if (uVar2 < uVar3) {
      puVar6 = (undefined1 *)(int)DAT_000497c0;
      param_1 = param_1 - 1;
      *param_2 = 1;
      *param_3 = 10;
      *puVar6 = 0;
    }
    else {
      local_28._0_1_ = 1;
    }
  }
  uVar5 = param_1 & 0xff;
  *PTR_SourcePolicy_RejectedDecrement_000497c8 = local_28._0_1_;
  if (*(char *)(int)DAT_000497c0 == '\x01') {
    if (uVar5 != 0) {
      uVar3 = SourcePolicy_LookupLatchThreshold(param_1);
      if (uVar2 < uVar3) {
        *PTR_DAT_000497cc = 0;
      }
      else if ((byte)PTR_SourcePolicy_LatchTimerBounds_000497d0[uVar5 - 1] < (byte)*PTR_DAT_000497cc
              ) {
        *(undefined1 *)(int)DAT_000497c0 = 0;
      }
    }
  }
  else if ((uVar5 != 0) && (uVar3 = SourcePolicy_LookupLowerFallback(param_1), uVar2 < uVar3)) {
    param_1 = param_1 - 1;
    *param_2 = 2;
    *param_3 = 10;
  }
  if (((((param_1 & 0xff) < 5) &&
       (uVar3 = SourcePolicy_LookupUpperFallback(param_1), uVar3 <= uVar2)) &&
      ((*PTR_SourcePolicy_EnableUpperFallback_00049840 == '\x01' || (cVar4 == '\x01')))) &&
     ((*PTR_DAT_00049844 & 1) == 1)) {
    param_1 = param_1 + 1;
    *param_2 = 2;
    *param_3 = 10;
  }
  if (((*PTR_SourcePolicy_EnableEdgeFallback_00049848 == '\x01') && (cVar4 != '\0')) &&
     (local_28 = uVar5, cVar4 != *(char *)(int)DAT_0004983c)) {
    while (((local_28._0_1_ < 5 && ((param_1 & 0xff) != 0)) &&
           (uVar3 = SourcePolicy_LookupEdgeFallback(param_1), uVar2 < uVar3))) {
      param_1 = param_1 - 1;
      *param_2 = 2;
      *param_3 = 10;
      local_28 = (uint)(byte)(local_28._0_1_ + 1) << 0x18;
    }
  }
  puVar1 = PTR_FUN_0004993c;
  iVar7 = (int)DAT_00049936;
  *(char *)(int)DAT_00049934 = cVar4;
  cVar4 = (*(code *)puVar1)(iVar7);
  if ((((*PTR_DAT_00049940 & 0x40) != 0) || (cVar4 == '\x01')) &&
     ((uVar2 <= *(ushort *)PTR_SourcePolicy_LowFallbackThreshold_00049944 && ((param_1 & 0xff) != 0)
      ))) {
    puVar6 = (undefined1 *)(int)DAT_00049938;
    param_1 = 0;
    *param_2 = 2;
    *param_3 = 10;
    *puVar6 = 0;
  }
  (*(code *)PTR_FUN_00049948)(param_1 & 0xff,0,5);
  return;
}

