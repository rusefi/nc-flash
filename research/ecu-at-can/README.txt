Current full-scope completion audit: completion-audit.txt (allthree incomplete).
OlderSH7055 manual does notresolve counterwidth; see CHECKPOINT for nextactions.

Latest down-count startup: tcu-downcount-startup.txt; full15574 reaches
TCNT0 access-width conflict1461A/F430. All scopes open; see CHECKPOINT.txt.

Latest interval startup: tcu-interval-startup.txt; strict145FE checks PASS,
full15574 stops14978/F666. All three scopes remain open; see CHECKPOINT.txt.

LATEST 2026-10-07: tcu-basic-hardware-startup.txt verifies UBC/BSC/DMAOR original
setup and advances full15574 to14602 bytewriteF4240 (ITVRR1). WCR reset-source
conflict and read-before-clear DMA errors remain explicit. All earlier stops
retained. CHECKPOINT owns verified archive/current next step/all three scopes.

LATEST 2026-10-07: tcu-native-can-lifecycle.txt completes320 native task periods
with1310 CAN IRQs/960frames/27ack RAM checks. Lastphase remains; oldforced-mode
lifecycle differs. tcu-icr-startup.txt verifies ICR/zeroIRQstatus and advances
full15574 to UBARH EC00. CHECKPOINT owns Ghidra refresh/all three open scopes.

LATEST 2026-10-07: tcu-hardware-startup.txt identifies original1570C recovery-flag
writes;256 independent RAM cases PASS. Full15574 stops at ICR ED18=00FF before
this tail. Native task timelines omit this prerequisite; do not force flags.
tcu-native-can-lifecycle.txt tracks320 periods and observer regression; CHECKPOINT
owns live run/archive status and all three broader requirements.

LATEST 2026-10-07: tcu-can-task-interrupt.txt verifies original CAN task admission
and timer:3072 gate/20 ISR cases, plus native timeline600 interrupts/432 frames.
CAN readiness precedes application readiness; missing traffic still faults.
Next320 native periods/request lifecycle. CHECKPOINT owns all three scopes.

LATEST 2026-10-07: tcu-hcan-startup.txt completes original11FA0 withnative
8003=1/8F6C0A;256HCAN+256timer wholeRAM/MMIO cases PASS,10fixture rejections.
Fullcallercoverage usesexternalGSR8/0; nohardwareproof. Diagnosticdefault and
oldstrictprobe outputs byte-identical. Next nativeCANIRQ1669A/11FB2 admission
andreceipts inexistingnative timeline. CHECKPOINT owns allthreegoals/Ghidra.

LATEST 2026-10-07: tcu-native-capture-startup.txt joins originalreadiness with
291CMT1/1293A+Bcapture interrupts. Three traces PASS; correctedandretainedA-only
fixturedefect. Nativegroup initialization differs209bytes versusoldsetup.
Next nativeCAN11FA0/HCANBCR configuration; probe stopsE402 withoutforcedmode8.
CHECKPOINT owns allthreegoals/currentGhidrarestore andseparate nextactions.

LATEST 2026-10-07: tcu-diagnostic-startup.txt joins original1217C initialization
and1218E admission into native readiness: three traces,24diagnostic/144application/
600CMT0 events PASS, no forcedmode3. Retained default outputs byte-identical.
Next native CAN/capture/CMT1 join; allthree broader scopes remain open.
CHECKPOINT owns current Ghidra save/restore and separate next actions.

LATEST 2026-10-07: tcu-readiness-admission.txt joinsnativeinitializers,
foregroundADC callers, CMT0 andapplicationinterrupts. Three retainedtraces:
450CMT0/108application/168foreground checks,93actualcapture-return RAMchecks,
216command-pin checks PASS. Mode3 reachedwithoutforcedreadyflags, one IRQafter
capturestate3. Refactoredhelper oldJSONs byte-identical. Nextnative diagnostic
admission andexistingCAN/capturetimeline join; fullreset/mainloop/physicalproof
stillopen. CHECKPOINT owns currentGhidrarestore andseparateallthreegoals.
Previous capture/timestamp proofs: tcu-capture-readiness.txt and
tcu-timestamp-configuration.txt. Counterreset-width conflict remains explicit.

LATEST 2026-10-07: tcu-capture-timeline.txt completes320 shared-clock cycles:
2602capture/1310CMT0/640CMT1,80hold/640command-pin checks PASS. Logger-only
alias defect preserved/validated; corrected9 matchesnormalizedfullfirst9.
Firstphase retires113; latercode5phase remains319. tcu-diagnostic-timer.txt:
256init/3072gate/20ISRprefix cases PASS; conditional500000phi period. Next
joinnative diagnosticISR into timeline. Allthreebroader scopes remainopen.
CHECKPOINT owns currentactions/1973annotation Ghidrarestore; olderentriesbelow
arehistorical andmustnotbe used ascurrentprocess/archive status.

CURRENT 2026-10-07: control-preemption.txt closes actualtask4->task7->task4
save/dispatch/resume at an explicit DCBA/selector2 boundary.512saveddispatcher
wholeRAM cases and600outer/601timer retainedcycles PASS;120event2 monitored
fields exactprior,298queue3/120queue2RAMreturns. tcu-capture-clock.txt verifies
512enable/256caller/256prescaler cases andgroundsconditionalTCNT0 Pphi/2.
Oldonce/application capture timestamps areinconsistentwiththat clock; next
mergeactualcaptureedge arrivals into the retainedtimeline. Allthreebroader
scopes remainopen. CHECKPOINT owns Ghidra/currentactions; olderentrieshistorical.

CURRENT 2026-10-07: control-scheduler-start.txt verifies128stockinitializations,
1024modeadmissions,96ADCstartup/192timerportcases. Originaltask17 continuation
stops at unidentified EC62write(A46F6); preservedstrictfixture result.
control-interrupt-nonidle.txt verifies512originalnonidlecontextsave and512direct
restore cases, fullRAM/fullregisters,156byteframes across16stocktasks. Native
schedulerreselection/interleaving/hardwareadmission remainsnext. Allthreebroader
scopes remainopen; CHECKPOINT owns currentarchiveidentity andnextactions.

CURRENT 2026-10-07: control-interrupt-timer.txt completes600originalidleIRQ
entry/return/scheduler cycles,298queue3/120queue2wholeRAMreturns; exactpriorrows
afterexplicitentryR4/PR accounting.576entry/576returngate/24idlehandoff plus
256VBR/256prioritycases PASS. CompatibleCMT1priority9; entryF0/taskstack and
hardwareframe remainfixtures. Startup/interleaving andphysicalDSC/roof
requirements remainopen. CHECKPOINT ownscurrentarchiveidentity andnextactions.

CURRENT 2026-10-07: control-timer-event2.txt completes600originaltimer/scheduler
cycles:600acquisition,150event1/120event2,298actualqueue3wholeRAMchecks;
all120monitoredtractionfields exactpriortrace.3584admission/512CMTconfiguration/
1488queue2producer/186queue2consumer cases PASS. Compatibleperiod20000phi/tick;
absoluteclock/vector/startup/admission remainopen. CHECKPOINT owns allthree
scopes, latestarchiveidentity andnextsteps. Datedentriesbelow arehistorical.

2026-10-07: control-queued-event2.txt completes120queuedpairs/140actualconsumer
RAM checks; allmonitoredfields exactprior120, additionalcallbacks execute.
tcu-application-clock.txt completes320application/1310CMT0/640CMT1/560capture
checks; phaseindex1code5 remains319. No physicaltiming/remotecontroller claim.
Next upstreamECUtimer F28C/1062E andTCUcapture/diagnostic timebases; CHECKPOINT
owns allthree scopes and Ghidra restoration status.

2026-10-07: tcu-clock-ratio.txt completes320 sensitivitypairs/15625CMT1/
32000CMT0/560capture/80hold PASS; oldtiming behavior differs, no vehicleclaim.
control-event2-producer-lead.txt now verifies1536 enqueue/606 consumer cases;
emptyqueueactivation andcallbackdispatch remain next. Artifact SHA identities
in application-clock-event2-artifacts.json; CHECKPOINT owns live application run.

2026-10-07: tcu-application-clock.txt joins original16A58 to retained tasks at
conditional81920phi period, CMT020000/CMT140960. Prefix8 and default-hook
reuse PASS; full320 running (CHECKPOINT owns livehandle). CAN/capture/diagnostic
cadence, common epoch and hardware admission remain explicit limitations.
All three broader scopes remain open.

2026-10-07: tcu-clock-hold.txt:2048 independentwholeRAM gatecases plus
32pairs/8actualreturns PASS; nativeclock/captureloss yields hold of1145 while
historysum is21888. tcu-cmt1-delivery.txt:512init/1024independentISRcases+6
rejections PASS; joined8pairs exactpriorbehavior. Full320 withbothnativeclocks
andactualhold checks isrunning; checkpointowns livehandle andscope limits.
TractionremoteDSC andbothroof operation/recovery gaps remainopen.

2026-10-07: tcu-cmt0-delivery.txt:8000 independent mixed timer-wheel cases
and8 joined pairs/800 nativeCMT0 prefixes PASS. Full320 is stillrunning;
CHECKPOINT owns itsliveprocess andnextverification. Capture320/560prefixes
alreadyPASS. CorrectedGhidra archive independentlyrestored:1929annotations,
984completeexports/11hashes. Allthreebroader goals remainopen; traction/roof
remote-controller andphysical gaps remain distinct.

2026-10-06: tcu-capture-delivery.txt:320 fullpairs/560 originalcaptureISR
prefixes PASS; exactpriortrace afteronlynewobservations/returnPC normalization.
tcu-cmt0-interrupt.txt:512 init/516 prefixcases PASS. Nativeclock admission
adds elapsed/countdownservice; nextjoin preserves theseeffects. Explicitinputs
andcadence, nohardwareclaim. TractionremoteDSC/bothroof gaps remainopen.

2026-10-06: tcu-recovery-cut.txt:320 exactpriorpairs,160cut/160admission
wholeRAM checks PASS. Originaladmissionrecovers290; timers146>=61 keepcut0.
Everyevenpair executescut (cadenceassumptioncorrected). tcu-capture-interrupts.txt:
512differentialRAM A/B ISRprefixcases+6rejections PASS; exactstatus/count/profile
accesses, registerrestoration beforeRTE. Next joinprefixes intosamefulltask.
TractionremoteDSC/bothroof operation/recovery gaps remainopen; nohardwareclaim.

2026-10-06: tcu-recovery-reference.txt:736 nativepairs and512 wholeRAM22DDC
cases PASS. Pendingphase/cache explains3070 fallback; secondexternalapproach
qualifiescode2 at190/retires194,126pairs idle/freeheap. Stopcaptures280 refreshes
zero at284, communicationactivefault clears284, inhibit288, normalinput290.
9454 remains0; next actual24FA0 eligibility/model inunchanged320pair fixture.
4384ISRprefix/184gate/184scale checks; exact160/80/128prefixes. Ghidra saved/
restored1923annotations/978exports/11hashes. Allthreebroader scopes remainopen.

2026-10-06: tcu-receive-recovery.txt:6144ISRcases/768predicatecases and320native
pairs PASS. SevenenabledCANIDs restored64, readiness116; activefaultretainedby
capture-derived80A4. Stoppingcaptures120 givesmeasurement0/reference3070/scaled329
at124; stillnofaultclear/phasecleanup.1728ISRprefix/80gate/40scale wholeRAMchecks,
exact64/120prefixes. Next retainedreference/phaseactivity trace. Allthreeopen.

2026-10-06: tcu-qualified-receive.txt:1280 directdiagnosticadmission wholeRAM
cases;160 native receive/application/diagnostic pairs with480ISRprefix and40gate
wholeRAM checks PASS. Explicitwheel8 releasesreset36; communicationqualifies42,
applicationinhibit44, substitution/cutwithdrawal46. MissingCAN200/240/420/4F1;
healthyrecovery andresidualrequeststate remainopen. No injectedfaultflags or
physicalcadence claim. Allthreebroader scopes remainopen; CHECKPOINT ownsnext.

2026-10-06: tcu-receive-admission.txt:2816wholeRAM originalHCANISRprefixcases
and6expiry/recoverychains PASS.352fulltasks execute nativecopy/admission/dispatch/
watchdog, numeric306 andretirement311;40idle/freeheap.192tickedtasks verify201
expiry/recovery; shortloss leavescomparison/gateheld. Explicitregistersamples,
mode8,preRTEstop/cadence. Next qualifiedcommunicationloss/diagnostic-task join.
Allthreebroader integration/traction/bothroof objectives remainopen.

2026-10-06: tcu-captured-requests.txt: original ECU201/215 encodedinputs +
capturecallbacks +512fullTCUtasks produce naturalnumericrequest306 ->CAN2160209
->originalECUdecoded9. Targetapproach via captureinterval qualifies280, retires311;
200furtheridle tasks, freeheap restored. Independent actualreturn models and
exact256prefixes PASS. Suppliedreceivadmission/cadence; no physicalbus/fullECU
sparkproof. Next actualCAN receiveadmission/freshness. Allthreebroadergoalsopen.

2026-10-06: tcu-initialized-requests.txt: original62groupinit plus full126EC
now creates overlappinggroup7/8 work via natural event1.352 explicittimer/task
pairs retire all sixphase records; finalexpiry320/release321,30furtheridle.
85actualackwholeRAM checks and4132directcases PASS; all915A remainswithdrawn.
Next originalcapture inputs ->fulltask ->CAN216/ECU; allthreebroadergoalsopen.

2026-10-06: tcu-periodic-request.txt:96 complete126EC tasks,48 selected gate
checks and192 existing wholeRAM command boundaries. Four seeded diagnostic
fault/recovery traces execute original cancellation, cleanup and event3 ack;
recovery does not recreate requests. 23BF0 is enable hysteresis, NOT creation.
Uninitialized baseline emits event1 but proves no successful allocation.
Next reuse62 original group initializers in full task; observe natural event1
payloads/acks/overlap. All three broader scopes remain open.

2026-10-06: control-acquired-qualification.txt: all120 queued acquisition/event2
pairs PASS, six wholeRAM39926 decodes and121 activity boundaries. ADC28 low
triggers fallback45; recovery copied64, consumed65, selects1F/20 mode2 at
65/85/105. 3072 direct decoder cases PASS. Supplied cadence/SCI/stack fixtures;
admitted downstream report RAM is not independently verified. FA0A/full3976C
prior leads corrected in report. Next TCU1FD24/23BF0 phase0/4 operational
request lifecycle using126EC harness. All three broader scopes remain open.

2026-10-06: control-task-dispatch.txt:64originaldescriptorprefix/456RTE checks
and7rejections PASS.32queueinit/352enqueue/352consume wholeRAM checksPASS.
Twentyexplicit index7 requests nowdispatchthroughRTE/acquisitiontoyields/idle;
ADC1publishesfloat10atcycle1,ADC28copiesat16 butfull decoder/enableabsent.
Next actualFA0A->E24C->2154C->178C0 full-decoder path; index8 wasfailedlead.
No cadence/interruptproducer/physicalproof; allthree scopesremainopen.

2026-10-06: control-acquisition-retained.txt:40event2 returns/41activity checks
show noADC acquisition/full decoder/phased publication. SeparateE26C reaches
4CE2/6718/1DF32 then3CB8; missingcurrentdescriptor stops3CD4 writeaddress3.
No taskreturn.158ADC interface/6rejection/15schedule-model checksPASS.
Next originalindex7 descriptor/dispatch (3D10/3B8A/3F34); staticleads saved.
Allthree scopes remainopen; no hardwarecadence or controllerproof.

2026-10-06: control-qualification-report.txt:9984 report/cache wholeRAM cases
and131072 mask checks pass. Stock1F/20 masks8000 admit unlike43/44. Initialized
40events pass41 activity boundaries plus10 qualification observations; at5/25
report gate enabled but raw0/enable0 selects no report. Next actual acquisition
freshness with changing explicit ADC samples, preserving downstream limit.
AllTCU/remoteDSC/bothroof requirements remain open; see CHECKPOINT.txt.

2026-10-06: control-initialize-syscr.txt verifiesSYSCR2 access andoriginal
E7B6/F52C helpers (2112checks/14rejections);10022 parentpasses3seededwholeRAM
backup/restore/clear checks. Parent->CA94->1619A->40events passes41activity
boundaries. Next6CFD8 qualificationreporting/same-taskfreshness usingthis
initializedfixture; fullreset/cadence/physical/remoteDSC/bothroof scopesopen.

2026-10-06: control-initialize-dma.txt verifies original100D8 clear of
FFFF4000..FFFFBF9F with8wholeRAMcases andstrictDMA register/gate/fill checks.
WithheldDMA servicekeepsoriginalwait. Clear->CA94->1619A->10events passes
11activityboundaries; zeroedholdcounters nowhaveexecutedlocalprovenance.
Parent10022 stillhitsSYSCR2 F70B read atF534. NextkeyedSYSCR2 fixture and
parentclear/restore proof; fullreset/physical/remoteDSC/bothroof scopesopen.

2026-10-06: control-initialize-timer.txt completesoriginal1619A inexplicit
fixtures after507directcallees.520registerchecks/12rejections,256original80D4
and64original6F29C wholeRAMcases pass. Twozero/seededinitializedruns plus10
outerreturns pass12activityboundaries.9158/915E/915C retaininitialseeds;
8FD4 reloads640. NextearlierRAM/inputsetup before21540->1619A. Fullreset,
physicalintegration,remoteDSC andbothroof scopesremainopen; CHECKPOINT.txt.

2026-10-06: control-initialize-fpu.txt addsboundedlocalFPSCR/zeroFDIV/quietNaN
support:3312instructionchecks,6expectedrejections,8originalselftest wholeRAM
returns55555555. Extended1619A gets95directcallees thenunsupportedF6D8bytewrite
at80F4; fullstartup unproved. Nextsource/testF6D8/F6C4 MMIO, thencounter/
firsttaskfreshness. Allthree broaderscopes remainopen; CHECKPOINT.txt.

2026-10-06: control-flag-bank.txt verifies38 stock calibration flags with64
wholeRAM cases and40 completeoutercalls/66 RAMboundaries.9125=1 islocalROM
publication; periodicconsumer precedespublication. Original1619A prefix also
passesbankreturn, thenstops at intentional-self-test candidate FDIV0/0 beyond
harnesssupport.1024 localSETT checks pass; nofullboot/hardwareclaim.
Next invalid-operation/FPSCR model or directneededcounterinitialization;
allECU/TCU,remoteDSC andbothroof scopes remainopen inCHECKPOINT.txt.

2026-10-06: control-activity-conditions.txt closesstockthreshold/admission
andindependenthold traces:39184directchecks and40outercalls/64fullRAM
boundaries pass.6F2C8 produces8FE0/8FDF;6F34C produces8FD8. Independenthold
readspriormode;lateradmission readsnewmode. Nextexecute744C6 flag-bank/caller
for9125 (staticROMcalibrationsource) andneededcounterinitialization.
Ghidrasaved/restored1894annotations/951exports/11hashes. TCU/remoteDSC and
bothroofdirection scopesremainincomplete; seeCHECKPOINT.txt.

2026-10-06: control-activity-hold.txt verifies9149 producer and640-count
8FD4 timer:17152directchecks,40outercalls/40fullRAMboundaries.9149 reads
priortimer;42BCC consumesnewhold;timerupdateslater.915C addsindependenthold.
Invalidprotected282Cread records534C/5354 butisnotadmittedinthisretained
fixture. Next6F2C8/8FD8 and74ED2/915C producers/freshness. Ghidrasavedand
restored1886annotations/947exports/11hashes. Allthree scopesremainopen;CHECKPOINT.txt.

2026-10-06: control-activity-hooks.txt verifiesoriginalDAE8 edge/state
notifications:25,221 checks plus40completeoutercalls/24mode/flag/edge
boundaries.735B0->1 emitsfirststart,1->0 firstend;907F0 state0 emitssecond
start, testedstate6 completesonlyiffirstpaircaughtup. Otherstatesunmodeled.
Inputhold fallsbut9149=1 keepsactivityflagasserted; nextverify74D62 producer
andactualfreshness. BothGhidraprograms saved/restored:1879annotations,944
exports,11hashes. IndependentTCU/DSC andbothroof scopesremainopen; CHECKPOINT.txt.

2026-10-06: control-outer-event.txt executes original2BCE6 event2 dispatch:
31completecalls verify18282-before-selectedtask,phase0..4cycle,invalidphase
reset andpending652D saturatingdecrement.21freshcases verify16172/1616C
hookcounterwrap;10retainedcalls showhooks onlyonfirstcall. Their admission
condition remainsopen; failed everycall hypothesis ispreserved. LocalPLDR
fixture only; nohardware/clock proof. NextDB32 hookproducer/conditions.
IndependentTCU/remoteDSC andbothroof scopes remainopen; seeCHECKPOINT.txt.

2026-10-06: control-task-stop.txt verifies filtered44A2bit0 ->722A ->735C
and the2C4FC/2C5DE stopconditions:4996directchecks pass. Retainedcomparison
passes48completetasks/49monitorboundaries:zero-input17thcall entersF8D6;
originalCA94/PFDRbit0=1 returns32calls. Explicitfixtures, notrealboot/pinproof.
768GBR/1800MUL.L checks,16original977A2 cases and6widthrejections also pass.
Nextactualouterevent2BCE6 admission/lifecycle/samplingfreshness; independent
TCUoperationalqueue/ack/persistence, remoteDSC andbothroof scopes remainopen.
Ghidrasaved/restored1870annotations/938exports/11hashes; seeCHECKPOINT.txt.

2026-10-06: control-task-serial.txt closesall8 isolatedmode0 taskfixtures:
6212directchecks,35completetasks/90qualificationboundaries pass. Retained
call16 entersoriginalnonreturningF8D6 evenwithadvancingtimer; thiscorrects
priorfrozen-counter-only explanation. Next:2C4FC/2C5DE conditions andactual
startup/peer evidence. SyntheticSCI0samples are notOEMresponses. Independent
TCU/DSC andbothroof requirements remainopen; seeCHECKPOINT.txt.

2026-10-06: control-task.txt extends originalECU18DC8 execution: five mode0
phasefixtures return; phases1/5 reachbothqualifiers buthaltlater atSCI0init;
phase3 needsXTRCT.7424 activitychecks/sixactualboundaries and3736 arithmetic
checks/16expectedaccessrejections pass. Mode1 timerwaitcannotprogresswith
frozenTCNT0. Fullstartup/cadence/freshness andremoteDSC proof remainopen.
Next: boundedXTRCT/SCI0 support andfullqualificationoracles. IndependentTCU
queue/ack/persistence andbothroofdirections retainallgaps inCHECKPOINT.txt.

2026-10-06: tcu-pulse-response.txt verifies53B5C wrapper, response construction,
record handoff and cleanup:3848 directchecks,24 fulltasks/six wrappers pass.
Two buffers alternate; positive44/length1, negative7F/04/error/length3 and
suppressed cleanup remain distinct. Trailing bytes retain outside length.
SAE Mode04 summary supports diagnostic-clear interpretation; this does not
close operational shiftqueue gaps. Nextprimarywork: tractionfulltask ordering.
All three scopes remain open; seeCHECKPOINT.txt for independent nextactions.

2026-10-06: tcu-pulse-request.txt executes54AFC admission,53520 predicate,
5604C permissions and541CC response withoriginalhelpers.5360 directchecks,
48 retainedfulltasks/fiveaccepted-or-rejectedrequests and384 timerwheelcalls
pass. Repeatedacceptedrequestscoalesce; activepulsecanrestart; return0 can
also suppressrejection withoutsetting9418. Nextwrapper53B5C/1D94C andactual
responsepublication/transport. Independenttraction/roof scopes remainopen.

2026-10-06: tcu-pulse-input.txt verifies rawbit17670 and qualified publication
51314:2576 directchecks,80 completeapplicationtasks/20 publicationboundaries,
48 explicitrawreader calls pass. Pulseproducer23DD0 consumespriorA520 before
thisphasepublishes; missingvalidity mayretainvalue. Counter91/92 scenarios
verifydelayededge andcutoff; noactualcadence claim. Request54AFC admission is
next; independenttraction/roof gaps remaininCHECKPOINT.txt.

2026-10-06: tcu-inhibit-writers.txt verifies47C9C latches and23DD0 timed
pulses atactualtaskboundaries:3920directchecks,96tasks/48newwriterboundaries,
512originaltimerwheelcalls pass. Producedmodepulse clearsmainlatch thensource1;
absoluteperiod remainsunproved. Nextrequestadmission/A520 andotherupstream
writers; allthreeindependent researchscopes remainopen inCHECKPOINT.txt.

2026-10-06: tcu-source-inhibit.txt verifiescomplete1F3CE andfivecommand
publication/GPIO/feedback atactualtaskboundaries.2322directchecks,3bounded
missing-key probes,104fulltasks/546boundaries pass. Source1release requires
9415==1 and9C58bit0clear; fivecommands mayrepopulatewhileinhibitstilllatched.
Out-of-nominal-table keysearch verifiedonlyforinjectedinputs; callerreachability
andphysicalidentities open. Separatetraction/roof scopes inCHECKPOINT.txt.

2026-10-06: tcu-application-order.txt executescomplete126EC/1E5F6 with
explicitperipherals.180taskcalls/122periodicbodies;4392directcallee targets,
phase/counter/event4 checks and360 fullcommand/pinboundarychecks pass.
24integratedcycle+96compare bodies useproducedA518/A5A0. Notallnestedsemantics
orboot/timing/hardware proved. Independenttraction/roof gaps inCHECKPOINT.txt.

2026-10-06: tcu-output-pin-switch.txt verifies sourcearbitration529AC,
185F8 pinselection/PFDR control and actual1271A tasktail.5,574checks,4expected
rejections,64retainedtails+6directtransitions pass. A5A0 immediateproducer
nowproved; fullscheduler/parentadmission open. Directnonbinary1->2->0 doesnot
reselectPWM; normalarbitrator emitsbinaryonly.147FE configuresPF14 output;
boardrole unproved. Independenttraction/roof scopes remaininCHECKPOINT.txt.

2026-10-06: tcu-timer-configuration.txt executes nine setup routines and
three original caller slices.176 positive checks,6 expected rejections,
32 cycle+128 compare bodies pass. Compatible manual: channel2/6 clock Pphi/2,
PMDR=0 on-duty non-complementary PWM, PB0..3 select TO6A..D. PBIR untouched;
absolute clock, polarity, delivery and board/plant evidence remain open.
Next TCU:1574C/1576C switching/callers and PBIR/clock writers. Full boot unproved.
Traction and BOTH roof directions retain independent gaps in CHECKPOINT.txt.

2026-10-06: tcu-cycle-callback.txt executes169A4 body,11F7C/124AA and
both ADCconversion/filter/publication chains.3970checks,4 expectedrejections,
80cyclebodies and320comparebodies pass with producedA518 replacingfixture.
Value/status areseparate; realunits/clock/pins/delivery remainopen. Static
configuration leads at144C8/145E4/1496C andboot36F0/3816/383C saved. Allthree
scopes remainopen; seeCHECKPOINT.txt for independenttraction/roof nextactions.

2026-10-06: tcu-output-task.txt executes full127BA/127FC task and1227E
callback through1692E compare-handler body (stops beforeRTE).2538 checks,
7 expected MMIO rejections and160 retained interrupt bodies pass. Activephase
services3,2,1,0; acquisitioneachcall, adaptation/historyonlyphase3. Realclock,
interruptdelivery,169A4 and pinsetup remainopen. Three zerodescriptor slots
readROM400->316, not sensors. Allthree scopes remain open; see CHECKPOINT.

2026-10-06: control-raw-enable.txt executes914B enable writer and first
raw qualification.21,580 checks and320 retained selective-acquisition cycles
pass; produced8EF8/8F30 feed original target/publication and ATspark admission.
Disabled qualification holds counters and does not clear latchedfallback;
inclusive sample recovery clears it. Callcount is not elapsedtime; fulltask
ordering, board identity, remoteDSC and physical integration remain open.
TCU and both roof directions remain separate; see CHECKPOINT.txt.

2026-10-06: control-raw-provenance.txt executes channel28/29 scales and
raw qualification through original caller1B17E..1B190.10,616 component checks
and180 retained ADC-to-target cycles pass. In-range6CAE DOES reset fallback
through6D876, refining the earlier isolated-latch finding. Actual cadence,
914B/8EF8 writers, board identity and remote DSC remain open. Allthree scopes
remain incomplete; roof and TCU next steps are separate in CHECKPOINT.txt.

2026-10-06: roof-revision-source-audit.txt records the AllCarManuals403
access limit and preserves seven D9G4 factory-mirror assets. Original2007
versus later-mirror paused-indicator clearing rows differ; no behavioral
change is inferred. Numeric CAN timeout/reversal/synchronization and receiver
proof remain missing.10 new artifacts pass source-integrity checks. Next
concrete work: traction40E0/40F4 and8F2C..2F provenance, then TCU setup.
Allthree scopes remain open; see CHECKPOINT.txt.

2026-10-06: tcu-output-adaptation.txt executes gain/integral adaptation,
offset lookup, eight-slot dispatch and timer initialization.5680 component
checks,8 expected rejections,3040 dispatcher calls and160 handoffs pass with
19 admitted updates. Timer registers and start bits are sourced separately to
Renesas; physical timing, earlier clock/mode/pin setup and full task cadence
remain open. Allthree scopes remain incomplete. Next concrete work: roof
archive source, preserving both directions and remote-controller gaps.

2026-10-06: control-raw-inputs.txt verifies raw input publication, protected
selection/history, and the sticky8F30 fallback latch. 576/9216/6912 direct
cases, six initializations,2048 latch cases and320 retained CAN4B0-to-target
cycles pass. Isolated latch ignores numeric recovery; upstream recovery now verified above. Sensor identities,
upstream qualifiers and actual cadence remain open.399B0 body was already
executed; its callers remain a lead. TCU configuration/writers and both roof
directions remain independent requirements; see CHECKPOINT.txt.

2026-10-06: roof-component-inspection.txt saves component motor diagrams,
deck-switch continuity and PTC thermal-retest references. Roof/deck connector
layouts differ; componentF-ground conflicts withdiagnosticF-signal. Prior
3O/PIDreferences arecorroborated, notnew;2006training PIDconflictremains.
18newartifacts verified;2007excerpt reproducesbyte-for-byte.2009multiplex
index recovered but actualsection stillmissing. Bothdirections reversal,
timeout,synchronization,recovery andOEMreceiver remainopen. Nexttraction
raw6Dxx/8F30/399B0; TCUconfiguration/writers remainindependent. SeeCHECKPOINT.

2026-10-06: control-acquisition-completion.txt verifies original alternate
ADC arming, A/D1 callback acknowledgement and paired sample capture. Hardware
ADF and software404B marker are distinct.320 retained schedules/7 explicitly
injected callbacks pass; actual delivery/timing/board identity remains open.
Next traction raw6Dxx/8F30/399B0; next roof applicable2009 technical/multiplex
09-02F/G, preserving both directions and interruption/reversal/timeout/sync/
recovery. TCU configuration/writers remain independent. Allthree scopes open.
See CHECKPOINT.txt for current evidence and reproducible artifacts.

2026-10-06: tcu-output-handoff.txt executes TCU correction, retained fallback
recovery, ADC sample accumulation and exact peripheral buffer writes. All
component checks,20 original caller tails and160 retained chains pass.
SH7055S-compatible documentation identifies BFR6A/B/D/C buffers; physical
actuation, configured timing and units remain open. Next traction:4DFE and
completion5E38/5CF4; roof retains its separate2009technical/multiplex lead
and both-direction interruption/reversal/timeout/synchronization/recovery
requirements. SeeCHECKPOINT.txt; allthree scopes incomplete, saved locally.

2026-10-06: roof-wiring-swf.txt saves original2008 factory0916-a/b/c with
readable schematics and reproducibleFFDec export. Sameyear motor3D/3E agrees
with2009wiring; prior diagnosticpin conflicts are notjust modelyearchanges.
Fourlimitcontacts share1V; PIDpolarity/controllerlogic remainunverified.
Bothfolding ANDunfolding interruption/reversal/timeout/synchronization/recovery
andOEMreceiver gaps remainopen. Nextroof2009technical/multiplex09-02F/G;
nextconcreteworkTCU18816/18A44handoff. Tractioncompletion/board/rawinputs and
DSCevidence remainindependent. SeeCHECKPOINT.txt; locallysaved, notcommitted.

2026-10-06: control-acquisition-schedule.txt verifies the complete periodic
ADC manager, selective bank retention and original manager/scaler call pair.
768 copies,3,072 configurations,2,048 managers,32 call pairs,320 retained and
320 paired cycles pass. The prior full-copy fixture does not prove cadence.
Board/units/completion contract and remote DSC evidence remain open. Next
roof applicable0916-a/b andmultiplex09-02F/G technical evidence; folding AND
unfolding reversal/timeout/synchronization/recovery/receiver gaps remain.
TCU18816/18A44 handoff and integration gaps remain independent. No additional
user artifacts; all three goals incomplete. See CHECKPOINT.txt. Saved locally.

2026-10-06: tcu-output-service.txt verifies originalrecordservice and
lookup/rate-limitedpreparation, with160retainedchains and20originalcallpairs.
Busyrecords stillrecomputeoutput; diagnosticflagscanbypassnormalratelimits.
NextTCU18816/18A44handoff remainsunexecuted; noactuator/CANidentityclaim.
NexttractionADCcaller/board work remainsindependent ofTCUprogress, asdo
roofboth-direction reversal/timeouts/synchronization/recovery/receiver gaps.
User hasnoadditionalartifacts. SeeCHECKPOINT.txt; allthreegoalsremainopen.

2026-10-06: tcu-base-publication.txt replaces observed3AC70 dependency
withanindependentmodel andverifies downstream1F2AA/53070 RAMpublication.
Stockslot1 isdisabled; signed16divisor boundarycorrected afterfailedmodel.
320integratedchains/160retainedcalls andcomponent/call-slicecheckspass.
Next530C8 service/rawwriters; thisdoesnotestablishCAN/actuatoridentity.
TractionADCboard/cadence/remoteDSC androofboth-direction reversal,timeout,
synchronization/recovery/receiver evidence remainindependent andincomplete.
SeeCHECKPOINT.txt. Noadditionaluserartifacts; no staging/commit/push.

2026-10-06: roof-2009-wiring-crosscheck.txt saves a visually verified NC
motor-wiring sheet:3C vacant/LHroof3D; RHdeck3M/3E. This narrows earlier
pin contradictions for the2009MY sheet; VIN applicability, motor polarity,
DECK_CL, reversal/timeout/synchronization andOEMreceiver proof remainopen.
Noadditionaluserartifacts. Bothfolding ANDunfolding retain interruption and
recovery scope. NextTCU3AC70/1F2AA; tractionADCboard/caller andDSCevidence
remainindependent. SeeCHECKPOINT.txt; locallysaved, no staging/commit/push.

Latest2026-10-06: control-acquisition.txt traces6CAC/6CB4 tolocal ADC-result
copy/decode/scaling andalternating direct/filtered publication. All1024counts,
260retainedcalls and320pairedcycles pass. OfficialSH7058 hardwarePDF is saved.
Boardwiring/units/actualscheduling andDSCsender/actuation remainopen. Nextroof
technicalrevision/reversal/timeouts/synchronization; TCU andADC leads persist.

Latest2026-10-06: control-mode-followers.txt verifies the post-mode producers,
retained minimum and countdown/expiry distinction:3,556 direct cases,
60 original seven-call slices,240 retained calls and320 paired cycles.
Produced67D0/67D4 replace ongoing fixtures; comparison records two changed
saved output checkpoints. Raw-input identity andactual scheduling remainopen.
Next6CAC/6CB4 source leads; TCU3AC70/1F2AA androof requirements stayactive.

Latest2026-10-06: tcu-class-application.txt follows original consumers into
allocated priority-list entries, selection/override, retained tail and9108
publication. Uniform admission rejects all65,536 counts under stock7713A=0.
The base3AC70 return remains an observed dependency, not an independent
semantic model. Both admission restrictions and conditional evidence are
preserved. Next: traction's five intervening187 bodies; TCU3AC70/1F2AA and
roof technical/receiver requirements remain independently open.

Latest 2026-10-06: tcu-class-adjustments.txt verifies class 0..2 updates,
spreading and consumers: 4,513 direct checks, 96 caller slices, 100 retained
updates and 45 scheduled slices. IMPORTANT: tcu-class-admission.txt then
executes all 65,536 input words, 480 complete callers and 120 retained calls.
Stock admission requires [12800,12800), so full 369A4 never invokes the
updater. Earlier post-admission slices remain conditional fixture evidence.
Next: tcu-class-application-leads.txt, consumer application and the separate
uniform-update stock restriction. All three research scopes remain open.

Latest2026-10-06: control-mode-feedback.txt verifies30202 and31BE6/31C0E:
10,918 direct cases,108 caller segments,450 retained calls,320 paired cycles.
Original mode/selector/timers replace fixtures; refined feedback includesmode10
andfalling-event selector change. Prior sourceJSON remains byte-identical.
Next independentTCU work: tcu-other-stored-setter-leads.txt (static36D1A lead).

Latest 2026-10-06: control-target-source.txt verifies the67E4 producer
30CE4 and helpers33C02/33C2A:1,275 direct cases,36 original caller slices,
80 retained calls and320 paired cycles. Inhibition preserves intermediate
history while forcing66.25 output. StockDB0C1=0 disables the optional final
filter. Prior follower replay remains byte-identical with the new input hook.

Latest2026-10-06: control-target-followers.txt verifies31C36/31662/31D8C:
3,664 direct cases,54 originaleight-call slices,130retained calls and320
pairedcycles. Counterexpiry canretainbothflags; inputproducer30CE4located.
roof-2015-document-crosscheck.txt preserves acomplete official2015PDF and
lateNC pause/resume/P-or-N evidence; reversal/timeout/receiver gaps persist.

Latest 2026-10-06: control-target-adjustment.txt verifies30DBA/30DE2/33BAC
and preceding31E56:4,042 direct cases,36 four-call and36 five-call checks,
40 retained calls, two320-cycle replays. Crucial stock constraint:DB0C0=0
makes31E56 clear6940, disabling the conditional incremental path. Both
conditional andstock-gated results are retained and explicitly separated.

Latest2026-10-06: tcu-adjustment-queue.txt links originalcreation/reset/
phasecompletion/retirement to storedadjustments.144callbackcases,12coupled
traces,2accepted-decrease traces. It also corrects theprevious8consumer
replays:setup hadresetproducedoffsets; correctedorder/inputassertions pass.

Latest2026-10-06: tcu-adjustment-timers.txt connects original timer wheel
to49B08 capture/abort edge observations and310F8 reset callback.
roof-2010-document-crosscheck.txt adds laterNC same-direction pause/resume
corroboration; reverse transition/receiver proof remains missing.

Latest2026-10-06: tcu-adjustment-lifecycle.txt verifies49B08 admission,
event/transition history,capture,peak,abort,completion andoffsetconsumer
connection:8988direct/13retained/8replays. Scheduler/hardware stillopen.

Latest2026-10-06: control-upstream-target.txt verifies30FB6/8BB20 production
of67FC:6081 direct cases,54 original caller checks,32 retained calls and
320cycles/36pairedCAN. Cross-task scheduling remains explicit.

Latest secondary ECU path: control-secondary-path.txt verifies seven bodies,
5681direct cases,72six-call/72twenty-call segments and320integratedcycles.
Descriptor substitution and retained effects are numeric evidence only.

Latest shared-control proof: control-input-gates.txt (11,043direct cases,
72fourteen-call segments,320cycles). New roof version evidence:
roof-training-graphics.txt; DECK_CL polarity differs between documents.

Latest roof evidence: roof-switch-graphics.txt; original graphical switch and
timing tables recovered, PDF saved under sources/. Documentation only.

Latest stored adjustment proof: tcu-stored-adjustments.txt (13,246direct,
18retained traces,24coupled replays). Caller state machine remains open.

Latest optional threshold proof: tcu-optional-thresholds.txt (3283 direct,
72 admission,48 threshold/scan and16 full selection replays).

Latest ECU/AT evidence: tcu-overlay-lifecycle.txt verifies45BA0 history
and27 naturally timed release traces; optional modifiers are now verified above.

Latest limit execution: control-input-limits.txt (2594 direct checks;
24 original caller segments;320 cycles/36 paired CAN updates).

Latest upstream execution: control-normalized-inputs.txt (6266 direct checks;
320 retained cycles/36 paired CAN updates). Full caller and physical identity open.

Latest continuation: see CHECKPOINT.txt. New static upstream leads are in
control-normalized-input-leads.txt; these are not new executed results.

2026-10-06 roof documentation update: roof-fault-recovery.txt records new
primary documentation and remaining receiver/reversal gaps. This advances
only the documentation status; no OEMPRHT firmware or CANcapture added.
Next graphical switch tables andPCMtype/receiver evidence. Folding AND
unfolding andtheir interruption/recovery scopes remain independentlyopen.

2026-10-06: control-normalized-contribution.txt advances traction/shared ECU
8118 production:10034 direct cases,12 originalcaller segments,320 serialcycles,
36 pairedCAN/320CAN211latch updates pass. Seven local producers modeled;
physicalsignal/sender/actuation stillopen. Next684C/6818/6CC8/7020 provenance,
72B4/72BC/gate writers; roofdocs/receiver independent. Allthreegoalsopen.
Ghidra independently restored:1405 annotations/693 exports/11 hashes.
Saved locally; no staging/commit/push.

2026-10-06: tcu-release-thresholds.txt verifies45AA4 active/release overlay:
5531 direct cases,10 retained calls,36 full selection replays. Faultclass6
retainedactive can suppress transition creation; recovery replays unchanged.
Allfourconfiguredthresholdproducers now modeled; upstream/taskorder remain
open. Next independent traction59720/8118 androoftransmissiontype/receiver
leads, then45BA0/815D andoptionalthresholdadjustments. Allthreegoalsopen.
Ghidra independently restored:1386 annotations/686 exports/11 hashes.
Saved locally; no staging/commit/push.

2026-10-06: tcu-retained-thresholds.txt verifies46200 hysteresis/capture,
admission and latched curve replacement:3906 direct cases,11 retained
calls and24 full proposal/selection replays pass. Previous captured inputs
control activation; source6 can publish with no descriptor replacement.
Next45AA4, upstream inputs and task order; then advance independent
traction/roof leads below. Allthree goals active/incomplete. Ghidra
independent restoration verifies1367 annotations/677 exports/11 hashes.
Saved locally; no staging/commit/push.

2026-10-06: tcu-class-thresholds.txt verifies original47240 class overlays
and rising-class operation tags:580 whole-body cases,125 curve builders,
12 retained threshold/scan calls,24 endpoint scans and56 full proposal/
selection replays pass.65535 is not an unconditional upper disable.
Next46200/45AA4 admission, upstream class/source producers and task order;
traction and roof retain distinct status/actions below. Broader60-case
axis-history citation is saved in Ghidra. Independent restoration verifies
1353 annotations,670 identical exports and11 project hashes; archive identity
is in the manifests and latest save block. Saved locally; no staging/commit/push.

2026-10-06: tcu-curve-sources.txt verifies primary threshold-bank priority,
2560 producer cases and2934 interpolation calls. Three saved-state replays
keep bank7404C throughout fault/recovery; four retained calls prove axis
selection precedes bank update (one-call lag). Dynamic copies checked in891
cases. Next model nondefault46200/45AA4/47240 overrides and bank-control
producers;49B08 is a separate, still-static monitor lead. Traction and roof
retain their independent requirements/actions in CHECKPOINT.txt. Saved locally, no staging,
commit or push. Ghidra identity is in the snapshot/restore manifests.

2026-10-06: tcu-threshold-axis-history.txt verifies entry-source axis capture
in4530C:60 calls,600 independent word lookups and60 proposal scans pass.
Leaving source13/14 for0 can change the next call proposal1->4 at fixed
measurement. Explicit upstream fixtures; task cadence remains unproved.
Next natural9C7C/9B40/941E producers and full transition consequences.
Traction/roof retain their separate status/actions below. Focused artifacts
saved locally; no staging/commit/push. Concurrent curve-source work was
detected and resolved by the14:54UTC idle/completed handoff. Broader60-case
Ghidra citation integration is complete with the class-threshold checkpoint.
See session-coordination.txt and session-handoff-reply.txt.

2026-10-06: tcu-fault-selection.txt locates the fault-driven transition
change in809C ->44FCE/9B3E ->4530C thresholds ->4508A.2520 axis cases and32
saved-state counterfactual replays pass;320-call observed fault trace matches
priorJSON exactly, with215 stage events. Restoring809C alone reverses the
proposal/creation in both fault/recovery snapshots. Healthy proposal1 versus
faultproposal4 yields accepted2/code1; recoveryproposal1 yields code6.
Ghidra independently restored:1339 annotations,663 exports,11 project hashes.
Next49B08/configured5DE90 threshold producers and curve/source provenance,
nondefault source admission, task/transport order and overlap/composites.
Traction/roof remain independently required with next steps in CHECKPOINT.txt.
Saved locally; no staging/commit/push.

2026-10-06: tcu-input-faults.txt verifies produced CAN215 group3D and
CAN201 group3C faults through allthree TCU inputs:3364 direct cases and97
diagnostic checkpoints pass.640 new retained cycles/16 active-ring paired
ECU checkpoints compare fault and matched healthy control. Fault qualification
at150 replaces code6 withcode1; recovery211 createscode6, retiring290.
Healthy control retires162; prior320-cycle baseline remains identical.
The duplicate-delivery harness lead is rejected and documented. Ghidra
independently restored:1335 annotations,661 exports,11 project hashes.
Next explain fault-driven reclassification through source/selection flags,
then transport/task order and overlap/composite transitions. Traction and
roof retain independent next steps in CHECKPOINT.txt. Saved locally; no staging/commit/push.

2026-10-06: tcu-paired-input.txt verifies CAN215 byte6 through both original
transition-input producers:18,216 direct cases,640 retained cycles and14
active-ring paired ECU checkpoints pass. Six additional traction bridge
steps connect shared CAN arbitration to CAN215/TCU809A; later local command
overrides can change output while CAN215 remains unchanged. Primary changes
reset815A but do not cancel captured phase retention in these profiles.
Next92D5bit7/group3D fault production, both-input recovery and actual task
order. Allthree research goals remain open; independent traction/roof next
actions remain in CHECKPOINT.txt. Ghidra restored:1327 annotations,661
matching exports and11 project hashes. Saved locally; no staging/commit/push.

2026-10-06: tcu-comparison-input.txt traces ECU CAN201 and receivedCAN4EC
arbitration into the original809C producer.13,888 direct cases,640 retained
cycles and18 new paired ECU checkpoints pass. CAN4EC increase can release a
held CAN215 liveinput duringphase1; sender/transport admission stays open.
Prior320-cycle baseline is unchanged. All three goals remain open, with
independent traction/roof actions preserved in CHECKPOINT.txt.

2026-10-06: tcu-qualification-lifecycle.txt connects selector-produced reset,
original timer increments and retained CAN215 input handling.1,715 direct
cases,960 manager cycles and21 paired ECU snapshots pass. Qualification939E
updates at100, but80F8 holds until163 after phase retirement162. This separates
caller publication lag from phase retention; task timing remains explicit.
All three goals remain open; distinct traction/roof actions in CHECKPOINT.txt.

2026-10-06: tcu-qualification-limit.txt connects ECU CAN215 to produced939E,
transition classification and original selection-before-publication order.
6,860 direct cases and4 paired probes pass. Two limits produce code6/code0;
changed CAN inputs affect939E after selection consumes its preceding value.
Explicit upstream reset/scheduling scope is documented. All three broad goals
remain open; distinct traction/roof next steps remain in CHECKPOINT.txt.

2026-10-06: tcu-transition-progress.txt connects original startup order and
three retained progress accumulators to classification and complete code6/
operation8 replacement.24,785 direct cases,640 retained calls and12 paired
ECU snapshots; spark-request allocation is suppressed by4C880 for operation8.
Older zero-progress traces retain their fixture scope. All three broad goals
remain incomplete, with separate traction/roof actions in CHECKPOINT.txt.

2026-10-06: tcu-transition-classification.txt resolves the proposal2->1/code0
question through original threshold/history/qualification logic.31448 direct
checks,640 retained calls and2 paired creation probes; prior67 paired outputs
unchanged. Produced code6/op8 retiresoldcode1 immediately; laterreplacement
lifecycle remainsopen. CHECKPOINT.txt retains distinct traction/roof actions.

2026-10-06: Latest source selection: tcu-source-selection.txt connects filtered input25
through17D60/22416, original495C0 proposal policy and full44CFE/48C08 to
CAN216/ECU.18736 direct cases,11 input samples,640 manager calls and67 paired
ECU checks pass. Two original phase records retire at110/218 withinputlow,
142/294 withinputhigh. ADC-invalid input retention is distinct from published
status2. Prior map/mode JSON regressions remain byte-identical. Next4508A
proposal/code0 classification, shared971A overlap, remaining source flags and
physical input25 identity/task order. All three research goals remain open.

2026-10-06: Latest phase-mode production: tcu-phase-mode.txt verifies original49260 and
its source/history helpers:9271 direct cases,7 retained hysteresis samples,
384 manager calls,386 mode/191 initial/223 qualifier/82 release checks and
17 paired ECU checkpoints. Produced modes0/1 shift the request start from
call80 to111 and withdrawal96 to112; both retire142. Source inputs and cadence
remain fixtures. Earlier map/release JSON regressions are byte-identical.
Next source9B40/9C91/9BFC/9ACD/9C00 production and full task/overlap/composite/
2->1 behavior. Traction and roof remain separate incomplete goals below.

2026-10-06: Latest ascending phase: tcu-ascending-phase.txt verifies initial-delay neighbor
branches, strict departure andtwo qualification routes:33015 direct cases,
70 retained probe calls,160 manager calls with80 initial/111 qualifier/52 release
oracles and10 paired ECU checks. Shared971A crossing flag canbe consumed by
anotherindex; fullring overlap remainsopen. Next8086 producer (staticstore
candidate492D2), fulloverlap/composite/2->1 and task timing. Allthree goals
remainincomplete; distincttraction/roof steps are preserved.

2026-10-06: Latest ascending predicates: tcu-ascending-predicates.txt verifies release
admission andreactivation:7762 direct cases,384 manager calls,327 predicate
oracles,124 release oracles and25 paired ECU checkpoints. Natural accepted
8081=2 reselects live map768 afterrebound; forced0 retainsrelease1280. Second
release capturesnew768 despitebit40. Both retire154. Prior map/release outputs
remainbyte-identical. Next32614/317E4 ascendingphase/overlap policy and input
provenance. Allthree goals remain incomplete; separate traction/roof steps stay.

2026-10-06: Latest ascending release: tcu-ascending-release.txt verifies4E0EE and its
bounds/capture/ratio helpers:5256 direct cases,12 gate combinations,12 retained
numeric updates,160 manager calls/52 checked release updates and34 paired ECU
checks. Stock release can restore a request after zero; activation9410/92D5
bits are not rechecked inside this callback. Original manager releases1280
through510/260/0, then retires142. Prior map verifier remains byte-identical.
Next4DF3C/4E314/4DDA0,32614 phase qualification and upstream inputs. Allthree
goals remain incomplete; separate traction and roof actions are preserved.

2026-10-06: Latest ascending TCU result: tcu-ascending-map.txt verifies the group7 map,
constructor and bit0 permission path:2908 direct cases,5 produced permission
updates,222 retained manager calls and29 paired ECU checkpoints pass. Original
creation enables9410bit0 from upstream inputs; code1 produces1280 through
CAN216 and changes calculated ECU spark under explicit coefficients. Earlier
zero fixtures had a closed permission gate and zero live map axis. Next4E0EE
release policy,4E314/predicates and upstream map inputs. All three goals remain
incomplete; distinct traction and roof next actions remain below.

2026-10-06: Latest magnitude group: control-magnitude.txt verifies six local producers
plus protected input initialization. 2565 direct checks and320 serialcycles/
36 pairedCAN updates pass. Fast0->1 retrigger reloads12-call holdoff without
newpulse; raw2 canpulse withoutreload. Secondmagnitude canpreservebaseline
withfirstgateoff. 72B4/72BC productionwriter/CANmapping isunproved. Prior
contribution pipeline isnowreusable; defaultJSON regression isbyte-identical.
Next59720->8118,72B4/72BC indirectwriters and67AC/7242/modegate provenance,
fulltask order. Preserve allthreegoals; nonecomplete.

2026-10-06: Latest contributions: control-contributions.txt executes nine original
baseline map/average,7978-gated80DC and independent80E0 correction bodies.
2375 direct/state checks,320 serialcycles,36 paired CAN updates and320
CAN211/latch updates pass. Request withdrawal retains7978/80DC suppression;
explicit admission-count reset restores contribution. Otherphysicalroles and
real timing remainopen. Next80FC/8100 producers593DE/59402 andsource maps,
67AC/7012/7016/A3A4 provenance andcross-task order. Allthree goals incomplete.

2026-10-06: Latest baseline source: control-baseline-source.txt executes six original
809C/8098 target, retention and decay producers. 4997 direct cases and140
serial cycles/22 paired CAN updates pass. Mode bit40/7EEE select distinct
maps; stock scale1 and countdown reload0. Target clear via7346 can retain
809C until the separate decay task. Publication helper resetsA3A4 as a fixture,
not a firmware writer. Next5903C/5904C/59070 baseline contributions,7012/7016/
A3A4 writers and cross-task publication order. All three goals remain incomplete.

2026-10-06: control-input-history.txt executes the full local baseline/history
calculation group 58F10 through58A7A and original protected publication.
1547 direct cases and140 serial cycles/21pairedCAN updates pass. Mode2 can
compute corrected8048 while downstream selector usesbaseline. History lag
can briefly raise the reconstructed input; local caps remain executed.
Next8098/contribution/mode producers and cross-task publication order; all
three goals remain active. Physical traction and OEM roof behavior stay open.

2026-10-06: control-ratio-inputs.txt verifies numerator producers and both
ratio factors, including full lookup/helper side effects. 767 direct cases,
two expected division-by-zero model stops, and 140 serial cycles with 21
paired CAN updates pass. Stock map factor is 1; the other factor uses shared
6DC4/6D40 inputs. Next 58A7A/8048, 80BC and protected input histories,
full task order and nonzero2310 restoration. All three goals remain active;
OEM PRHT receiver/commands and physical traction outputs remain unverified.

2026-10-06: control-history.txt verifies retainedratio/remainder,
hysteresis,countdown/holdoff andprotected2310 decay.1692 directcases and
220 serialcycles/23pairedCAN updates pass. Near-zero numeratorclearsratio;
near-zero denominatorholds it. Timer113 plusrepeating3/2/1/0 holdoff gates
~0.05decay. Cross-tasktiming/nonzero2310 originremainunverified. Nextratio
inputproducers583B8..5855A andrecordrestoration. Allthreegoalscontinue;
OEMPRHT receiver/commands andphysicaltraction outputs remainopen.

2026-10-06: control-sources.txt verifies override lookup input selection,
stock maps/bounds and8248->6D00 normal-command coupling.1028 directcases
and180 serialcycles with21 pairedCAN updates pass; no source/outputinjection
inthenewlifecycle. Absolute ramp canignore8248 changeswhile normalcandidate
stilltracksit. Next8018 producer58280 andretained2310/801C/8028 state,
240xx stage/enable,fulltask/protectedRAM/recovery. Allthreegoalsremainactive;
OEM PRHT receiver/commands andphysicaltraction outputs remainunverified.

2026-10-06: control-overrides.txt verifies original5620/5650/565C numeric
producers and initializers. 2904 direct cases and2578 retained serial cycles
with27 paired CAN updates pass. Relative override captures feedback atcount50
then ramps; absolute override follows source throughtimer63 then ramps,
with exactly0->1 reset atstage>=3. No numericoutput injection innewloops.
Next source8248 writer5C56C/bounds and39D24->6D00 coupling,stage/enable
240xx,fulltask andprotectedRAM/recovery. Allthree goals remainactive;
OEM PRHT receiver/fold-unfold andphysicaltraction outputs remainunverified.

2026-10-06: control-timers.txt verifies original timer/enable producers,
PDDRbit11 output and filtered536C source.1458 timer cases,432 GPIO cases,
1600 filter checks and2514 retained serial cycles pass, plus38 pairedfault/
clear cycles andthree valid-record comparisons. SparseinvalidprotectedRAM
sets5354 andchangesmode1 admission;it isseparatefromserialfault20A8.
Nextfulltask/earlierinputs,numeric5620/5650 andprotectedinitialization.
Allthree goals remainactive throughCHECKPOINT.txt;no commit/push.

2026-10-06: control-admission.txt verifies full24910 override priority and
24C88/24DCE/24E06 local feedback/monitor enables.4991 cases, six retained
checkpoints,126 countdown calls and32 paired TCU/CAN/serial paths pass.
Feedback fault rejects that override; local priority can return to normal
candidate. Fullvehicle reaction remains open. Next earlier timer/input
producers and complete task/recovery order. All three goals remain active.

2026-10-06: control-policy.txt verifies feedback-driven command override and
full missing-feedback admission. 1800 direct cases, 224 SHLL16 vectors,
eight paired checkpoints and 30 serial loss/recovery calls pass. Fault20A8
inhibits its own monitor on the next call; valid replies alone do not restore
counting. Explicit clear plus251 enabled monitor calls sets recovery57CD.
Local enable producers, recovery consumers and physical effects remain open.
All three goals continue through CHECKPOINT.txt; saved locally, no commit/push.

2026-10-06: control-reply.txt verifies application reply acceptance, retained
feedback, request sequencing and missing-feedback fault behavior. 1746 cases,
five paired checkpoints and 28 loss/recovery points pass. Full monitor gate
policy and physical recipient remain open. Continue all three goals through
CHECKPOINT.txt.

2026-10-06: control-serial.txt verifies SCI1 command/reply framing, checksum,
timeout/recovery and actual pairedCAN-to-TDR propagation with sampledMMIO.
Externalrecipient,pins,timing andphysicalactuation remainunproved. Next
applicationreply admission/feedback;allthreegoals continue viaCHECKPOINT.txt.

2026-10-06: throttle-candidate.txt connects sharedCAN calculation to
stock angleconversion,prioritized command and outgoingwordbuffer.1227 direct
cases and6 paired retained checkpoints pass. Saveddefinition supports throttle
labels;transport,physical actuator andOEM roofreceiver remain unproved.
Continue allthree goals via CHECKPOINT.txt.

2026-10-06 update: see control-conversion.txt for verified numeric map
inversion/blending through72FC,324 direct/180 selection/12 paired cases.
Physical actuator identity and upstream A720/history remain open. Preserve
ECU/AT, deep traction and OEM roof fold/unfold including interruption/recovery.
Current continuation and Ghidra archive identity: CHECKPOINT.txt.

Current research scope: ECU/AT CAN integration, deep traction-control logic,
and NC PRHT folding/unfolding CAN integration. All remain incomplete; see
traction-roof.txt for the added goals and their completion criteria, and
CHECKPOINT.txt for current next steps. Repository memory policy is AGENTS.md.

Newest numeric convergence (2026-10-06): numeric-arbitration.txt verifies
four outputs from fullA6490, combining CAN211/21A requests with TCU216/218.
Original producers/decoders feed independent RTZ arithmetic checks; grouped
218 expiry also changes the fresh216 limit. Stock model-map inputs are used
in8 integrated cases. Further histories/physical actuator roles remain open;
allthree goals and concrete next consumers are retained in CHECKPOINT.txt.

Newest traction evidence (2026-10-06): traction-flags.txt verifies CAN211
flags gating CAN21A numeric values and setting retained control latch7978.
Expiry/recovery is executed; flag loss alone does not clear the latch.
1024 paired TCU216/ECU cases show stock calibration disables216bit7's
potential latch input. Physical throttle/fuel roles and CAN21A sender remain
open. Numeric, flag, history and countdown boundary tests, JSON and Ghidra
annotations are saved; allthree goals continue in CHECKPOINT.txt.

Newest cached-source evidence (2026-10-06): tcu-reference-policy.txt verifies
active/cached/stale discrepancy behavior and the distinct alternate source
cache, including fullmode-gated elapsed-counter service. Two capture-driven
control/recovery sequences show reference changes with unchangedCAN216byte4;
72 ECU checks pass. Physical timing and broader TCU/traction/roof requirements
remain open. Independent models, results and Ghidra progress are saved.

Newest reference acquisition (2026-10-06): tcu-reference-source.txt verifies
18-entry capture history, filtering and source selection through full2086C.
Both timestamp paths now drive three complete shifts/35 paired ECU checks,
including nonzero code7 requests, without directly injecting measured or
reference source words. Separate history windows can make80EA and80EC differ.
Physical capture identity/timing and remaining policy/traction/roof work stay
open; reproduction, boundary evidence and Ghidra continuation are saved.

Newest acquisition evidence (2026-10-06): tcu-measurement.txt connects real
timestamp-delta/history/measurement producers to two complete shift lifecycles
and CAN216/ECU. Stale data clears the measurement; recovery needs two fresh
captures and gradually replaces reset history.86 measurement/22 request paired
checks pass.80EC acquisition, physical timing/units, traction and OEM PRHT
requirements remain open. Tests, evidence and Ghidra progress are saved.

Newest source evidence (2026-10-06): tcu-reference-error.txt verifies seven
produced reference words and the clipped two-sample error used for code9 hold
release. Eight lifecycles/73 paired ECU checks use original reference/error
producers, with no direct9218/80D8 injection. Measured inputs, scheduling and
physical units remain open; concrete acquisition leads are saved for next work.

Newest retirement evidence (2026-10-06): tcu-phase-retirement.txt executes
all ten request-group acknowledgements, head/tail removal and idle recovery.
Ten initialized-group lifecycles/64 paired ECU checks pass, including real
ascendinggroup7 and wraparound. Code9's separate80D8 hold explains a difference
from minimal initialization. Original source production and broader goals
remain open; evidence, rotation extension and Ghidra progress are saved.

Newest phase evidence (2026-10-06): tcu-phase-policy.txt connects selector
acceptance, actual timer advancement and descending phase qualification to
CAN216 reduction, ECU spark and request release. Three lifecycles/22 paired
checks pass. Phase completion differs from ring retirement; remaining groups,
source identities and physical timing continue in CHECKPOINT.txt alongside
traction and OEM roof goals. Ghidra predicates/tables and snapshot refreshed.

Newest selection/creation evidence (2026-10-06): selection-creation.txt joins
accepted-state publication to actual group8 phase/request creation. Six
CAN231/ECU and12 CAN216/ECU checks pass. Admission can allocate a request
while phase activation and returned reduction remain absent. The bounded
operation0 result and unfinished classifier/phase leads are saved together.

Newest upstream-admission evidence (2026-10-06): tcu-request-admission.txt
executes original event1 creation, captured map inputs, enable hysteresis and
fault-source cancellation. Nine lifecycles/45 paired ECU checks pass. Gate
suppression retains requests; cancellation releases them. Physical timing,
remaining source roles and allthree research goals continue in CHECKPOINT.txt.

Newest timer evidence (2026-10-06): tcu-request-timing.txt verifies original
hold/ramp timer advancement and periodic request service. Twelve complete
lifecycles use original timer code; service delay changes release observation.
Call ratios are proved, physical durations remain open. Allthree goals and
next steps remain in CHECKPOINT.txt; reproducible script/JSON saved alongside.

Newest managed-request evidence (2026-10-06): tcu-request-dispatch.txt verifies
original event/heap lifecycle through request states, completion/cancellation,
CAN216 and ECU spark.28 paired paths and8 abort lifecycles pass. Produced
calibration indices are0..4; prior15-index probes were synthetic. Full timing,
physical source roles and allthree broader goals continue via CHECKPOINT.txt.

Newest TCU map/ramp evidence (2026-10-06): tcu-request-maps.txt executes
constructor snapshots, stock calibration requests and timer decay through
CAN216 to ECU spark alongside CAN211 traction. Boundary tests and12 paired
lifecycle paths pass. Stock offset curves arezero; full dispatch, input units
and scheduler remain open. Allthree research goals continue in CHECKPOINT.txt.

Newest TCU request evidence (2026-10-06): tcu-slot2.txt executes initialized
12-entry/3-entry candidate lists,mode-sensitive merge and record2 through
CAN216 to ECU spark.841 merge cases,600 queue operations and60 paired paths
pass. Sentinel asymmetry and allocation failure bookkeeping are preserved.
Physical policy entry and remaining phase logic stay open in CHECKPOINT.txt.

Newest local-input fault evidence (2026-10-06): local-input-faults.txt proves
P0704/P0850 group mapping, event-count diagnostics and serial-to-MT231 fault
and recovery behavior. Stock AT dispatch masks block these reports beyond
the internal cache, despite enabled DTC bytes. Tests pass; source units,
physical timing and OEM PRHT reception remain open. Full scope in CHECKPOINT.

Newest local-input evidence (2026-10-06): local-inputs.txt verifies serial
bank acquisition and two-sample filtering through MT CAN231. Input44A4 is
not direct GPIO.2048 serial,1024 initialization,256 filter and9 stateful
CAN publication cases pass. Diagnostic producer leads are saved as static;
physical switches, scheduler and OEM roof reception remain unresolved.

Newest MT/AT ownership evidence (2026-10-06): mt-can231.txt verifies the
ECU's distinct MT231 payload and local neutral-candidate flag, alongside
actual TCU selector production. Configuration-disabled transmission can
publish retained fields. Full source/pack/admission and paired tests pass;
PRHT reception and transmission-type semantics remain unproved.

Newest roof evidence (2026-10-06): roof-aftermarket.txt preserves a public
NC converter image and65536 executed selector/gear cases. Its menu labels
CAN231 codes1/3 Park/Neutral, independently corroborating the ECU/TCU pair.
OEM PRHT reception remains unproved; the public converter release predates
its announced roof update. Exact inputs, sources, limits and next steps are
saved in that record and CHECKPOINT.txt. All three goals remain active.

Newest output-scheduler evidence (2026-10-06): output-inhibition.txt connects
CAN211 patterns and actual TCU CAN216 production through the full ECU caller
to timer-register writes. Request caching, deferred inhibition and release
boundaries are verified. Hardware pin routing, timer timing and normal full
record lifecycles remain open; all three goals continue in CHECKPOINT.txt.

Newest traction pattern evidence (2026-10-06): traction-pattern.txt executes
CAN211 conversion through stock model thresholds, hysteresis, rotating event
masks and shared cylinder inhibition.120 integrated paths and1280 stateful
events pass alongside exhaustive pattern sampling. Hardware outputs, DSC
sender identity and real scheduling remain open; full scope in CHECKPOINT.txt.

Newest stock model evidence (2026-10-06): model-sources.txt traces real ECU
coefficient/offset maps and the pattern-count producer through CAN215, TCU
request handling and same-ECU CAN211/216 spark. All198 feedback cases use
stock model sources; sensor/state inputs and scheduler remain fixtures.
Full evidence, tests, limits and continuation are in CHECKPOINT.txt.

Newest shared CAN215 fault policy (2026-10-06): can215-invalid.txt executes
invalid qualification, two-field substitution and healthy recovery through
CAN216 into ECU spark. It also corrects3A/3B/3C recovery to500 ticks plus
the next producer pass; old sparse samples did not prove5000. Updated tests
and results pass. Full scope and next steps remain in CHECKPOINT.txt.

Newest CAN215 feedback (2026-10-06): can215-feedback.txt verifies ECU
publication through TCU conversion, diagnostic selection and CAN216 return
to the same ECU spark model alongside CAN211. Invalid data can hold the
previous value before fault substitution. Full findings, reproducible tests
and remaining traction/roof objectives are indexed in CHECKPOINT.txt.

Newest TCU request trace (2026-10-06): tcu-spark-requests.txt executes
record aggregation and phase3 ramp through CAN216 to ECU spark. Stock
records1/2 use ordered priority, not min/max. CAN215 is an upstream static
lead for the base input; full scope and continuation remain in CHECKPOINT.txt.

Newest simultaneous spark trace (2026-10-06): spark-interaction.txt connects
TCU CAN216word0 to per-cylinder spark and verifies additive interaction with
CAN211, plus concurrent cylinder cuts. Tests and limits are recorded beside
the findings; all three research objectives remain active.

Newest transition gate (2026-10-06): transition-gate.txt identifies and
executes the9545mask04 producer2D1BC, fullcaller2C7B0 and CAN231/ECU path.
Tests cover gate truth/preservation, source writers and release lifecycle.
Physical mode meanings and scheduler conditions remain unproved; traction
and PRHT goals remain active. See CHECKPOINT.txt for continuation.

LFFEEE ECU / LFG1TF000 TCU CAN investigation

Newest reporting trace (2026-10-06): selection-reporting.txt distinguishes
requested8084, admittedcandidate9C85, next8085 andpublished8081. Complete
TCUupdates throughCAN231 intoECUflags areverified, withdelay/acceptanceholds.
Physicalgear attainment andwall-clocktiming remainunproved.

Newest selection follow-up (2026-10-06): selection-pipeline.txt corrects the
activation interpretation: the default-input update clears the enabling flag.
The complete3-stage caller is executed; conditional effect persists, but
normal activation and final physicalgear effect remainunproved.

Newest continuation (2026-10-06): can201-byte6.txt and its verification JSON
record ECU publication, TCU scaling/change history, group3C recovery and an
executed downstream selection rule. Group3D also triggers byte6 fallback.
Physical source/units and selection role remain unproved; traction and PRHT
requirements remain open. See CHECKPOINT.txt for the next concrete work.
Evidence checkpoint: 2026-10-05

Latest invalid-data policy: can201-invalid.txt / verify_can201_invalid.py
execute ECU6B4F ->CAN201FFFF ->TCUgroup3A qualification ->substitution/cut
inhibit ->ECU commands.2048 producer cases,25 helper cases,six base andtwo
interrupted-recovery lifecycles pass, plus qualification/dependency/global
gates andseven complete round-trip checkpoints. Holds old value for500 ticks;
then substitutes20480. Recovery needs500 healthy ticks plus the next producer pass with80A4=0.
Internal history persists without the tested DTC/CAN report outputs. This
closes the three-source provenance ofA98E; overall objectives remain open.
Next21628/CAN201byte6 andgroup3C, CAN211 traction arbitration, PRHT CAN
speed/neutral attribution. Physical timing and remote internals stay unproved.

Previous controller recovery: hcan-recovery.txt / verify_hcan_recovery.py
execute the bus-off handler body, reset/retry states, group35 diagnostic and
CAN201/cut policy.1024 helper,128 handler,240 deadline/retry,8 acknowledgement,
1024 producer,16 monitor-gate cases and47 lifecycle checkpoints pass. At10
retries the inhibit asserts; healthy recovery preserves storedC073. Local
controller recovery suppresses groups36/37/38 missing-message producers.
New static lead583DC/table5F198 mapsCAN201validity8816 togroup3A; execute
its timed qualification/recovery next. Then21628 byte6 consumer, CAN211
traction arbitration and PRHT speed/neutral attribution. All three objectives remain
active; explicit register fixtures do not establish electrical/physical timing.

Previous diagnostic policy: can201-fault-policy.txt records the verified chain
from groups35/36/3A through57258/A98E to CAN201 substitution and cut inhibit.
146 mapping cases,512 paired summary cases and14 CAN loss/recovery lifecycles
pass. Loss of any enabled class0 frame can inhibit the request even while201
arrives; stored history alone does not. Group36 recovery requires more than
5000 healthy ticks and80A4=0. Physical causes of35/3A and tick units remain
open. Next: their producers, CAN211 traction arbitration and PRHT CAN speed/
neutral attribution. All three requirements remain active and incomplete.
See the authoritative record for fixtures, failed leads and reproduction.

Previous interpolation evidence: software-lookup.txt / verify_software_lookup.py
execute all65536 input values of stock cut-threshold curve703C0 against an
independent integer formula.1115 ISA tests cover the separate rotate/swap/
CLRT extension. Updated round-trip verifier passes800 mixed control cases,
30 axis-producer/paired cases and the prior84 numeric/512 mapping/11 lifecycle
cases.9334 derives from89A8 via22ECC with diagnostic fallback and word wrap.
Next upstream acquisition17D9C, A98E diagnostic provenance, timer scheduling
and201byte6 consumer21628. Physical units, traction and roof internals remain
unresolved; all three requirements stay active. Prior/current turns progress.

Previous CAN201 round trip: can201-cut-loop.txt / verify_can201_cut_loop.py
execute ECU6DB4 ->201word0 ->TCU8814/80E8 ->9454 ->216bit5 ->ECU cylinder
commands.84 numeric,512 diagnostic mapping,800 control/paired cases and11
stateful TCU steps pass. Hysteresis and invalid-held versus substituted data
are distinct. Lookup endpoints execute; five interior cases fail closed on
unsupported rotates in software-double helpers. Next extend lookup arithmetic,
traceA98E fault provenance and timing gates; physical units remain unproved.
All ECU/TCU, traction and PRHT requirements remain active/incomplete.

Roof follow-up: traction-roof.txt [J-L] now records the factory2008 opening/
closing sequence, button-release pause/resume, manual latch completion and
left/right pulse-mismatch diagnostics. The sequence is documented rather
than firmware-executed; CAN IDs, reversal and timeout transitions stay open.

Latest speed-fault evidence: speed-fault.txt / verify_speed_fault.py execute
capture counters ->group13/code0722 ->92C6bit2 ->CAN216FFFF ->ECU201FFFF,
even with healthy alternate4B0 inputs.6001 handler calls,512 one-hot mapping,
384 helper combinations,20 gate rejections and48 recovery cases pass.
Active recovery restores transmission and resets limiting while retaining
stored0722. No physical timing or PRHT receiver is established. Next prioritize
PRHT speed-invalid/neutral attribution and CAN211 traction arbitration;
TCU global monitor gate58768 and201 downstream consumers remain open.
All three objectives remain active/incomplete. No ROM/application changes.

Previous TCU speed evidence: tcu-speed.txt / verify_tcu_speed.py execute
52B10 source math ->18F8C limiter/fault modes ->216 ->ECU201.936 limiter
cases,140 upstream cases and10 lifecycle steps pass, with byte4 division
now executed. New integer extension passes1200 ISA and66153 division cases.
verify_tcu_can201.py passes432 copy cases and1225 audited full callbacks:
only bytes0/1/6 read there; no global claim about speed bytes4/5 non-use.
Next:92C6 bit2 fault producer, mode callers,A552/capture provenance, and
TCU downstream consumers. Physical units and PRHT receiver remain open;
all original ECU/TCU, traction and roof objectives remain active/incomplete.
Previous goal turn and this turn both made concrete evidence progress.

Previous speed evidence: can201-speed.txt / verify_can201_speed.py execute
CAN4B0 selection/average -> CAN201 bytes4-5, with CAN216 bytes5-6 providing
the AT fallback and independent invalidity gate.1600 paths,66 encoder bounds,
96 paired TCU216 cases and4 pack modes pass. Separate bounded RTZ harness
passes581 rational,306 arithmetic,732 FMAC cases and8 expected rejections.
Physical units, DSC ownership, TCU201 consumption and PRHT receiver remain
unproven. Next: TCU216 word5 producer,201 receive audit,7353/freshness gates.
All three full research objectives remain active; no ROM/application changes.

Previous threshold evidence: selector-threshold.txt / verify_selector_threshold.py
trace the threshold to a local timer-capture path (static upstream), execute
all65536 application scaling inputs,256 capture-configuration fixtures and
18 paired TCU->ECU threshold cases. Exact raw threshold932E>=7680. Physical
sensor/units and full upstream arithmetic remain unverified; strict harness
stops at22DFE MULS.W and5AF4C DIV0U are recorded, not mocked.
Next: sensor/pulse scaling and group13 producer; separately trace PCM speed
for PRHT. All original ECU/TCU, traction and roof objectives remain active.

Previous recovery evidence: selector-recovery.txt / verify_selector_recovery.py
execute30000 full timer-service calls,64 paired selector recovery cases and
history/dependency gates. Active0708 can force231 invalid while its confirmed
report remains absent. Recovery requires a specific input combination. Real
clock units, physical input names and roof consumption remain unproven.

Previous diagnostic evidence: selector-faults.txt / verify_selector_faults.py
execute group15 qualification, stored0707, mapped92CD flags and CAN231
through ECU state decoding.384 producer cases,7 countdown vectors,18 timer
boundaries and9 paired lifecycle steps pass. Recovery and full group16
qualification remain open.

Previous selector evidence: selector-inputs.txt / verify_selector.py execute
sampled TCU inputs through filtering, CAN231 and the ECU combined flag723A.
256 input transitions plus ADC/fault/override cases pass. CAN codes1 and3
are combined by both modules, supporting a P/N hypothesis; physical wiring,
P versus N identity and PRHT consumption are still unresolved.
See tcu-can211.txt for the prior bounded receipt-monitoring result.

RESULT AND SCOPE

LFFEEE-stock.bin contains AT engine-ECU logic and an AT calibration. This is
supported by executable configuration branches, six AT ratios, actual CAN
receive handlers, and matching message packers in LFG1TF000.bin. It is not
merely an inference from a filename or a transmission-controller definition.

The earlier LF9VEB image is configured as MT, although its executable has
shared AT/MT branches. Changing its mode byte alone has NOT been established
as a working AT conversion. LFFEEE and LFG1TF000 are not proven to be an OEM
matched software pair; matching message layouts establish protocol overlap,
not complete vehicle compatibility.

This checkpoint establishes message ownership, buffers, byte order, several
normalization formulas, state decoding, and some downstream consumers. The
paired execution now also reaches per-cylinder command zeroing from TCU216
bit5; see ACTUATION EVIDENCE below for its boundaries and stale-frame result.
The physical meaning of several fields and the complete engine-actuation and
fault-recovery chains remain open. Do not treat the field descriptions here
as a complete DBC or a validated CAN emulator.

ADDITIONAL ACTIVE GOALS

The user also requires deep traction-control logic/integration and NC PRHT
folding/unfolding CAN integration. See traction-roof.txt for completion
criteria, original-code CAN211 findings, factory source links and open issues.
verify_network.py / network-verification.json preserve executable211 and
receipt-fault checks. freshness.txt and verify_freshness.py now extend this
to TCU record deadlines/fault bits and ECU inhibition/recovery gates. These
are ongoing goals, not completed interfaces. diagnostics.txt and
verify_diagnostics.py extend the TCU work to two qualification timers,
stock211 qualification exclusions and the ECU9710 configuration-read path.
fault-reporting.txt / verify_fault_reporting.py now trace class0 qualification
to stored diagnosticC100, CAN216 bit1, ECU6E53/24EE, and5000-tick active recovery.
Stored report/bit1 persist in that tested recovery; mechanical fallback is open.
warning-status.txt extends this to PID01 MIL status, ECU CAN420 byte5 bit6
and active TCU CAN231 byte1 bit6; startup/override gates are executed.
can211-spark.txt / verify_can211_spark.py now execute CAN211 word0 through
model inversion, correction/arbitration and all four cylinder spark values.
Twenty synthetic examples and component/gate tests pass; sender, wire units
and ignition timer hardware are not established.
Roof workshop sources now establish MT-neutral/AT-P-N interlocks and a
direct window handshake, with explicit unresolved connector inconsistencies.

FILES AND PROVENANCE

Persistent Ghidra work is in ghidra/live/nc-at-can.gpr (with its .rep directory).
The Git-eligible ghidra/nc-at-can.tar.gz checkpoint preserves both programs,
analysis and 330 verified annotations. See ghidra/README.txt for restore and
refresh instructions, and CHECKPOINT.txt for the latest static follow-up leads.
Function exports and reproducible annotation scripts are saved alongside it.
The repository-wide memory policy is in ../../AGENTS.md and ../../CLAUDE.md;
CHECKPOINT.txt holds continuation state. ecu-import-review.txt retains the
earlier ECU-only calibration/DFCO/diagnostic investigation as historical work.
sources/ preserves the exact Romdrop XML and CRC downloads with URL/hash
provenance. Run verify_import.py to reproduce import-verification.json.

ECU: ../../examples/LFFEEE-stock.bin
  1,048,576 bytes; internal ID LFFEEE at file offset 0xB8046.
  SHA256 7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08
  Copied unchanged from:
  C:\Users\snow\Downloads\SW-LFFEEE000.HEX\SW-LFFEEE000.HEX.bin
  The supplied Windows path is a directory. Its payload is a raw binary,
  not an Intel HEX text file. No conversion, patch, or checksum repair was
  applied. All 35 ECU checksum records pass. Normalized calibration CRC32
  0x4F465365 matches the romdrop factory database.

TCU: ../../examples/LFG1TF000.bin (already present in the repository)
  524,288 bytes; SW-LFG1TF000.HEX string at 0x10612.
  SHA256 8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6
  Local XML describes a 2006 6AT SJ6A-EL. Its SH7058 CPU label conflicts
  with the executable's register map. HCAN at FFFFE400 matches the SH7055
  family, including the byte order of ID registers. Application GBR is
  FFFF8000 (set at 0x10414 using the constant at 0x76C84). Exact chip
  variant remains unconfirmed. ECU checksum routines were not applied.

MT comparison: ../../examples/lf9veb.bin
  SHA256 bfd0965a0f51f60a951d8cd3ef8fe77e5a37fbc326ddb723edf0ede4b1640fbf
  All 35 checksum records pass; factory normalized CRC32 0x00808CC3.

Addresses below are hexadecimal. ROM addresses are offsets into their
respective unmodified files. RAM addresses retain the FFFF prefix. All
payload byte numbers are zero-based; payload words are big-endian.

CONFIGURATION EVIDENCE

                           LFFEEE AT         LF9VEB MT
  Selector address         B8296             B858E
  Selector value           0                 1
  Selector reader          429E8             39380
  Initialization           42728             390C0
  Mode flags RAM           FFFF734A          FFFF6C76
  Final drive address      C1200             C14F8
  Final drive              4.10              4.10
  Ratios 1..6              3.538, 2.060,      3.815, 2.260,
                           1.404, 1.000,      1.640, 1.177,
                           0.713, 0.582       1.000, 0.787

The selector is used unless it is FF, which invokes a RAM/configuration
fallback. Initialization produces flags 80 for selector 0, 40 for selector
1, and A0 for selector 3. The receive paths below require bit 40 CLEAR and
the separate byte at FFFF734C equal to 1. Initialization at4288C derives it
from B8297==1 (stock1) via protected setter154C0. Its physical option name
remains unconfirmed; do not call it a health flag without evidence.

The presence of the ratio constants does not establish that the AT branch
uses that table. ECU 3F600 uses the calibrated ratios when bit 40 is set;
with that bit clear it multiplies FFFF6A38 and FFFF6A3C instead. Only their
initialization to 1 has been found so far. Their runtime origin is unresolved.

CAN OWNERSHIP AND TRANSPORT

The ECU has 16-byte descriptors: +0 u32 ID, +4 direction (0 TX, 1 RX),
+5 mailbox, +6 DLC, +8 RAM buffer, +12 option. Mailbox numbers >=20 select
the second CAN channel. verification.json contains the extracted records.

ID    Sender in active AT configuration    ECU descriptor    ECU buffer
200   ECU                                 378CC             FFFF6B14
201   ECU                                 378DC             FFFF6B2C
215   ECU                                 378FC             FFFF6B50
216   TCU                                 3790C             FFFF6A40
218   TCU                                 3791C             FFFF6A68
231   TCU                                 3794C             FFFF6ABC
240   ECU                                 379CC             FFFF6B70
420   ECU                                 379DC             FFFF6B80
4C1   TCU                                 37A0C             FFFF6B0C
4EC   ECU                                 37A1C             FFFF6B94
4F1   ECU                                 37A3C             FFFF6BBC

ECU 6906 checks receive status, copies a fresh mailbox to the descriptor
buffer via 10AA0, and returns zero on success. The AT receive handlers are
34C1E (216), 35156 (218), and 3579C (231). Dispatch begins at 34416.

TCU TX driver 1B26C selects a descriptor by r5 and a mailbox by r4. Its
ID table at 5C864 stores the HCAN register representation:

index  ROM bytes  CAN ID  DLC at 5C86E  buffer table at 5C874
0      20 FD      7E9     8             FFFF8EE4
1      20 98      4C1     1             FFFF8EEC
2      20 46      231     8             FFFF8EED
3      00 43      218     8             FFFF8EF5
4      C0 42      216     8             FFFF8EFD

Decode these two ID bytes as little-endian, then shift right 5. This is
HCAN register byte order; it does not make the CPU or payload little-endian.
The driver writes the mailbox ID (1B28A), copies payload bytes, and sets
TXPR (1B376). Its application TX set contains no 21A. The ECU receives
21A, but assigning that frame to this TCU would be incorrect.

TCU RX filters at 5C8C0, remap at 5C8D8, copied lengths at 5C8E4, buffers
at 5C8F0; driver 1B630 onward checks DLC and dispatches copies/callbacks:

ID    TCU buffer  Copied bytes
200   FFFF8F40    7
201   FFFF8F39    7
211   FFFF8F34    5
215   FFFF8F2C    8
240   FFFF8F24    8
420   FFFF8F23    1
430   FFFF8F1C    7
4B0   FFFF8F14    8
4EC   FFFF8F0D    7
4F1   FFFF8F05    8
7DF   callback 1DB10
7E1   callback 1CB3A

Copied byte counts are receiver requirements, not necessarily wire DLC.
211, 430 and 4B0 also appear as ECU receivers; they are not ECU transmitters
just because both controllers have those IDs in their tables.

231 OWNERSHIP SWITCH

The ECU also has TX descriptor 3793C for 231. Function 36D52 increments
a u16 counter and considers transmission when the result is at least25.
Initializer36D40 seedsFFFE and falls through, allowing an immediate initial
attempt;25 calls apply after clearing the counter. At 36D6A..36D92 it
transmits only when FFFF734A bit 40 is SET or FFFF734C is ZERO. Active AT
reception instead requires bit 40 clear and FFFF734C == 1. Thus descriptor
presence alone does not imply simultaneous ECU/TCU ownership. 36DB0 uses
the same TX gate when packing bytes 0..3, and zeros bytes 4..7. The distinct
MT field builders and retained-field edge cases are now executed in
mt-can231.txt; PRHT reception and transmission-type semantics remain open.

218: TCU APPLICATION THROUGH ECU DECODER

Payload    TCU setter        ECU raw destination (unpacker 35420)
0..1       1C448             FFFF6A92 u16
2          1C476             FFFF6A96 u8
3          flag setters     FFFF6A97 u8
4..5       1C51C             FFFF6A94 u16
6          1C54C             FFFF6A98 u8
7          flag setters     FFFF6A99 u8

TCU sender 191F0 has default (argument 0), normal (1), and invalid (16)
branches. In its normal branch, bytes 0..1 are:
  v = signed16[FFFF941C]
  raw = clamp(2 * (2000 - v), 0, 8000)
unless FFFF916D bit 1 is set, in which case raw is FFFF.
ECU normalization at 35218 onward converts valid raw to
  float[FFFF6A70] = raw * approximately 0.05 - 200
and uses zero for FFFF or fault byte FFFF69E2 == 1. For unsaturated normal
TCU values, the combined result is approximately -v/10.

TCU byte 2 normally equals (signed16[FFFF80F2] >> 7) + 50; fault bit 7 of
FFFF92C6 selects FF. ECU produces float[FFFF6A74] = byte2 - 50. This
resembles a temperature representation but physical meaning is unconfirmed.

Byte 3 bit 7 is zero only when FFFF8080 == 6, FFFF92CA bit 7 is clear,
and FFFFA5B8 != 1; otherwise it is one. Other flags need semantic names.
Bytes 4..5 are FFFF in all three branches of this stock sender. The ECU
supports a numeric value in float[FFFF6A78], using 65537.0 as its invalid
sentinel. Thus a decoder can support a field that this sender leaves invalid.

TCU 191A8 separately prepares byte 6 from signed16[FFFF9118]:
  raw = clamp((source >> 6) + 50, 0, 254), or FF for source 7FFF.
ECU converts valid byte 6 to min(2*raw - 100, cal[B8274] = 50), stored
at FFFF6A80. Invalid/fault/MT conditions select -10000.0.

Machine-code examples from synthetic RAM (byte 6 was initially zero):
  sender arg 0:  0F A0 46 00 FF FF 00 00
  sender arg 1:  0E B0 46 00 FF FF 00 00
                 with 941C=120, 80F2=20*128, 8080=6
                 first field decodes to approximately -12
  sender arg 16: FF FF FF 80 FF FF 00 00
These are test vectors, not captured bus traffic.

Downstream: 2EF94 averages eight samples of FFFF6A70 at FFFF66C4..66E0
into FFFF66E4. 2E590 clamps this relative to B873C=0, with bounds
B8740=-15 and B8744=+15. It then uses a rate parameter B8748=1 and filter
parameter B874C=0.9; B86D9 permits a newest-sample bypass. FFFF66F0 feeds
2E630, which adds state-selected calibration corrections into FFFF66F4.
2E72A onward derives threshold/state arrays from it. This is real ECU
consumption, but does not yet prove that this field is a spark-retard demand.
FFFF671C is a separate filtered signal sourced from FFFF6D58; it must not
be conflated with FFFF66F4 just because both occur in the same functions.
Byte 2's float reaches 3E9E2 / FFFF703C / 2C190. Bytes 4..5 reach 5BD28
and 5BD3A; byte 6 reaches A6930. Final actuator attribution remains open.

216: VALUE REQUESTS AND STATUS

Payload    TCU setter        ECU raw destination (unpacker 35034)
0..1       1C5CA             FFFF6A48 u16
2..3       1C624             FFFF6A4C u16
4          1C654             FFFF6A58 u8
5..6       1C666             FFFF6A50 u16
7          flag setters     FFFF6A5A u8

TCU sender 18F10 uses signed16[FFFF915A] and signed16[FFFF80BC] for the
first two words: (source >> 5) + 512, lower bounded by zero; source 7FFF
selects FFFE in normal mode. Mode 0 also sends FFFE; mode 16 sends FFFF.
This corrects the first checkpoint's source-address and sentinel transcription.
Seven full producer cases now execute those distinctions, including negative
values and a decoy at FFFF80BA. ECU 34CEC copies accepted raw fields into working storage.
The first word normalizes to raw - 512 at FFFF6A34; invalid FFFF, network
fault 69E2==1, or MT mode select 65537.0. 3B584 passes it into FFFF6E04
unless local conditions choose another value. 3B5FE subtracts that value
from a larger control calculation. This is a candidate torque-request
path, with physical units still requiring independent confirmation.

The second word is retained at FFFF6A54 when the receive counter is live;
the counter-expired path writes FFFF there, FF at FFFF6A5C, and FFFF at
FFFF6A56. 34EB8 onward applies additional invalidity/gear checks and
calibration-dependent recovery before producing FFFF6A30. A6B04 takes a
minimum against this value and stores the resulting calculation at
FFFFA70C. Exact final throttle/load/torque attribution remains open.

ACTUATION EVIDENCE: TCU216 BIT5 TO PER-CYLINDER COMMAND ZEROING

This chain is executed from original function entry points by
verify_actuation.py, with complete original bodies and no mocked helpers:

  TCU FFFF9454 ->18F8C ->216 byte7 bit5
    -> ECU35034/34CEC ->FFFF6A61
    ->3B4D4 ->FFFF6E62
    ->3AD04 ->FFFF6E2C/2D, countdowns6E28/29
    ->3AC14 ->FFFF6E35..38 (cylinder indices1..4)
    ->4D716 ->FFFF78D0..D3 bit80
    ->44E50 ->zero at FFFF740C/7410/7414/7418.

3AD04 requires6530=1,6531=0,6567=1,checked700E=1,6E2E=0,65F0=1.
B81AC/AD enable the two pairs (stock bothFF). Rising edges load100 from
B81AE/AF; a held request decrements on subsequent calls, reaches zero on
call100 and does not reload until released/reasserted. No millisecond
interpretation is established. 3AC14 pairs1/4 and2/3 independently; stock
TCU bit5 drives both pairs. A separate6E2A counter overrides all four.
The ECU also supports216 bit2 through3AE52, but this TCU clears that bit.
Bit6 is not the stock source of6E64: B81B3=0 chooses231 bit4 plus7346.

4D716 updates each cylinder only for the matching event class in ROM table
4F4F0. It ORs/clears80 in78CF+cylinder and calls42EA8. 42EA8 aggregates
the four status bits, combines other inhibition sources and an8B5C0
diagnostic overlay, then stores mask736A and Boolean7368. The test visits
each cylinder event and controls the diagnostic overlay, rather than
pretending a single function call updates all cylinders at once.

44E50 selects an exact floating-point zero for cut cylinders. Nonzero
alternative commands were explicitly seeded, so default zero-filled RAM
cannot accidentally pass the test. The continuation4514C reads7408 and
feeds a larger fuel calculation;4D6EC reads741C and scales by1000 into78B0.
That intervening calculation and the final injector-timer endpoint are NOT
yet proven. The supported conclusion is software command suppression, not
a demonstrated electrical injector shutdown on a running vehicle.

Freshness caveat established by execution: decrementing the216 receipt
counter1->0 via34C66 does NOT by itself clear the decoded bit5 request in
34CEC. Network flag69E2=1 also does not clear this bit there. These paths
still initiate the countdown/zeroing chain under the controlled local gates.
They must not be described as the complete ECU fault policy: other tasks
can change gates, mode or global state. MT mode or734C!=1 clears the
request in the tested normalization path. Whole-system timeout/DTC handling
is still required to establish the real loss-of-TCU behavior.

Verification: python research/ecu-at-can/verify_actuation.py
  80 paired flag/condition scenarios (all16 source flag combinations,
  active/MT/config-off/expired-receipt/network-fault states), six independent
  local-gate rejection cases, TCU modes0/16, a held-request lifecycle over
  101 follow-up calls plus release/reassert, and four ECU-local pair cases.
  Saved output: actuation-verification.json.

The TCU normal-mode test sets92C6 bit5 to invalidate the unrelated byte4
numeric field, avoiding its divider while executing the full sender's flag
path. Word5 stays valid. Source9454 is a controlled internal input: its
upstream generation conditions have not been executed. Candidate writer
2512E is inside the250xx routine and must be traced next.

sh_exact_float.py adds bit-preserving moves and EXACT finite arithmetic to
the integer interpreter. It rejects inexact, subnormal and non-finite
arithmetic instead of substituting host rounding for SH-2E truncation.
The CAN216 integer-valued normalization is exact; no general FPU/exception,
peripheral, scheduling or physical-vehicle emulation is claimed. Manual
FMAC example2*4+1=9 and inexact-result rejection are checked independently.

231: SIX-STATE AND SELECTOR DECODING

TCU application sender 19414 calls 19912 for byte 0's upper nibble.
With FFFF8080 == 6 and fault bit 6 of FFFF92CD clear, internal values
0..5 at FFFF8081 encode as upper-nibble values 1..6. Invalid cases can
encode F; other controller states can encode 0 or E. These are strong
gear-state candidates, but current versus commanded gear is unresolved.

The ECU unpacker 35BB8 reads byte 0 to FFFF6ADC, byte 1 to FFFF6ADD,
and the word at bytes 2..3 to FFFF6ADA. Normalizer 3585C:
  upper nibble 1..6 -> one-hot flags FFFF6ACB..FFFF6AD0
  lower nibble 0..6 -> one-hot flags FFFF6AD1..FFFF6AD7
  other nibble values -> all corresponding flags zero
  byte1 bit7 -> FFFF6AC8; bit4 -> FFFF6AC9; bit3 -> FFFF6ACA
The mode/configuration gate skips normalization entirely when inactive;
it does not itself clear previously stored state flags.

Lower-nibble producer at 194AC..19566 counts four input flags. Multiple
active flags or the fault bit produce F; otherwise the selected flags
produce codes 1,2,3,4 (or 0 when none). Physical P/R/N/D labels need a
trace to the selector input wiring. Do not assign labels from code order.
New selector-inputs.txt traces the first four inputs to sampled PKDR bits2..5
and executes their complete filtering-to-ECU chain. Codes1/3 combine at ECU
411F0 into723A/7244; the individual physical labels remain hypotheses.

Bytes 2..3 come from 198BE: invalid conditions return FFFF; otherwise
clamp(signed32[FFFFA5A8] - 10, 10, 499). The physical unit is unresolved.
The ECU ignores bytes 4..7 in its unpacker despite the TCU sending them.

REVERSE DIRECTION: ECU TO TCU

201: ECU assembler 365D0 packs three BE words from FFFF6B3C, FFFF6B3E,
FFFF6B38, then bytes FFFF6B40/41. Its first value comes from the filtered
signal at FFFF6B34, sourced from FFFF6DB4. Conversion divisor 0.25 at
36820 is consistent with RPM*4. TCU getter 1C890 reconstructs that same
word from FFFF8F39. Consumer 171CC applies conversion helper 10F38 using
tables 5C812/5C5A4, storing a value at FFFF8814 and validity at FFFF8816.
The pack/getter pairing is executed by the verifier; physical RPM labeling
is still an inference until the source/conversion chain is fully named.

Follow-up tcu-speed.txt executes complete201 receipt dispatch: word0/4
->8814 and byte6*5 ->8808, with invalid markers retaining old values but
changing validity.1225 audited callbacks read only payload0/1/6; this does
not exclude other computed consumers of bytes4/5. The same record executes
the TCU216 numeric source, limiter and fault recovery through ECU201.

200: ECU assembler near 36234 writes words from FFFF6B1C/1E/20; 362AA
copies FFFF6B22 to byte 6. TCU 176B0 consumes byte6 bit0 at FFFF8F46
into FFFF88D0 with validity FFFF88D1. Other fields remain untraced.
240: ECU assembler 36F08 -> FFFF6B70 -> TCU FFFF8F24, consumed near
17FA4. Remaining reverse-direction fields require further investigation.

TIMING AND FAULTS

TCU records at 5C610, stride 28, include nominal scheduling counts:
216=10, 218=20, 231=25, 4C1=100. 19D44 forms deadlines using the counter
returned by 11874 (FFFF84D0). 11864 increments that counter once per
call through 128B6 <- 123C2 <- CMT0 ISR 16D6C. Initialization 16D5C
writes 624 to CMCOR0 (FFFFF716) and starts CMT0. Clock divider and board
clock must be established before asserting these periods in milliseconds.

ECU receive counters:
  216 FFFF6A5D / reload calibration B8249 / decrement 34C66
  218 FFFF6A90 / reload calibration B824A / decrement 3519E
  231 FFFF6AD8 / reload calibration B824B / decrement 357E4
Fresh-message handlers reload them. Network flags FFFF69E0, FFFF69E2,
FFFF735A bit7 and other per-path conditions affect validity. Full fault
aggregation, DTC assignment, timeout units and recovery sequences are open.

REPRODUCING EXECUTABLE EVIDENCE

  python research/ecu-at-can/verify_bridge.py

The script pins both SHA256 hashes and runs the actual unmodified integer
SH instructions using sh_subset.py. It includes real bitfield helper and
interrupt-mask helper code. It does not mock the selected packer bodies.

Checks:
  576 generic bitfield-setter cases
  64 vectors each for 216, 218, 231 pack/unpack and reverse 201 pack/get
  3 complete 218 sender mode examples
  6 complete 231 sender -> ECU state-normalizer examples
  256 ECU nibble-decoder combinations
  3 inactive mode/configuration gate cases
  7 complete 216 word-producer cases, including signed limits and sentinels
  Total: 1,107 cases

The generic bitfield helper 5AD7C uses MSB-relative offsets:
shift = 8 - offset - width. Descriptor 0001 writes bit 7, not bit 0;
0004 writes the high nibble and 0404 the low nibble.

This is a strict integer instruction subset with synthetic zero-filled RAM,
an artificial stack, and direct payload transfers. Unsupported instructions
raise errors. It does not simulate peripherals, actual interrupts, FPU,
scheduling, or the vehicle. Floating-point formulas are not tested by this
integer interpreter; the separate actuation harness now executes the exact
CAN216 normalization and command-copy path. Assertions must remain enabled.

verification.json is the saved output. import-verification.json preserves
the original read-only checksum/identity/calibration check. disassembly.txt
contains selected ROM excerpts; disassemble.py regenerates them using an
SH-capable GNU objdump, or finds aligned literal references for follow-up.
Literal searches miss some GBR-relative, computed, and MOV.W references.
Raw disassembly can render literal pools as instructions: follow branches
and SH delay slots rather than treating every printed line as executable.

PRIORITIZED REMAINING WORK

1. Continue CAN211 spark endpoints per can211-spark.txt: ignition timer,
   model coefficients and other throttle/fuel paths remain open.
   Trace 216 / FFFF6A34 and FFFF6A30 through ECU output arbitration to
   named torque, load, throttle, ignition or fuel commands.
2. Name 218 fields from both origins and consumers, especially 941C and
   the ECU 2D9C0..2F194 state logic; avoid a premature spark-retard label.
3. Trace 231 selector inputs and determine actual versus target gear.
4. Complete ECU->TCU 200/201/215/240/420 field maps and scaling.
5. Establish timer clock/dividers, exact frame deadlines, timeout-to-DTC
   paths, bus-off recovery and stale-data behavior on both ends.
6. Check OEM software pairing and use captures/hardware to validate the
   inferred physical meanings and timing. No hardware testing occurred.

EXTERNAL PRIMARY/ORIGINAL SOURCES

Romdrop author definitions and factory CRC database:
https://github.com/speepsio/romdrop/blob/master/metadata/lffeee.xml
https://github.com/speepsio/romdrop/blob/master/romdrop.crc

Renesas SH7055S hardware manual, HCAN register map and CMT register map:
https://www.renesas.com/en/document/mah/sh-2e-sh7055s-hardware-manual
Appendix A, printed pages 910 onward; CMT chapter 14, printed pages 448-452.

Renesas SH7058 hardware manual, ECU HCAN-II register map:
https://www.renesas.com/en/document/mah/sh-2e-sh7058-f-ztat-tm-hardware-manual

Renesas SH-2E software manual REJ09B0316-0200:
https://www.renesas.com/en/document/mah/sh-2e-software-manual
FPU rounding; FLOAT/FMAC/FMOV, printed pages184..191. The new bounded
execution harness accepts only exact arithmetic results.

Mazda published ratios (cross-check, not proof of software pairing):
https://news.mazdausa.com/download/2010-MX-5-specs.pdf

Supplier's own LFFE automatic-ROM listing (provenance context):
https://www.mazdaecu.eu/mazda-mx-5/mazda-mx-5-nc/2008-2.0-mzr-a-t-stage5-lffe/

2026-10-07 follow-up: tcu-cmt1-delivery.txt full320/2560CMT1/32000CMT0/
80actualhold returns PASS, exactprior320. tcu-cmt-configuration.txt verifies
originalstartup andconditional256:125 eventratio, distinct fromsupplied100:8.
Clock/task scheduling andphysicalintegration remainopen. Tractionevent2
producer/order, CAN211/21A sender/units/remoteDSC andbothroof directions with
interruption/reversal/timeout/sync/recovery remainexplicit inCHECKPOINT.txt.

2026-10-07: tcu-interrupt-setup.txt verifies VBR/GBR/INTC localstartup,
CMT0/1 compatiblepriorities9/8. Exact256:125 clockprefix8 passes butchanges
freshness at4 underonce/taskcapturefixture; full320 sensitivityrunpending.
Nativeapplicationclock16A3C/16A58 isnext concretelead, withunverifiedrelative
81920peripheralclock period. BroaderECU/AT, tractionevent2/CAN211/21A/remoteDSC
andbothroof directions/interruption/recovery remainopen inCHECKPOINT.txt.

2026-10-07: tcu-application-interrupt.txt verifies256init/2816gate/26original
ISRprefixes andcompleteapplicationbody. Conditional81920phi applicationperiod
nowhasexecutedcompare-update support; retainedtiming/capturejoin remainsnext.
control-event2-producer-lead.txt savesstaticECU queuedproducer1826E->2BC8C
->DAE8bank0/index4->F5A0selector3. Executeproducer/consumer/order vs task7 next.
Neither closesCAN211/21A sender/units/remoteDSC orbothroof directions/recovery.
Ghidrarefreshverified; fullclockratio sensitivityrun stilllive inCHECKPOINT.txt.
