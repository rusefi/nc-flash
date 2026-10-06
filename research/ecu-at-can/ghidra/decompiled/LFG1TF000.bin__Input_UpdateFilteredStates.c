/* Ghidra analysis output; verify against original SH instructions. */

/* Thirty channels; first four assert/release thresholds2/2. ADC gate failure sets status3 and
   retains filtered value. Full body executed with explicit read-only register fixtures. */

void Input_UpdateFilteredStates(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  char *pcVar4;
  byte bVar5;
  char cVar6;
  undefined *puVar7;
  undefined *puVar8;
  int iVar9;
  
  puVar2 = PTR_DigitalInput_FilterDescriptors_00017338;
  puVar1 = PTR_DAT_00017334;
  iVar9 = 0;
  pcVar4 = PTR_DigitalInput_FilterDescriptors_00017338;
  puVar7 = PTR_DAT_00017334;
  puVar8 = PTR_DAT_00017334;
  do {
    if (0x1d < iVar9) {
      return;
    }
    cVar3 = (*(code *)PTR_Input_CheckADCGates_0001733c)((int)(char)puVar2[iVar9 * 0xc + 8]);
    if (cVar3 == '\x01') {
      puVar1[iVar9 * 5 + 2] = 3;
      puVar1[iVar9 * 5 + 1] = 0;
      puVar1[iVar9 * 5 + 4] = 0;
    }
    else {
      cVar3 = (*(code *)PTR_Input_ReadDigitalDescriptor_00017340)
                        (*(undefined4 *)(puVar2 + iVar9 * 0xc + 4));
      bVar5 = (puVar1 + iVar9 * 5)[1];
      if (puVar1[iVar9 * 5] == '\x01') {
        if (cVar3 == '\0') {
          bVar5 = bVar5 + 1;
          if ((byte)(puVar2 + iVar9 * 0xc)[1] <= bVar5) {
            puVar1[iVar9 * 5] = 0;
LAB_0001732e:
            bVar5 = 0;
          }
        }
        else {
joined_r0x00017348:
          if (bVar5 != 0) {
            bVar5 = bVar5 - 1;
          }
        }
      }
      else {
        if (cVar3 != '\x01') goto joined_r0x00017348;
        bVar5 = bVar5 + 1;
        if ((byte)puVar2[iVar9 * 0xc] <= bVar5) {
          puVar1[iVar9 * 5] = 1;
          goto LAB_0001732e;
        }
      }
      puVar1[iVar9 * 5 + 1] = bVar5;
      cVar6 = puVar1[iVar9 * 5 + 3];
      if (puVar1[iVar9 * 5 + 4] == '\0') {
        puVar1[iVar9 * 5 + 4] = 1;
        cVar6 = puVar2[iVar9 * 0xc + 1];
        if (cVar3 == '\x01') {
          cVar6 = *pcVar4;
        }
      }
      if (cVar6 != '\0') {
        cVar6 = cVar6 + -1;
      }
      if (cVar6 == '\0') {
        puVar7[2] = 2;
      }
      puVar8[3] = cVar6;
    }
    iVar9 = iVar9 + 1;
    puVar8 = puVar8 + 5;
    puVar7 = puVar7 + 5;
    pcVar4 = pcVar4 + 0xc;
  } while( true );
}

