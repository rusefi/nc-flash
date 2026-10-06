/* Ghidra analysis output; verify against original SH instructions. */

/* All65536 bytecode/input800B pairs produce808C in0..4 using70A20 five-threshold rows and316A8
   family. Establishes normal three-by-five parameter-group layout. See tcu-request-dispatch.txt. */

int SparkRequest_ProduceParameterIndex(void)

{
  byte bVar1;
  uint uVar2;
  int iVar3;
  
  bVar1 = DAT_ffff800b;
  uVar2 = (*(code *)PTR_ApplicationCode_SelectThresholdFamily_000314fc)();
  iVar3 = 4;
  if (bVar1 < (byte)PTR_SparkRequest_ParameterIndexThresholds_00031500[(uVar2 & 0xffff) * 5 + 4]) {
    for (iVar3 = 0;
        (byte)PTR_SparkRequest_ParameterIndexThresholds_00031500[iVar3 + (uVar2 & 0xffff) * 5] <=
        bVar1; iVar3 = iVar3 + 1) {
    }
  }
  DAT_ffff808c = (char)iVar3;
  return iVar3;
}

