/* Ghidra analysis output; verify against original SH instructions. */

/* First exact-one among7188/89/8A/8B selects0/1/2/3;else4 into7181.243 priority/enable cases. */

char Pattern_SelectRequestIndex(void)

{
  char cVar1;
  
  if (*PTR_Pattern_UpperThresholdLatch_0003fe9c == '\x01') {
    *PTR_Pattern_ClassifiedIndex_0003fe98 = 0;
    cVar1 = '\x01';
  }
  else {
    if (*PTR_Pattern_MiddleThresholdLatch_0003fea0 == '\x01') {
      cVar1 = '\x01';
    }
    else if (*PTR_Pattern_LowerThresholdLatch_0003fea4 == '\x01') {
      cVar1 = '\x02';
    }
    else {
      cVar1 = *PTR_Pattern_MinimumRequestFlag_0003fea8;
      if (cVar1 != '\x01') {
        *PTR_Pattern_ClassifiedIndex_0003fe98 = 4;
        return cVar1;
      }
      cVar1 = '\x03';
    }
    *PTR_Pattern_ClassifiedIndex_0003fe98 = cVar1;
  }
  return cVar1;
}

