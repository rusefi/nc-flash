/* Ghidra analysis output; verify against original SH instructions. */

/* 6936=1 iff6927zero andraw9462zero.154B0 israwgetter, no checksum.1024cases; raw2
   mayallowproducerdecrement butkeepsflag0. */

undefined4 ControlMode_PublishExpiry(void)

{
  char cVar1;
  
  if ((*PTR_ControlMode_ExpiryCountdown_00030750 == '\0') &&
     (cVar1 = (*(code *)PTR_FUN_0003073c)(PTR_DAT_00030738), cVar1 == '\0')) {
    *PTR_ControlMode_ExpiredFlag_00030754 = 1;
    return 0;
  }
  *DAT_0003081c = 0;
  return 0;
}

