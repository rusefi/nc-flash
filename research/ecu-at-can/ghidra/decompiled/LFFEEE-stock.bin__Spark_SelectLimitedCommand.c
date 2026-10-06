/* Ghidra analysis output; verify against original SH instructions. */

/* Normal path clamps7C94+7B6C+7AB4 between selected7AD0 andD05AC then7A78. Special modes/other
   gates exist; see can211-spark.txt for tested scope. */

undefined4 Spark_SelectLimitedCommand(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  undefined4 *puVar4;
  float extraout_fr0;
  undefined4 uVar5;
  float fVar6;
  
  puVar2 = PTR_DAT_0004fd40;
  puVar1 = PTR_FUN_0004fd3c;
  if (((int)(char)*PTR_DAT_0004fd10 & 0x80U) != 0) {
    fVar6 = *(float *)PTR_DAT_0004fce4;
    uVar5 = 1;
    goto LAB_0004fcd6;
  }
  if ((*PTR_DAT_0004fd10 & 0x40) != 0) {
    fVar6 = *(float *)PTR_DAT_0004fd38 - *(float *)PTR_DAT_0004fd34;
    uVar5 = 1;
    goto LAB_0004fcd6;
  }
  cVar3 = (*(code *)PTR_FUN_0004fd3c)(PTR_DAT_0004fd44);
  if (cVar3 == '\x01') {
    cVar3 = (*(code *)puVar1)(PTR_DAT_0004fd48);
    if (cVar3 == '\x01') {
      uVar5 = *(undefined4 *)PTR_DAT_0004fd4c;
    }
    else {
      uVar5 = *(undefined4 *)PTR_DAT_0004fd50;
    }
    *(undefined4 *)puVar2 = uVar5;
  }
  else {
    if ((*PTR_DAT_0004fd54 == '\x01') &&
       (cVar3 = (*(code *)PTR_FUN_0004fd3c)(PTR_DAT_0004fd58),
       puVar4 = (undefined4 *)PTR_DAT_0004fd5c, cVar3 == '\0')) {
LAB_0004fc92:
      uVar5 = *puVar4;
    }
    else if (*(float *)PTR_DAT_0004fd60 <= 0.0) {
      if ((0.0 < *(float *)PTR_DAT_0004fd68) &&
         (puVar4 = (undefined4 *)PTR_DAT_0004fd70, *PTR_DAT_0004fd6c == '\x01')) goto LAB_0004fc92;
      cVar3 = (*(code *)puVar1)(PTR_DAT_0004fd74);
      if (cVar3 == '\x01') {
        uVar5 = *(undefined4 *)PTR_DAT_0004fd78;
      }
      else {
        uVar5 = *(undefined4 *)PTR_DAT_0004fd7c;
      }
    }
    else {
      uVar5 = *(undefined4 *)PTR_DAT_0004fd64;
    }
    uVar5 = (*(code *)PTR_FUN_0004fd84)(uVar5,*(undefined4 *)PTR_DAT_0004fd80);
    *(undefined4 *)puVar2 = uVar5;
  }
  uVar5 = (*(code *)PTR_FUN_0004fd98)
                    (*(float *)PTR_DAT_0004fd8c + *(float *)PTR_DAT_0004fd88 +
                     *(float *)PTR_DAT_0004fd90,*(undefined4 *)puVar2,
                     *(undefined4 *)PTR_DAT_0004fd94);
  fVar6 = extraout_fr0;
LAB_0004fcd6:
  *(float *)PTR_DAT_0004fcec = fVar6;
  return uVar5;
}

