/* Ghidra analysis output; verify against original SH instructions. */

/* Executed1024mode0cases atfourcallerindices:returns(byte9935+u16index ==C0),noRAMwrites.
   Othermodesunmodeledhere;noDTC/physicalfaultidentification. Mode0queryorder/shortcircuitverified.
    */

undefined4 Control_QueryStatusClass(uint param_1,char param_2)

{
  char cVar1;
  ushort uVar2;
  undefined4 uVar3;
  
  uVar3 = 0;
  param_1 = param_1 & 0xffff;
  if (param_2 == '\0') {
    if ((byte)PTR_DAT_00090484[param_1] == DAT_0009047a) {
      uVar3 = 1;
    }
  }
  else if (param_2 == '\x01') {
    uVar2 = (ushort)(byte)PTR_DAT_00090484[param_1];
    if (((uVar2 == DAT_0009047a) || (uVar2 == DAT_0009047c)) || (uVar2 == 0x70)) {
      uVar3 = 1;
    }
  }
  else if (param_2 == '\x02') {
    cVar1 = (*(code *)PTR_FUN_00090488)();
    if (cVar1 == '\x01') {
      uVar3 = 1;
    }
  }
  else if ((param_2 == '\x03') && (PTR_DAT_0009048c[param_1] == '\x01')) {
    uVar3 = 1;
  }
  return uVar3;
}

