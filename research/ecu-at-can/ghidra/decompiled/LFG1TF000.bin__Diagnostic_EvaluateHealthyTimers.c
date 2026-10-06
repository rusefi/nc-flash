/* Ghidra analysis output; verify against original SH instructions. */

/* Eight-byte records5F008; mapped21 uses5000 ticks and count1 at5F0E0. Helpers581AA/58200/58274
   consumeA9DC status02 and publishAA0F flags. */

void Diagnostic_EvaluateHealthyTimers(void)

{
  byte bVar1;
  char cVar2;
  byte *pbVar3;
  undefined *puVar4;
  byte *pbVar5;
  byte *pbVar6;
  
  pbVar3 = PTR_Diagnostic_HealthyConfiguration_00058144 + DAT_0005813a;
  puVar4 = PTR_DAT_00058140;
  for (pbVar6 = PTR_Diagnostic_HealthyConfiguration_00058144; pbVar6 <= pbVar3; pbVar6 = pbVar6 + 8)
  {
    bVar1 = *pbVar6;
    cVar2 = FUN_00058186((int)(char)bVar1);
    if (cVar2 != '\x11') {
      pbVar5 = (byte *)((uint)bVar1 + (int)DAT_0005813c);
      if (cVar2 == '\x01') {
        FUN_000581aa(pbVar6,puVar4,(int)(char)bVar1,1,2);
        if ((*pbVar5 & 2) != 0) {
          *pbVar5 = *pbVar5 | 0x80;
        }
      }
      else if (cVar2 == '\b') {
        *pbVar5 = 0;
        *(undefined2 *)(puVar4 + 4) = 0;
      }
    }
    puVar4 = puVar4 + 8;
  }
  return;
}

