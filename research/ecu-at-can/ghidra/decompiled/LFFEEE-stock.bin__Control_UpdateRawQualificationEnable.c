/* Ghidra analysis output; verify against original SH instructions. */

/* Copies6CB4 to9108;914B=1 iff8<value<200, else0.40 boundary cases and1024 ADC1-scaled inputs;
   enables atcount410. Physical units open. See control-raw-enable.txt. */

void Control_UpdateRawQualificationEnable(void)

{
  float *pfVar1;
  undefined *puVar2;
  
  puVar2 = PTR_DAT_00074e90;
  pfVar1 = DAT_00074e88;
  *DAT_00074e88 = *(float *)PTR_Control_LocalFilterInput_00074e8c;
  if ((*(float *)PTR_DAT_00074e94 <= *pfVar1) || (*pfVar1 <= *(float *)PTR_DAT_00074e98)) {
    *puVar2 = 0;
  }
  else {
    *puVar2 = 1;
  }
  return;
}

