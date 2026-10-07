/* Ghidra analysis output; verify against original SH instructions. */

/* 8F32 isCAN215 byte6. FF retains unsigned880C andsets880E1; otherbytes*5 via original10F38
   descriptors5C80E/5C59C, status2.768 whole1ACF0 callback cases. */

void CAN215_DecodePrimaryInput(void)

{
  undefined *puVar1;
  undefined2 uVar2;
  undefined1 uVar3;
  
  uVar2 = *(undefined2 *)PTR_CAN215_PrimaryDecodedValue_0001712c;
  uVar3 = 1;
  if ((uint)(byte)*PTR_DAT_00017134 != (int)DAT_00017126) {
    puVar1 = (undefined *)
             (*(code *)PTR_FUN_00017140)
                       ((uint)(byte)*PTR_DAT_00017134,PTR_CAN215_PrimaryInputScale_0001713c,
                        PTR_CAN215_PrimaryOutputScale_00017138);
    if ((int)PTR_DAT_00017144 < (int)puVar1) {
      puVar1 = PTR_DAT_00017144;
    }
    if ((int)puVar1 < 0) {
      puVar1 = (undefined *)0x0;
    }
    uVar2 = SUB42(puVar1,0);
    uVar3 = 2;
  }
  puVar1 = PTR_CAN215_PrimaryValidity_00017130;
  *(undefined2 *)PTR_CAN215_PrimaryDecodedValue_0001712c = uVar2;
  *puVar1 = uVar3;
  return;
}

