/* Ghidra analysis output; verify against original SH instructions. */

/* Returnsbool(916F&1); verified abort priority fromstates2/3/4/5 through queue andheap release. See
   tcu-request-dispatch.txt. */

bool SparkRequest_GlobalReleaseGuard(void)

{
  return (*PTR_Request_CancellationFlags_0004cd14 & 1) != 0;
}

