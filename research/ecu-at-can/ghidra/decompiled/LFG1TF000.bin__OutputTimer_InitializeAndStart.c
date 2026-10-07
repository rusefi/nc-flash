/* Ghidra analysis output; verify against original SH instructions. */

/* Originaltimerregister writes verifiedall256 initialF401 bytes: stop2A/6/7,
   clear87F4/counters,33333 cycle/buffer/duty values,TCNT2A0/GR2A4166, start6A..D and2A. Exactaccess
   order in verifier. Priorclock/mode/pinsetup andrealcounting notsimulated. */

void OutputTimer_InitializeAndStart(void)

{
  undefined2 *puVar1;
  undefined2 *puVar2;
  undefined2 *puVar3;
  undefined2 uVar4;
  undefined1 *puVar5;
  byte *pbVar6;
  
  pbVar6 = (byte *)(int)DAT_00016a08;
  *pbVar6 = *pbVar6 & 0xfb;
  puVar5 = (undefined1 *)(int)DAT_00016a0a;
  *puVar5 = 0;
  OutputTimer_ClearPhase();
  puVar2 = (undefined2 *)(int)DAT_00016a0c;
  *puVar2 = 0;
  puVar3 = (undefined2 *)(int)DAT_00016a0e;
  *puVar3 = 0;
  puVar1 = (undefined2 *)(int)DAT_00016a10;
  *puVar1 = 0;
  puVar3[-2] = 0;
  uVar4 = (undefined2)DAT_00016a20;
  puVar2[2] = uVar4;
  puVar3[2] = uVar4;
  puVar1[6] = uVar4;
  puVar3[4] = uVar4;
  puVar2[6] = uVar4;
  puVar3[6] = uVar4;
  puVar1[10] = uVar4;
  puVar3[8] = uVar4;
  puVar2[10] = uVar4;
  puVar3[10] = uVar4;
  puVar1[0xe] = uVar4;
  puVar3[0xc] = uVar4;
  *puVar5 = 0;
  *(undefined2 *)(int)DAT_00016a12 = 0;
  *(undefined2 *)(int)DAT_00016a16 = DAT_00016a14;
  *puVar5 = 0xf;
  *pbVar6 = *pbVar6 | 4;
  return;
}

