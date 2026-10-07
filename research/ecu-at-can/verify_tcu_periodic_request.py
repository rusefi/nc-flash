"""Check complete-task request service ordering and delayed cancellation.

Fault input is explicitly seeded mapped diagnostic summaryA962 bit2, not a
sensor fault or physical diagnosis. Original21C1C,1FD24,31524 and queue cleanup
execute. No internal916F or9410 injection; no externally supplied ack/event4.
"""
import json
from pathlib import Path

import probe_tcu_periodic_request as probe
from verify_can201_byte6 import w, r

ROOT = Path(__file__).resolve().parent


def main():
    saved = json.loads((ROOT/'tcu-periodic-request-probe.json').read_text())
    assert len(saved['rows']) == 48
    baseline_checks = 0
    for row in saved['rows']:
        assert row['status'] == 'returned'
        assert row['phase'] == row['call'] % 8
        events = [4, 2] if row['phase'] % 2 == 0 else [4]
        if not row['managed'] and row['call'] in [1, 5, 9, 13]:
            events.append(1)
        assert [v['event'] for v in row['events']] == events
        assert all(v['payload'] == 0 for v in row['events'] if v['event'] != 1)
        assert all(v['caller'] == '0x48fac' for v in row['events'] if v['event'] == 1)
        assert row['after']['0xa2ba'] == int(row['managed'])
        assert row['after']['0x916f'] & 1 == 0
        assert row['after']['0x9410'] == 0
        if row['managed']:
            assert row['record_bytes'][0] == 2
            assert ('0x4cc90' in row['callbacks']) == (row['call'] % 2 == 1)
        expected_entries = ['0x1fd24', '0x23bf0'] if row['phase'] in [0, 4] else []
        assert [v['entry'] for v in row['checks']] == expected_entries
        assert all(v['expected'] == v['actual'] == 0 for v in row['checks'])
        baseline_checks += len(row['checks'])

    paths = []
    for phase in [0, 1, 4, 7]:
        t, record = probe.fixture(phase=phase, managed=True)
        # Explicit stored diagnostic input, retained until recovery at call8.
        w(t, 0xA962, 4)
        first_aggregate = (-phase) % 4
        cancel_call = next(c for c in range(first_aggregate+1, 8) if c % 2 == 1)
        recovery_call = next(c for c in range(8, 12) if (phase+c) % 4 == 0)
        rows = []
        for call in range(12):
            if call == 8:
                w(t, 0xA962, 0)
            t.request_checks = []
            t.request_events = []
            t.request_calls = []
            result = probe.app.run(t)
            assert t.request_pending is None
            # Original full task publishes the explicit diagnostic input.
            assert bool(r(t, 0x92C6) & 4) == (first_aggregate <= call < recovery_call)
            assert bool(r(t, 0x916F) & 1) == (first_aggregate <= call < recovery_call)
            assert r(t, 0xA2BA) == int(call < cancel_call)
            assert ('0x4cca4' in t.request_calls) == (call == cancel_call)
            acknowledgements = [v for v in t.request_events if v['event'] == 3]
            assert len(acknowledgements) == int(call == cancel_call)
            assert all(v['caller'] == '0x4c372' for v in acknowledgements)
            assert all(v['event'] in [2, 3, 4] for v in t.request_events)
            if call >= cancel_call:
                assert r(t, 0xA202, 2) == r(t, 0xA1AC) == 0
                assert r(t, 0x9F3C, 4) == 0x007FFFFF
                assert r(t, record, 20) == 0
            rows.append(dict(call=call, phase=(phase+call) % 8,
                             summary=r(t, 0xA962), published=r(t, 0x92C6),
                             cancellation=r(t, 0x916F), enable=r(t, 0x9410),
                             manager=r(t, 0xA2B8), count=r(t, 0xA2BA),
                             events=t.request_events.copy(),
                             callbacks=t.request_calls.copy(),
                             checks=t.request_checks.copy(),
                             application=result))
        paths.append(dict(initial_phase=phase, aggregate_call=first_aggregate,
                          cancellation_call=cancel_call,
                          recovery_aggregate_call=recovery_call, rows=rows))

    # Default helper behavior remains available to existing direct experiments.
    creation_cases = 0
    for code in [6, 7]:
        for operation in [0, 0x17]:
            for head in [0, 15]:
                probe.admission.upstream(code, operation, head)
                creation_cases += 1
    data = dict(status='PASS', scope=__doc__, rom_sha256=saved['rom_sha256'],
                baseline_task_calls=48, fault_recovery_task_calls=48,
                baseline_selected_field_checks=baseline_checks,
                fault_selected_field_checks=sum(len(row['checks'])
                                               for p in paths for row in p['rows']),
                existing_whole_ram_command_boundaries=192,
                original_creation_regression_cases=creation_cases, paths=paths,
                limits='Selected916Fbit0/9410byte oracles, not complete aggregate RAM. '
                       'Creation explicitly delivered through original event1 before tasks. '
                       'No natural transition admission, overlap, hardware cadence or physical proof.')
    (ROOT/'tcu-periodic-request-verification.json').write_text(json.dumps(data, indent=2)+'\n')
    print('PASS', {k:v for k,v in data.items() if k.endswith('calls') or k.endswith('checks')})
    print('cancellation calls', [(p['initial_phase'], p['cancellation_call']) for p in paths])


if __name__ == '__main__':
    main()
