"""Bounded selector acceptance -> original phase/request creation -> CAN.

Only descending adjacent selections 3->2, 4->3 and 5->4 are covered.
Source RAM and call order are fixtures; physical gear and timing are unproved.
"""
import hashlib
import json

from verify_can201_byte6 import TCU, w, r
from verify_selection_reporting import report
from verify_tcu_request_dispatch import fixture
from verify_tcu_request_admission import periodic, paired_snapshot


def main():
    cases = []
    for old, code in [(3, 7), (4, 8), (5, 9)]:
        t = fixture()
        t.run(0x31524, 0)
        w(t, 0x606F, old)
        t.run(0x48BC0)
        w(t, 0x8080, 6)
        w(t, 0x8084, old-1)
        w(t, 0x92D0, 4)
        w(t, 0xA93A, 1)
        for address, value in [(0x80EA, 4672), (0x80F6, 4224),
                               (0x809C, 20000), (0x80EE, 1000)]:
            w(t, address, value, 2)
        snapshots = []
        for blocked in [True, False]:
            w(t, 0x9545, 4 if blocked else 0)
            t.run(0x48C08, limit=1000000)
            assert r(t, 0x8081) == old-int(not blocked)
            assert r(t, 0x96C5) == r(t, 0xA2BA) == int(not blocked)
            assert r(t, 0x9C87) == (255 if blocked else code)
            assert r(t, 0x9C88) == 0
            assert bool(r(t, 0x9C8A) & 1) == blocked
            snapshots.append({'blocked': blocked, **report(t),
                              'phase_count': r(t, 0x96C5),
                              'request_count': r(t, 0xA2BA)})
        record = r(t, 0xA2BC, 4) & 65535
        assert record == 0x9F40
        assert r(t, 0xA2C0, 2) == 8
        assert r(t, record) == 2 and r(t, record+1) == code
        assert [r(t, 0x95D4+i) for i in range(10, 15)] == [code, 0, 0, 0, 0]
        assert r(t, record+14, 2) == 9344
        assert r(t, record+16, 2) == 18688
        service_rows = []
        for call in range(1, 5):
            t.run(0x31524, 2, limit=1000000)
            periodic(t)
            assert r(t, 0x95E1) == 0 and r(t, record) == 2
            assert r(t, 0x915A, 2) == 0x7FFF
            returned = paired_snapshot(t)
            assert returned['at_correction'] == 0
            service_rows.append({'event2_calls': call,
                                 'phase_state': r(t, 0x95E1),
                                 'request_state': r(t, record), **returned})
        cases.append({'old': old, 'requested': old-1, 'transition_code': code,
                      'acceptance': snapshots, 'periodic': service_rows})
    print(json.dumps({'scope': __doc__.strip(),
                      'tcu_sha256': hashlib.sha256(TCU).hexdigest(),
                      'acceptance_can231_checks': 6,
                      'periodic_can216_ecu_checks': 12, 'cases': cases,
                      'limits': 'Zero reference/timer RAM remains explicit. Acceptance creates a request but does not prove phase activation. Only group8 is initialized for these cases. CAN216 snapshot helper forces byte4 invalid; ECU model/gates and CAN211 are fixtures. No physical timing, DSC attribution or OEM roof reception is established.'}, indent=2))


if __name__ == '__main__':
    main()
