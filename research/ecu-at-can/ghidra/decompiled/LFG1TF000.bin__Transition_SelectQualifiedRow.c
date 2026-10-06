/* Ghidra analysis output; verify against original SH instructions. */

/* History0->0;1->1/2 bybit0;2->3/4 fornext1,5/6 fornext2
   bybit2,otherwise3;3->7;4->8;other->9.9C54bit1 unused.12288 cases
   allhistorybytes/validcolumns/lowflags. */

undefined4 Transition_SelectQualifiedRow(char param_1,char param_2)

{
  undefined4 uVar1;
  
  if (param_1 == '\0') {
    uVar1 = 0;
  }
  else if (param_1 == '\x01') {
    uVar1 = 1;
    if ((*(byte *)(int)DAT_000476ce & 1) == 1) {
      uVar1 = 2;
    }
  }
  else if (param_1 == '\x02') {
    uVar1 = 3;
    if ((param_2 == '\x01') && ((*(byte *)(int)DAT_000476ce & 1) == 1)) {
      uVar1 = 4;
    }
    if ((param_2 == '\x02') && (uVar1 = 5, (*(byte *)(int)DAT_000477f8 & 4) != 0)) {
      uVar1 = 6;
    }
  }
  else if (param_1 == '\x03') {
    uVar1 = 7;
  }
  else if (param_1 == '\x04') {
    uVar1 = 8;
  }
  else {
    uVar1 = 9;
  }
  return uVar1;
}

