/* Ghidra analysis output; verify against original SH instructions. */

/* Full stock inverse mapsA25CC/A25E0,718C blend,offset andlimits toA660 verified in324 cases.
   Physical actuator identity unproved;control-conversion.txt. */

void Control_InvertAndBlendMaps(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined4 *puVar3;
  int iVar4;
  char cVar6;
  int iVar5;
  undefined1 uVar7;
  float fVar8;
  float fVar9;
  undefined4 uVar10;
  char acStack_10008 [65536];
  float local_8 [2];
  
  iVar4 = (int)DAT_000a50e0;
  fVar9 = (*(float *)PTR_Control_InverseTargetInput_000a50f8 * *(float *)PTR_DAT_000a50f4 *
          DAT_000a50fc) / *(float *)PTR_DAT_000a5100;
  *(float *)PTR_DAT_000a5104 = fVar9;
  *(undefined4 *)((int)local_8 + DAT_000a50e2 + iVar4) = *(undefined4 *)PTR_DAT_000a5108;
  *(undefined4 *)((int)local_8 + DAT_000a50e4 + iVar4) = *(undefined4 *)PTR_DAT_000a510c;
  uVar10 = *(undefined4 *)PTR_DAT_000a5110;
  *(undefined4 *)((int)local_8 + DAT_000a50e6 + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a511c)(uVar10,DAT_000a5114,DAT_000a5118);
  *(bool *)((int)local_8 + DAT_000a50e8 + iVar4) = fVar8 <= fVar9;
  uVar10 = DAT_000a5120;
  if (*(char *)((int)local_8 + DAT_000a50e8 + iVar4) == '\0') {
    uVar10 = 0;
  }
  *(undefined4 *)((int)local_8 + DAT_000a50ea + iVar4) = uVar10;
  uVar10 = DAT_000a5128;
  if (*(char *)((int)local_8 + DAT_000a50e8 + iVar4) != '\0') {
    uVar10 = DAT_000a5124;
  }
  *(undefined4 *)((int)local_8 + DAT_000a50ec + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a511c)
                           (*(undefined4 *)((int)local_8 + DAT_000a50e6 + iVar4),uVar10,DAT_000a5118
                           );
  fVar9 = *(float *)PTR_DAT_000a5104;
  *(bool *)((int)local_8 + DAT_000a50ee + iVar4) = fVar8 <= fVar9;
  uVar10 = DAT_000a512c;
  if (fVar8 > fVar9) {
    uVar10 = 0;
  }
  *(undefined4 *)((int)local_8 + DAT_000a50f0 + iVar4) = uVar10;
  if (*(char *)((int)local_8 + DAT_000a50ee + iVar4) == '\0') {
    uVar10 = DAT_000a5204;
    if (*(char *)((int)local_8 + DAT_000a50e8 + iVar4) != '\0') {
      uVar10 = DAT_000a5138;
    }
    *(undefined4 *)(&stack0x00000034 + iVar4) = uVar10;
  }
  else {
    uVar10 = DAT_000a5134;
    if (*(char *)((int)local_8 + DAT_000a50e8 + iVar4) != '\0') {
      uVar10 = DAT_000a5130;
    }
    *(undefined4 *)(&stack0x00000030 + iVar4) = uVar10;
  }
  *(undefined4 *)((int)local_8 + DAT_000a51f8 + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a520c)
                           (*(undefined4 *)((int)local_8 + DAT_000a51fa + iVar4),uVar10,DAT_000a5208
                           );
  fVar9 = *(float *)PTR_DAT_000a5210;
  *(bool *)((int)local_8 + DAT_000a51fc + iVar4) = fVar8 <= fVar9;
  uVar10 = DAT_000a5214;
  if (fVar8 > fVar9) {
    uVar10 = 0;
  }
  *(undefined4 *)((int)local_8 + DAT_000a51fe + iVar4) = uVar10;
  if (*(char *)((int)local_8 + DAT_000a51fc + iVar4) == '\0') {
    if (*(char *)((int)local_8 + DAT_000a5200 + iVar4) == '\0') {
      uVar10 = DAT_000a531c;
      if (*(char *)((int)local_8 + DAT_000a5202 + iVar4) != '\0') {
        uVar10 = DAT_000a5230;
      }
      *(undefined4 *)(&stack0x00000048 + iVar4) = uVar10;
    }
    else {
      uVar10 = DAT_000a522c;
      if (*(char *)((int)local_8 + DAT_000a5202 + iVar4) != '\0') {
        uVar10 = DAT_000a5228;
      }
      *(undefined4 *)(&stack0x00000044 + iVar4) = uVar10;
    }
    *(undefined4 *)(&stack0x0000004c + iVar4) = uVar10;
  }
  else {
    if (*(char *)((int)local_8 + DAT_000a5200 + iVar4) == '\0') {
      uVar10 = DAT_000a5224;
      if (*(char *)((int)local_8 + DAT_000a5202 + iVar4) != '\0') {
        uVar10 = DAT_000a5220;
      }
      *(undefined4 *)(&stack0x0000003c + iVar4) = uVar10;
    }
    else {
      uVar10 = DAT_000a521c;
      if (*(char *)((int)local_8 + DAT_000a5202 + iVar4) != '\0') {
        uVar10 = DAT_000a5218;
      }
      *(undefined4 *)(&stack0x00000038 + iVar4) = uVar10;
    }
    *(undefined4 *)(&stack0x00000040 + iVar4) = uVar10;
  }
  *(undefined4 *)((int)local_8 + DAT_000a530e + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a5324)
                           (*(undefined4 *)((int)local_8 + DAT_000a5310 + iVar4),uVar10,DAT_000a5320
                           );
  fVar9 = *(float *)PTR_DAT_000a5328;
  *(bool *)((int)local_8 + DAT_000a5312 + iVar4) = fVar8 <= fVar9;
  if (fVar8 <= fVar9) {
    uVar10 = 0x40000000;
  }
  else {
    uVar10 = 0;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5314 + iVar4) = uVar10;
  if (*(char *)((int)local_8 + DAT_000a5312 + iVar4) == '\0') {
    if (*(char *)((int)local_8 + DAT_000a53fa + iVar4) == '\0') {
      if (*(char *)((int)local_8 + DAT_000a53fc + iVar4) == '\0') {
        uVar10 = DAT_000a5420;
        if (*(char *)((int)local_8 + DAT_000a53fe + iVar4) != '\0') {
          uVar10 = DAT_000a541c;
        }
        *(undefined4 *)(&stack0x00000024 + iVar4) = uVar10;
      }
      else {
        uVar10 = DAT_000a5418;
        if (*(char *)((int)local_8 + DAT_000a53fe + iVar4) != '\0') {
          uVar10 = DAT_000a5414;
        }
        *(undefined4 *)(&stack0x00000020 + iVar4) = uVar10;
      }
      *(undefined4 *)(&stack0x00000028 + iVar4) = uVar10;
    }
    else {
      if (*(char *)((int)local_8 + DAT_000a53fc + iVar4) == '\0') {
        uVar10 = DAT_000a5410;
        if (*(char *)((int)local_8 + DAT_000a53fe + iVar4) != '\0') {
          uVar10 = DAT_000a540c;
        }
        *(undefined4 *)(&stack0x00000018 + iVar4) = uVar10;
      }
      else {
        uVar10 = DAT_000a5408;
        if (*(char *)((int)local_8 + DAT_000a53fe + iVar4) != '\0') {
          uVar10 = DAT_000a5404;
        }
        *(undefined4 *)(&stack0x00000014 + iVar4) = uVar10;
      }
      *(undefined4 *)(&stack0x0000001c + iVar4) = uVar10;
    }
    *(undefined4 *)(&stack0x0000002c + iVar4) = uVar10;
  }
  else {
    if (*(char *)((int)local_8 + DAT_000a5316 + iVar4) == '\0') {
      if (*(char *)((int)local_8 + DAT_000a5318 + iVar4) == '\0') {
        uVar10 = DAT_000a5348;
        if (*(char *)((int)local_8 + DAT_000a531a + iVar4) != '\0') {
          uVar10 = DAT_000a5344;
        }
        *(undefined4 *)(&stack0x00000008 + iVar4) = uVar10;
      }
      else {
        uVar10 = DAT_000a5340;
        if (*(char *)((int)local_8 + DAT_000a531a + iVar4) != '\0') {
          uVar10 = DAT_000a533c;
        }
        *(undefined4 *)(&stack0x00000004 + iVar4) = uVar10;
      }
      *(undefined4 *)(&stack0x0000000c + iVar4) = uVar10;
    }
    else {
      if (*(char *)((int)local_8 + DAT_000a5318 + iVar4) == '\0') {
        uVar10 = DAT_000a5338;
        if (*(char *)((int)local_8 + DAT_000a531a + iVar4) != '\0') {
          uVar10 = DAT_000a5334;
        }
        *(undefined4 *)((int)local_8 + iVar4 + 4) = uVar10;
      }
      else {
        uVar10 = DAT_000a5330;
        if (*(char *)((int)local_8 + DAT_000a531a + iVar4) != '\0') {
          uVar10 = DAT_000a532c;
        }
        *(undefined4 *)((int)local_8 + iVar4) = uVar10;
      }
      *(undefined4 *)(&stack0x00000000 + iVar4) = uVar10;
    }
    *(undefined4 *)(&stack0x00000010 + iVar4) = uVar10;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5400 + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a5428)
                           (*(undefined4 *)((int)local_8 + DAT_000a5402 + iVar4),uVar10,DAT_000a5424
                           );
  if (*(float *)PTR_DAT_000a542c < fVar8) {
    uVar10 = 0;
  }
  else {
    uVar10 = 0x3f800000;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5478 + iVar4) = uVar10;
  fVar8 = *(float *)((int)local_8 + DAT_000a547c + iVar4) +
          *(float *)((int)local_8 + DAT_000a547a + iVar4) +
          *(float *)((int)local_8 + DAT_000a547e + iVar4) +
          *(float *)((int)local_8 + DAT_000a5480 + iVar4) +
          *(float *)((int)local_8 + DAT_000a5478 + iVar4) + 1.0;
  *(float *)((int)local_8 + DAT_000a5480 + iVar4) = fVar8;
  uVar10 = DAT_000a55f0;
  switch((int)fVar8) {
  case 1:
    uVar10 = DAT_000a5580;
    break;
  case 2:
    uVar10 = DAT_000a5584;
    break;
  case 3:
    uVar10 = DAT_000a5588;
    break;
  case 4:
    uVar10 = DAT_000a558c;
    break;
  case 5:
    uVar10 = DAT_000a5590;
    break;
  case 6:
    uVar10 = DAT_000a5594;
    break;
  case 7:
    uVar10 = DAT_000a5598;
    break;
  case 8:
    uVar10 = DAT_000a559c;
    break;
  case 9:
    uVar10 = DAT_000a55a0;
    break;
  case 10:
    uVar10 = DAT_000a55a4;
    break;
  case 0xb:
    uVar10 = DAT_000a55a8;
    break;
  case 0xc:
    uVar10 = DAT_000a55ac;
    break;
  case 0xd:
    uVar10 = DAT_000a55b0;
    break;
  case 0xe:
    uVar10 = DAT_000a55b4;
    break;
  case 0xf:
    uVar10 = DAT_000a55b8;
    break;
  case 0x10:
    uVar10 = DAT_000a55bc;
    break;
  case 0x11:
    uVar10 = DAT_000a55c0;
    break;
  case 0x12:
    uVar10 = DAT_000a55c4;
    break;
  case 0x13:
    uVar10 = DAT_000a55c8;
    break;
  case 0x14:
    uVar10 = DAT_000a55cc;
    break;
  case 0x15:
    uVar10 = DAT_000a55d0;
    break;
  case 0x16:
    uVar10 = DAT_000a55d4;
    break;
  case 0x17:
    uVar10 = DAT_000a55d8;
    break;
  case 0x18:
    uVar10 = DAT_000a55dc;
    break;
  case 0x19:
    uVar10 = DAT_000a55e0;
    break;
  case 0x1a:
    uVar10 = DAT_000a55e4;
    break;
  case 0x1b:
    uVar10 = DAT_000a55e8;
    break;
  case 0x1c:
    uVar10 = DAT_000a55ec;
    break;
  case 0x1d:
    break;
  case 0x1e:
    break;
  case 0x1f:
    break;
  case 0x20:
    uVar10 = DAT_000a5624;
    break;
  default:
    goto switchD_000a5474_default;
  }
  *(undefined4 *)((int)local_8 + DAT_000a561e + iVar4) = uVar10;
switchD_000a5474_default:
  uVar10 = DAT_000a578c;
  switch((int)*(float *)((int)local_8 + DAT_000a5620 + iVar4)) {
  case 1:
    uVar10 = 0;
    break;
  case 2:
    uVar10 = DAT_000a5720;
    break;
  case 3:
    uVar10 = DAT_000a5724;
    break;
  case 4:
    uVar10 = DAT_000a5728;
    break;
  case 5:
    uVar10 = DAT_000a572c;
    break;
  case 6:
    uVar10 = DAT_000a5730;
    break;
  case 7:
    uVar10 = DAT_000a5734;
    break;
  case 8:
    uVar10 = DAT_000a5738;
    break;
  case 9:
    uVar10 = DAT_000a573c;
    break;
  case 10:
    uVar10 = DAT_000a5740;
    break;
  case 0xb:
    uVar10 = DAT_000a5744;
    break;
  case 0xc:
    uVar10 = DAT_000a5748;
    break;
  case 0xd:
    uVar10 = DAT_000a574c;
    break;
  case 0xe:
    uVar10 = DAT_000a5750;
    break;
  case 0xf:
    uVar10 = DAT_000a5754;
    break;
  case 0x10:
    uVar10 = DAT_000a5758;
    break;
  case 0x11:
    uVar10 = DAT_000a575c;
    break;
  case 0x12:
    uVar10 = DAT_000a5760;
    break;
  case 0x13:
    uVar10 = DAT_000a5764;
    break;
  case 0x14:
    uVar10 = DAT_000a5768;
    break;
  case 0x15:
    uVar10 = DAT_000a576c;
    break;
  case 0x16:
    uVar10 = DAT_000a5770;
    break;
  case 0x17:
    uVar10 = DAT_000a5774;
    break;
  case 0x18:
    uVar10 = DAT_000a5778;
    break;
  case 0x19:
    uVar10 = DAT_000a577c;
    break;
  case 0x1a:
    uVar10 = DAT_000a5780;
    break;
  case 0x1b:
    uVar10 = DAT_000a5784;
    break;
  case 0x1c:
    uVar10 = DAT_000a5788;
    break;
  case 0x1d:
    break;
  case 0x1e:
    break;
  case 0x1f:
    break;
  case 0x20:
    uVar10 = DAT_000a5898;
    break;
  default:
    goto switchD_000a561a_default;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5880 + iVar4) = uVar10;
switchD_000a561a_default:
  uVar10 = (*(code *)PTR_Lookup_FloatMap2D_000a58a0)
                     (*(undefined4 *)((int)local_8 + DAT_000a5882 + iVar4),
                      *(undefined4 *)((int)local_8 + DAT_000a5880 + iVar4),DAT_000a589c);
  *(undefined4 *)((int)local_8 + DAT_000a5884 + iVar4) = uVar10;
  uVar10 = (*(code *)PTR_Lookup_FloatMap2D_000a58a0)
                     (*(undefined4 *)((int)local_8 + DAT_000a5882 + iVar4),
                      *(undefined4 *)((int)local_8 + DAT_000a5886 + iVar4),DAT_000a589c);
  *(undefined4 *)((int)local_8 + DAT_000a5888 + iVar4) = uVar10;
  *(undefined4 *)((int)local_8 + DAT_000a588a + iVar4) =
       *(undefined4 *)PTR_Control_InverseBlendWeight_000a58a4;
  cVar6 = (*(code *)PTR_FUN_000a58ac)(PTR_DAT_000a58a8);
  if (cVar6 == '\0') {
    fVar8 = *(float *)((int)local_8 + DAT_000a588a + iVar4) - *(float *)PTR_DAT_000a58b4;
  }
  else {
    fVar8 = *(float *)PTR_DAT_000a58b0 + *(float *)((int)local_8 + DAT_000a588a + iVar4);
  }
  *(float *)((int)local_8 + DAT_000a588c + iVar4) = fVar8;
  if (fVar8 < 1.0) {
    if (0.0 < fVar8) {
      uVar10 = *(undefined4 *)((int)local_8 + DAT_000a588c + iVar4);
    }
    else {
      uVar10 = 0;
    }
    *(undefined4 *)((int)local_8 + DAT_000a588e + iVar4) = uVar10;
  }
  else {
    *(undefined4 *)((int)local_8 + DAT_000a588e + iVar4) = 0x3f800000;
  }
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a58a0)
                           (*(undefined4 *)((int)local_8 + DAT_000a5882 + iVar4),DAT_000a58b8,
                            DAT_000a58bc);
  fVar9 = *(float *)PTR_DAT_000a58c0;
  *(bool *)((int)local_8 + DAT_000a5890 + iVar4) = fVar8 <= fVar9;
  uVar10 = DAT_000a58c4;
  if (fVar8 > fVar9) {
    uVar10 = 0;
  }
  *(undefined4 *)((int)local_8 + DAT_000a588c + iVar4) = uVar10;
  uVar10 = DAT_000a58cc;
  if (*(char *)((int)local_8 + DAT_000a5890 + iVar4) != '\0') {
    uVar10 = DAT_000a58c8;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5892 + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a58a0)
                           (*(undefined4 *)((int)local_8 + DAT_000a5882 + iVar4),uVar10,DAT_000a58bc
                           );
  fVar9 = *(float *)PTR_DAT_000a58c0;
  *(bool *)((int)local_8 + DAT_000a5894 + iVar4) = fVar8 <= fVar9;
  uVar10 = DAT_000a58d0;
  if (fVar8 > fVar9) {
    uVar10 = 0;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5996 + iVar4) = uVar10;
  if (*(char *)((int)local_8 + DAT_000a5998 + iVar4) == '\0') {
    uVar10 = DAT_000a59bc;
    if (*(char *)((int)local_8 + DAT_000a599a + iVar4) != '\0') {
      uVar10 = DAT_000a59b8;
    }
    *(undefined4 *)((int)local_8 + DAT_000a599e + iVar4) = uVar10;
  }
  else {
    uVar10 = DAT_000a59b4;
    if (*(char *)((int)local_8 + DAT_000a599a + iVar4) != '\0') {
      uVar10 = DAT_000a59b0;
    }
    *(undefined4 *)((int)local_8 + DAT_000a599c + iVar4) = uVar10;
  }
  *(undefined4 *)((int)local_8 + DAT_000a59a0 + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a59c4)
                           (*(undefined4 *)((int)local_8 + DAT_000a59a2 + iVar4),uVar10,DAT_000a59c0
                           );
  fVar9 = *(float *)PTR_DAT_000a59c8;
  *(bool *)((int)local_8 + DAT_000a59a4 + iVar4) = fVar8 <= fVar9;
  uVar10 = DAT_000a59cc;
  if (fVar8 > fVar9) {
    uVar10 = 0;
  }
  *(undefined4 *)((int)local_8 + DAT_000a59a6 + iVar4) = uVar10;
  if (*(char *)((int)local_8 + DAT_000a59a4 + iVar4) == '\0') {
    if (*(char *)((int)local_8 + DAT_000a5aaa + iVar4) == '\0') {
      uVar10 = DAT_000a5acc;
      if (*(char *)((int)local_8 + DAT_000a5aac + iVar4) != '\0') {
        uVar10 = DAT_000a5ac8;
      }
      *(undefined4 *)((int)local_8 + DAT_000a5ab0 + iVar4) = uVar10;
    }
    else {
      uVar10 = DAT_000a5ac4;
      if (*(char *)((int)local_8 + DAT_000a5aac + iVar4) != '\0') {
        uVar10 = DAT_000a5ac0;
      }
      *(undefined4 *)((int)local_8 + DAT_000a5aae + iVar4) = uVar10;
    }
    *(undefined4 *)((int)local_8 + DAT_000a5ab2 + iVar4) = uVar10;
  }
  else {
    if (*(char *)((int)local_8 + DAT_000a5998 + iVar4) == '\0') {
      uVar10 = DAT_000a59dc;
      if (*(char *)((int)local_8 + DAT_000a599a + iVar4) != '\0') {
        uVar10 = DAT_000a59d8;
      }
      *(undefined4 *)((int)local_8 + DAT_000a59aa + iVar4) = uVar10;
    }
    else {
      uVar10 = DAT_000a59d4;
      if (*(char *)((int)local_8 + DAT_000a599a + iVar4) != '\0') {
        uVar10 = DAT_000a59d0;
      }
      *(undefined4 *)((int)local_8 + DAT_000a59a8 + iVar4) = uVar10;
    }
    *(undefined4 *)((int)local_8 + DAT_000a59ac + iVar4) = uVar10;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5ab4 + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a5ad4)
                           (*(undefined4 *)((int)local_8 + DAT_000a5ab6 + iVar4),uVar10,DAT_000a5ad0
                           );
  fVar9 = *(float *)PTR_DAT_000a5ad8;
  *(bool *)((int)local_8 + DAT_000a5ab8 + iVar4) = fVar8 <= fVar9;
  if (fVar8 <= fVar9) {
    uVar10 = 0x40000000;
  }
  else {
    uVar10 = 0;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5aba + iVar4) = uVar10;
  if (*(char *)((int)local_8 + DAT_000a5ab8 + iVar4) == '\0') {
    if (*(char *)((int)local_8 + DAT_000a5bb6 + iVar4) == '\0') {
      if (*(char *)((int)local_8 + DAT_000a5bb2 + iVar4) == '\0') {
        uVar10 = DAT_000a5c20;
        if (*(char *)((int)local_8 + DAT_000a5bb4 + iVar4) != '\0') {
          uVar10 = DAT_000a5be4;
        }
        *(undefined4 *)((int)local_8 + DAT_000a5c16 + iVar4) = uVar10;
      }
      else {
        uVar10 = DAT_000a5be0;
        if (*(char *)((int)local_8 + DAT_000a5bb4 + iVar4) != '\0') {
          uVar10 = DAT_000a5bdc;
        }
        *(undefined4 *)((int)local_8 + DAT_000a5bb8 + iVar4) = uVar10;
      }
      *(undefined4 *)((int)local_8 + DAT_000a5c18 + iVar4) = uVar10;
    }
    else {
      if (*(char *)((int)local_8 + DAT_000a5bb2 + iVar4) == '\0') {
        uVar10 = DAT_000a5bd8;
        if (*(char *)((int)local_8 + DAT_000a5bb4 + iVar4) != '\0') {
          uVar10 = DAT_000a5bd4;
        }
        *(undefined4 *)(&stack0x00000070 + iVar4) = uVar10;
      }
      else {
        uVar10 = DAT_000a5bd0;
        if (*(char *)((int)local_8 + DAT_000a5bb4 + iVar4) != '\0') {
          uVar10 = DAT_000a5bcc;
        }
        *(undefined4 *)(&stack0x0000006c + iVar4) = uVar10;
      }
      *(undefined4 *)(&stack0x00000074 + iVar4) = uVar10;
    }
    *(undefined4 *)((int)local_8 + DAT_000a5c1a + iVar4) = uVar10;
  }
  else {
    if (*(char *)((int)local_8 + DAT_000a5abc + iVar4) == '\0') {
      if (*(char *)((int)local_8 + DAT_000a5bb2 + iVar4) == '\0') {
        uVar10 = DAT_000a5bc8;
        if (*(char *)((int)local_8 + DAT_000a5bb4 + iVar4) != '\0') {
          uVar10 = DAT_000a5bc4;
        }
        *(undefined4 *)(&stack0x00000060 + iVar4) = uVar10;
      }
      else {
        uVar10 = DAT_000a5bc0;
        if (*(char *)((int)local_8 + DAT_000a5bb4 + iVar4) != '\0') {
          uVar10 = DAT_000a5bbc;
        }
        *(undefined4 *)(&stack0x0000005c + iVar4) = uVar10;
      }
      *(undefined4 *)(&stack0x00000064 + iVar4) = uVar10;
    }
    else {
      if (*(char *)((int)local_8 + DAT_000a5aaa + iVar4) == '\0') {
        uVar10 = DAT_000a5ae8;
        if (*(char *)((int)local_8 + DAT_000a5aac + iVar4) != '\0') {
          uVar10 = DAT_000a5ae4;
        }
        *(undefined4 *)(&stack0x00000054 + iVar4) = uVar10;
      }
      else {
        uVar10 = DAT_000a5ae0;
        if (*(char *)((int)local_8 + DAT_000a5aac + iVar4) != '\0') {
          uVar10 = DAT_000a5adc;
        }
        *(undefined4 *)(&stack0x00000050 + iVar4) = uVar10;
      }
      *(undefined4 *)(&stack0x00000058 + iVar4) = uVar10;
    }
    *(undefined4 *)(&stack0x00000068 + iVar4) = uVar10;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5c1c + iVar4) = uVar10;
  fVar8 = (float)(*(code *)PTR_Lookup_FloatMap2D_000a5c28)
                           (*(undefined4 *)((int)local_8 + DAT_000a5c1e + iVar4),uVar10,DAT_000a5c24
                           );
  if (*(float *)PTR_DAT_000a5c2c < fVar8) {
    uVar10 = 0;
  }
  else {
    uVar10 = 0x3f800000;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5c78 + iVar4) = uVar10;
  fVar8 = *(float *)((int)local_8 + DAT_000a5c7c + iVar4) +
          *(float *)((int)local_8 + DAT_000a5c7a + iVar4) +
          *(float *)((int)local_8 + DAT_000a5c7e + iVar4) +
          *(float *)((int)local_8 + DAT_000a5c78 + iVar4) +
          *(float *)((int)local_8 + DAT_000a5c80 + iVar4) + 1.0;
  *(float *)((int)local_8 + DAT_000a5c80 + iVar4) = fVar8;
  uVar10 = DAT_000a5df0;
  switch((int)fVar8) {
  case 1:
    uVar10 = DAT_000a5d80;
    break;
  case 2:
    uVar10 = DAT_000a5d84;
    break;
  case 3:
    uVar10 = DAT_000a5d88;
    break;
  case 4:
    uVar10 = DAT_000a5d8c;
    break;
  case 5:
    uVar10 = DAT_000a5d90;
    break;
  case 6:
    uVar10 = DAT_000a5d94;
    break;
  case 7:
    uVar10 = DAT_000a5d98;
    break;
  case 8:
    uVar10 = DAT_000a5d9c;
    break;
  case 9:
    uVar10 = DAT_000a5da0;
    break;
  case 10:
    uVar10 = DAT_000a5da4;
    break;
  case 0xb:
    uVar10 = DAT_000a5da8;
    break;
  case 0xc:
    uVar10 = DAT_000a5dac;
    break;
  case 0xd:
    uVar10 = DAT_000a5db0;
    break;
  case 0xe:
    uVar10 = DAT_000a5db4;
    break;
  case 0xf:
    uVar10 = DAT_000a5db8;
    break;
  case 0x10:
    uVar10 = DAT_000a5dbc;
    break;
  case 0x11:
    uVar10 = DAT_000a5dc0;
    break;
  case 0x12:
    uVar10 = DAT_000a5dc4;
    break;
  case 0x13:
    uVar10 = DAT_000a5dc8;
    break;
  case 0x14:
    uVar10 = DAT_000a5dcc;
    break;
  case 0x15:
    uVar10 = DAT_000a5dd0;
    break;
  case 0x16:
    uVar10 = DAT_000a5dd4;
    break;
  case 0x17:
    uVar10 = DAT_000a5dd8;
    break;
  case 0x18:
    uVar10 = DAT_000a5ddc;
    break;
  case 0x19:
    uVar10 = DAT_000a5de0;
    break;
  case 0x1a:
    uVar10 = DAT_000a5de4;
    break;
  case 0x1b:
    uVar10 = DAT_000a5de8;
    break;
  case 0x1c:
    uVar10 = DAT_000a5dec;
    break;
  case 0x1d:
    break;
  case 0x1e:
    break;
  case 0x1f:
    break;
  case 0x20:
    uVar10 = DAT_000a5e24;
    break;
  default:
    goto switchD_000a5c74_default;
  }
  *(undefined4 *)((int)local_8 + DAT_000a5e1e + iVar4) = uVar10;
switchD_000a5c74_default:
  uVar10 = DAT_000a5f8c;
  switch((int)*(float *)((int)local_8 + DAT_000a5e20 + iVar4)) {
  case 1:
    uVar10 = 0;
    break;
  case 2:
    uVar10 = DAT_000a5f20;
    break;
  case 3:
    uVar10 = DAT_000a5f24;
    break;
  case 4:
    uVar10 = DAT_000a5f28;
    break;
  case 5:
    uVar10 = DAT_000a5f2c;
    break;
  case 6:
    uVar10 = DAT_000a5f30;
    break;
  case 7:
    uVar10 = DAT_000a5f34;
    break;
  case 8:
    uVar10 = DAT_000a5f38;
    break;
  case 9:
    uVar10 = DAT_000a5f3c;
    break;
  case 10:
    uVar10 = DAT_000a5f40;
    break;
  case 0xb:
    uVar10 = DAT_000a5f44;
    break;
  case 0xc:
    uVar10 = DAT_000a5f48;
    break;
  case 0xd:
    uVar10 = DAT_000a5f4c;
    break;
  case 0xe:
    uVar10 = DAT_000a5f50;
    break;
  case 0xf:
    uVar10 = DAT_000a5f54;
    break;
  case 0x10:
    uVar10 = DAT_000a5f58;
    break;
  case 0x11:
    uVar10 = DAT_000a5f5c;
    break;
  case 0x12:
    uVar10 = DAT_000a5f60;
    break;
  case 0x13:
    uVar10 = DAT_000a5f64;
    break;
  case 0x14:
    uVar10 = DAT_000a5f68;
    break;
  case 0x15:
    uVar10 = DAT_000a5f6c;
    break;
  case 0x16:
    uVar10 = DAT_000a5f70;
    break;
  case 0x17:
    uVar10 = DAT_000a5f74;
    break;
  case 0x18:
    uVar10 = DAT_000a5f78;
    break;
  case 0x19:
    uVar10 = DAT_000a5f7c;
    break;
  case 0x1a:
    uVar10 = DAT_000a5f80;
    break;
  case 0x1b:
    uVar10 = DAT_000a5f84;
    break;
  case 0x1c:
    uVar10 = DAT_000a5f88;
    break;
  case 0x1d:
    break;
  case 0x1e:
    break;
  case 0x1f:
    break;
  case 0x20:
    uVar10 = DAT_000a60a0;
    break;
  default:
    goto switchD_000a5e1a_default;
  }
  *(undefined4 *)((int)local_8 + DAT_000a6086 + iVar4) = uVar10;
switchD_000a5e1a_default:
  uVar10 = (*(code *)PTR_Lookup_FloatMap2D_000a60a8)
                     (*(undefined4 *)((int)local_8 + DAT_000a6088 + iVar4),
                      *(undefined4 *)((int)local_8 + DAT_000a6086 + iVar4),DAT_000a60a4);
  *(undefined4 *)((int)local_8 + DAT_000a608a + iVar4) = uVar10;
  uVar10 = (*(code *)PTR_Lookup_FloatMap2D_000a60a8)
                     (*(undefined4 *)((int)local_8 + DAT_000a6088 + iVar4),
                      *(undefined4 *)((int)local_8 + DAT_000a608c + iVar4),DAT_000a60a4);
  *(undefined4 *)((int)local_8 + DAT_000a608e + iVar4) = uVar10;
  if (*PTR_DAT_000a60ac == '\0') {
    fVar9 = *(float *)((int)local_8 + DAT_000a6092 + iVar4);
    *(float *)((int)local_8 + DAT_000a6096 + iVar4) =
         *(float *)((int)local_8 + DAT_000a6094 + iVar4) - fVar9;
    fVar8 = DAT_000a60c4;
    if ((*(float *)((int)local_8 + DAT_000a6096 + iVar4) < DAT_000a60c4) &&
       (fVar8 = DAT_000a60c8, DAT_000a60c8 < *(float *)((int)local_8 + DAT_000a6096 + iVar4))) {
      fVar8 = *(float *)((int)local_8 + DAT_000a6096 + iVar4);
    }
    *(float *)PTR_Control_InverseBaseResult_000a60cc =
         ((*(float *)((int)local_8 + DAT_000a6094 + iVar4) - *(float *)PTR_DAT_000a60c0) *
          *(float *)((int)local_8 + DAT_000a6098 + iVar4) +
         (*(float *)PTR_DAT_000a60c0 - fVar9) * *(float *)((int)local_8 + DAT_000a609a + iVar4)) /
         fVar8;
    puVar1 = PTR_Control_InverseActiveResult_000a61e4;
    fVar9 = *(float *)((int)local_8 + DAT_000a608a + iVar4);
    *(float *)((int)local_8 + DAT_000a609c + iVar4) =
         *(float *)((int)local_8 + DAT_000a608e + iVar4) - fVar9;
    fVar8 = DAT_000a60c4;
    if ((*(float *)((int)local_8 + DAT_000a609c + iVar4) < DAT_000a60c4) &&
       (fVar8 = DAT_000a60c8, DAT_000a60c8 < *(float *)((int)local_8 + DAT_000a609c + iVar4))) {
      fVar8 = *(float *)((int)local_8 + DAT_000a61d8 + iVar4);
    }
    *(float *)PTR_Control_InverseActiveResult_000a61e4 =
         ((*(float *)((int)local_8 + DAT_000a608e + iVar4) - *(float *)PTR_DAT_000a60c0) *
          *(float *)((int)local_8 + DAT_000a6086 + iVar4) +
         (*(float *)PTR_DAT_000a60c0 - fVar9) * *(float *)((int)local_8 + DAT_000a608c + iVar4)) /
         fVar8;
    puVar2 = PTR_DAT_000a61ec;
    fVar8 = *(float *)((int)local_8 + DAT_000a61da + iVar4);
    iVar5 = (int)DAT_000a61dc;
    *(float *)PTR_DAT_000a61ec =
         *(float *)puVar1 * fVar8 + (1.0 - fVar8) * *(float *)PTR_Control_InverseBaseResult_000a61e8
    ;
    puVar1 = PTR_DAT_000a61f0;
    fVar8 = *(float *)puVar2 - *(float *)((int)local_8 + iVar5 + iVar4);
    *(float *)PTR_DAT_000a61f0 = fVar8;
    puVar2 = PTR_DAT_000a61f4;
    if (fVar8 < 0.0) {
      uVar10 = 0;
    }
    else {
      uVar10 = *(undefined4 *)puVar1;
    }
    *(undefined4 *)PTR_DAT_000a61f4 = uVar10;
    *(undefined4 *)PTR_DAT_000a61f8 = *(undefined4 *)puVar2;
  }
  else {
    uVar10 = (*(code *)PTR_Lookup_FloatCurve_000a60b4)
                       (*(undefined4 *)((int)local_8 + DAT_000a6090 + iVar4),DAT_000a60b0);
    *(undefined4 *)PTR_DAT_000a60b8 = uVar10;
    *(undefined4 *)PTR_DAT_000a60bc = uVar10;
  }
  uVar10 = (*(code *)PTR_Lookup_FloatCurve_000a6200)
                     (*(undefined4 *)((int)local_8 + DAT_000a61de + iVar4),DAT_000a61fc);
  *(undefined4 *)PTR_DAT_000a6204 = uVar10;
  uVar10 = (*(code *)PTR_Lookup_FloatCurve_000a6200)
                     (*(undefined4 *)((int)local_8 + DAT_000a61de + iVar4),DAT_000a6208);
  *(undefined4 *)PTR_DAT_000a620c = uVar10;
  if (*PTR_DAT_000a6210 == '\0') {
    fVar8 = *(float *)PTR_DAT_000a61f8;
    if (*(float *)PTR_DAT_000a6204 < *(float *)PTR_DAT_000a61f8) {
      fVar8 = *(float *)PTR_DAT_000a6204;
    }
    *(float *)((int)local_8 + DAT_000a61e0 + iVar4) = fVar8;
    if (fVar8 < *(float *)PTR_DAT_000a620c) {
      fVar8 = *(float *)PTR_DAT_000a620c;
    }
    *(float *)PTR_Control_LimitedInverseValue_000a6218 = fVar8;
  }
  else {
    *(float *)PTR_Control_LimitedInverseValue_000a6218 =
         *(float *)PTR_DAT_000a6214 - *(float *)((int)local_8 + DAT_000a61dc + iVar4);
  }
  puVar3 = DAT_000a6220;
  if ((*(float *)PTR_DAT_000a6204 <= *(float *)PTR_DAT_000a61f8) ||
     (*(float *)PTR_DAT_000a61f8 <= *(float *)PTR_DAT_000a620c)) {
    uVar7 = 1;
  }
  else {
    uVar7 = 0;
  }
  *PTR_DAT_000a621c = uVar7;
  *puVar3 = *(undefined4 *)((int)local_8 + DAT_000a61da + iVar4);
  return;
}

