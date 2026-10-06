/* Ghidra analysis output; verify against original SH instructions. */

/* StockC90A0=1 chooses72C8 unlessA3A4==1 then72F8;207C clamp with72F4/72F0 to72FC.180 selection
   cases;physical meaning open. */

void Control_SelectAndLimitPublishedValue(void)

{
  char cVar1;
  undefined4 uVar2;
  
  if ((*PTR_DAT_0004227c == '\0') ||
     (cVar1 = (*(code *)PTR_FUN_00042284)(PTR_DAT_00042280), cVar1 == '\x01')) {
    uVar2 = *(undefined4 *)PTR_DAT_00042288;
  }
  else {
    uVar2 = *(undefined4 *)PTR_Control_PublishedInverseValue_0004228c;
  }
  uVar2 = (*(code *)PTR_FUN_00042298)
                    (uVar2,*(undefined4 *)PTR_DAT_00042294,*(undefined4 *)PTR_DAT_00042290);
  *(undefined4 *)PTR_Control_SelectedPublishedValue_0004229c = uVar2;
  return;
}

