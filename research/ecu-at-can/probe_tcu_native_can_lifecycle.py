"""Native startup and CAN/capture loss through 320 application periods.

Reuse one native event loop and original request observer/acknowledgement model.
No forced task/readiness/receive mode or post-admission history reset. Explicit
finite peripheral samples, external CAN201/215/zero4EC traffic and pulse inputs;
no full boot, physical interrupt/bus/actuator or remote-controller proof.
"""
import copy
import hashlib
import json
from pathlib import Path

import verify_tcu_native_can_timeline as timeline
import probe_tcu_initialized_requests as requests
from probe_tcu_capture_timeline import edges, APP_PERIOD, LOSS_TIME
from verify_can201_byte6 import TCU

ROOT = Path(__file__).resolve().parent
END_PHI = 320 * APP_PERIOD


class Machine(timeline.Machine):
    def instruction(self, pc):
        requests.observe_initialized(self, pc)
        return super().instruction(pc)

    def observe_event(self, kind, ordinal):
        assert not self.creation_returns and self.ack_pending is None
        assert len(self.acks) == len(self.ack_checks)
        out = {}
        if kind == 'application' or self.creations or self.acks or self.retired:
            out['request_observation'] = dict(
                creations=copy.deepcopy(self.creations), acks=self.acks.copy(),
                ack_checks=copy.deepcopy(self.ack_checks), retired=self.retired.copy())
        if kind == 'application':
            out['request_snapshot'] = requests.snapshot(self)
        self.creations, self.acks, self.ack_checks, self.retired = [],[],[],[]
        return out


def fixture():
    t = timeline.fixture(end_phi=END_PHI)
    t.__class__ = Machine
    t.creations, t.creation_returns, t.acks = [],[],[]
    t.ack_pending = None
    t.ack_checks, t.retired = [],[]
    return t


def verify(result):
    rows = result['rows']
    apps = [row for row in rows if row['kind']=='application']
    assert len(apps) == 320
    for channel in ['A','B']:
        delivered = [row['phi'] for row in rows if row['kind']=='capture_'+channel
                     and row['event']['delivered']]
        expected = [phi for phi in edges(channel)
                    if result['summary']['capture_enabled_phi'] < phi <= END_PHI]
        assert delivered == expected and all(phi < LOSS_TIME for phi in delivered)
    counts = {kind:sum(row['kind']==kind for row in rows)
              for kind in ['can_task','receipt','cmt0','cmt1','diagnostic']}
    assert counts == dict(can_task=END_PHI//20000,receipt=320,cmt0=END_PHI//20000,
                          cmt1=640,diagnostic=END_PHI//500000)
    # Same input trajectory through the old horizon: preserve every old field,
    # including native state, all interrupt/return oracles and callback history.
    baseline = json.loads((ROOT/'tcu-native-can-timeline-verification.json').read_text())['scenarios'][0]
    prefix = [{k:v for k,v in row.items() if k not in ['request_observation','request_snapshot']}
              for row in rows if row['phi'] <= timeline.END_PHI]
    assert prefix == baseline['rows']
    assert result['initialization'] == baseline['initialization']
    assert result['extra_initialization'] == baseline['extra_initialization']
    old = json.loads((ROOT/'tcu-diagnostic-timeline-probe.json').read_text())['rows']
    assert len(old)==320
    comparisons = []
    for app,prior in zip(apps,old):
        now=app['request_snapshot']; before=prior['after']
        differences={k:dict(native=now[k],prior=before[k])
                     for k in now if now[k]!=before[k]}
        comparisons.append(dict(application_ordinal=app['ordinal'],prior_call=prior['call'],
                                differing_fields=differences))
    observations=[row for row in rows if 'request_observation' in row]
    transitions=[]
    previous=None
    for row in apps:
        snap=row['request_snapshot']; event=row['request_observation']
        state={k:snap[k] for k in ['0xa2ba','0x96c5','0x96c4']}
        if state!=previous or event['creations'] or event['retired']:
            transitions.append(dict(application_ordinal=row['ordinal'],state=state,
                retired=event['retired'],heap=snap['heap_first_header_9f3c']))
        previous=state
    summary=dict(counts=counts,received_frames=3*counts['receipt'],
        capture_interrupts={c:sum(row['kind']=='capture_'+c and row['event']['delivered'] for row in rows) for c in ['A','B']},
        diagnostic_actual_return_ram_checks=rows[-1]['diagnostic_ram_checks'],
        request_lifecycle_changes=transitions,
        request_word_values=sorted({row['request_snapshot']['request_word_915a'] for row in apps}),
        final_receive_state=rows[-1]['receive_state'],final_sources=rows[-1]['sources'],
        default_prefix_rows_compared=len(prefix),pulse_loss_phi=LOSS_TIME,
        creations=[dict(phi=row['phi'],kind=row['kind'],ordinal=row['ordinal'],
                        payload=c['payload']) for row in observations
                   for c in row['request_observation']['creations']],
        whole_ram_ack_checks=sum(len(row['request_observation']['ack_checks']) for row in observations),
        application_snapshots_different=sum(bool(row['differing_fields']) for row in comparisons),
        final_snapshot=apps[-1]['request_snapshot'])
    return dict(summary=summary,comparison_to_prior_fixture=comparisons)


def main():
    result=timeline.capture.startup.native.run(50000,7,machine_factory=fixture,end_phi=END_PHI)
    out=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),scenario=result,
             limits='CAN period20000phi; externalGSR0, three frames each81920phi, prior pulse trajectory and loss280*81920. Initializer order/common zero event epoch/zero latency are fixture assumptions. No full boot/hardware actuation; all broader goals remain open.')
    path=ROOT/'tcu-native-can-lifecycle-probe.json'
    # Preserve execution even if the record comparison detects a regression.
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(dict(status=result['status'],summary=result.get('summary'),
               error=result.get('error'),pc=result.get('pc')),flush=True)
    assert result['status']=='PASS'
    verify_saved()


def verify_saved():
    # Compare serialized records on both sides: live MMIO tuples serialize as
    # JSON arrays. Do not compare raw Python tuples with a decoded baseline.
    path=ROOT/'tcu-native-can-lifecycle-probe.json'
    out=json.loads(path.read_text())
    assert out['scenario']['status']=='PASS'
    result=verify(out['scenario'])
    result.update(status='PASS',execution_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        limits='All original prefix record fields match, not hardware timing/fullboot. Comparison to prior forced-mode fixture reports differences without assuming equivalence.')
    (ROOT/'tcu-native-can-lifecycle-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['summary'],flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only',action='store_true')
    args=parser.parse_args()
    if args.verify_only:verify_saved()
    else:main()
