/* Ghidra analysis output; verify against original SH instructions. */

/* Signed80B4*32/10 truncates then saturates16 via10D0C ->92E2/92E4. Also80B2 ->92E6 andA528 ->92D2
   flag. CAN215 conversion and diagnostic selection now executed end-to-end; see
   can215-feedback.txt. */

void SparkRequest_ConvertBaseInputs(void)

{
  undefined *puVar1;
  undefined2 uVar2;
  
  (*(code *)PTR_FUN_000217e8)();
  uVar2 = (*(code *)PTR_FixedPoint_DivideToSignedWord_000217ec)((int)SparkRequest_BaseInput << 5,10)
  ;
  puVar1 = PTR_SparkRequest_BaseValue_000217f4;
  *(undefined2 *)PTR_DAT_000217f0 = uVar2;
  *(undefined2 *)puVar1 = uVar2;
  uVar2 = (*(code *)PTR_FixedPoint_DivideToSignedWord_000217ec)
                    ((int)CAN215_SecondApplicationValue << 5,10);
  *DAT_000217f8 = uVar2;
  return;
}

