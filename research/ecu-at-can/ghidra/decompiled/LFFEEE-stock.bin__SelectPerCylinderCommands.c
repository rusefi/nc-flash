/* Ghidra analysis output; verify against original SH instructions. */

/* Bit80 at78CF+cyl selects zero at7408+4*cyl. Verified paired TCU216 effect; final injector timer
   path remains open. */

uint SelectPerCylinderCommands(void)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  
  iVar3 = DAT_00045034;
  puVar2 = PTR_CylinderCutStatusBase_00045030;
  puVar1 = PTR_PerCylinderCommandBase_0004502c;
  uVar10 = *(undefined4 *)PTR_DAT_00045018;
  uVar9 = *(undefined4 *)PTR_DAT_0004501c;
  uVar8 = *(undefined4 *)PTR_DAT_00045020;
  uVar7 = *(undefined4 *)PTR_DAT_00045024;
  puVar6 = (undefined4 *)(PTR_PerCylinderCommandBase_0004502c + 4);
  uVar5 = (uint)(byte)*PTR_DAT_00045028;
  if (((int)(char)PTR_CylinderCutStatusBase_00045030[1] & 0x80U) == 0) {
    if ((*(byte *)(DAT_00045034 + 1) & 0x20) == 0) {
      if (uVar5 == 4) {
        *puVar6 = uVar10;
      }
      else if (uVar5 == 6) {
        *puVar6 = uVar9;
      }
      else if (uVar5 == 0) {
        *puVar6 = uVar8;
      }
    }
    else {
      *puVar6 = uVar7;
    }
  }
  else {
    *puVar6 = 0;
  }
  puVar6 = (undefined4 *)(puVar1 + 8);
  if (((int)(char)puVar2[2] & 0x80U) == 0) {
    if ((*(byte *)(iVar3 + 2) & 0x20) == 0) {
      if (uVar5 == 2) {
        *puVar6 = uVar10;
      }
      else if (uVar5 == 4) {
        *puVar6 = uVar9;
      }
      else if (uVar5 == 6) {
        *puVar6 = uVar8;
      }
    }
    else {
      *puVar6 = uVar7;
    }
  }
  else {
    *puVar6 = 0;
  }
  puVar6 = (undefined4 *)(puVar1 + 0xc);
  if (((int)(char)puVar2[3] & 0x80U) == 0) {
    if ((*(byte *)(iVar3 + 3) & 0x20) == 0) {
      if (uVar5 == 6) {
        *puVar6 = uVar10;
      }
      else if (uVar5 == 0) {
        *puVar6 = uVar9;
      }
      else if (uVar5 == 2) {
        *puVar6 = uVar8;
      }
    }
    else {
      *puVar6 = uVar7;
    }
  }
  else {
    *puVar6 = 0;
  }
  puVar6 = (undefined4 *)(puVar1 + 0x10);
  if (((int)(char)puVar2[4] & 0x80U) == 0) {
    uVar4 = -(((*(byte *)(iVar3 + 4) & 0x20) == 0) - 1);
    if (uVar4 == 1) {
      *puVar6 = uVar7;
      uVar5 = uVar4;
    }
    else if (uVar5 == 0) {
      *puVar6 = uVar10;
      uVar5 = uVar4;
    }
    else if (uVar5 == 2) {
      *puVar6 = uVar9;
    }
    else if (uVar5 == 4) {
      *puVar6 = uVar8;
    }
  }
  else {
    *puVar6 = 0;
    uVar5 = 1;
  }
  return uVar5;
}

