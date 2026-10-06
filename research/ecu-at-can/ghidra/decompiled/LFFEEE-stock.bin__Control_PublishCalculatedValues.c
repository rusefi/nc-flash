/* Ghidra analysis output; verify against original SH instructions. */

/* Copies A660/A65C/A658/A650/A654 to72C8/72CC/72D0/72D4/72D8;A613/A612 exact1 to72DC/72DD. */

undefined4 Control_PublishCalculatedValues(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00041ad4)(0x10);
  *(undefined4 *)PTR_Control_PublishedInverseValue_00041adc =
       *(undefined4 *)PTR_Control_LimitedInverseValue_00041ad8;
  *(undefined4 *)PTR_DAT_00041ae4 = *(undefined4 *)PTR_DAT_00041ae0;
  *(undefined4 *)PTR_DAT_00041aec = *(undefined4 *)PTR_DAT_00041ae8;
  *(undefined4 *)PTR_DAT_00041af4 = *(undefined4 *)PTR_DAT_00041af0;
  *(undefined4 *)PTR_DAT_00041afc = *(undefined4 *)PTR_DAT_00041af8;
  if (*PTR_DAT_00041b04 == '\x01') {
    *PTR_DAT_00041b00 = 1;
  }
  else {
    *PTR_DAT_00041b00 = 0;
  }
  if (*PTR_DAT_00041b0c == '\x01') {
    *PTR_DAT_00041b08 = 1;
  }
  else {
    *PTR_DAT_00041b08 = 0;
  }
  uVar1 = (*(code *)PTR_FUN_00041b10)(uVar1);
  return uVar1;
}

