"""Receive ISR prefix boundary matrix and executed frame/expiry/recovery chains.

Selected original mailboxes/finiteHCAN samples; no RTE or hardware proof.
"""
import json
from pathlib import Path
import tcu_receive_fixture as rx
from verify_can201_byte6 import r, w

ROOT = Path(__file__).resolve().parent


def main(indices=(1, 6, 8), filename='tcu-receive-admission-verification.json'):
    t = rx.fixture()
    count = 0
    for index in indices:
        for mode in range(256):
            for dlc in sorted({0, rx.LENGTHS[index]-1, rx.LENGTHS[index], 8}):
                w(t, 0x8F6C, mode)
                w(t, 0x8F71, 0xA5)
                w(t, 0x8F4E, 0x55AA, 2)
                t.sr = 0xA0 | (mode & 1)
                payload = bytes((index*7+mode+i*11) & 255 for i in range(8))
                result = rx.receipt(t, index, payload, dlc)
                assert result['admitted'] == (dlc >= rx.LENGTHS[index] and bool(mode & 12))
                count += 1
    # Supply actualprefix->dispatcher receipts, then advance originaltickroutine.
    # Otherrecord deadlines are explicitfuture fixtures to isolate these3records.
    chains = []
    for recovery in [0, 1]:
        for index, record in [(1, 12), (6, 3), (8, 1)]:
            t = rx.fixture()
            w(t, 0x8F6C, 8)
            w(t, 0x868C, recovery)
            for i in range(18):
                w(t, 0x8B38+8*i, 100000, 4)
            payload = (rx.phase.received.PAYLOAD201 if index == 8 else
                       rx.phase.received.PAYLOAD215 if index == 6 else bytes(8))
            period = 25 if index == 1 else 10
            rows = []
            for tick in range(period+2):
                if tick:
                    t.run(0x11864)
                fresh = tick in [0, period+1]
                if fresh:
                    rx.receipt(t, index, payload)
                    t.run(0x1BD10)
                    # Normalreturn sentinel is not an executed instruction.
                    row = t.rx_pending.pop()
                    assert row['entry'] == '0x1bd10' and row['return_pc'] == 0xFFFFFFF0
                t.run(0x19AF0)
                row = t.rx_pending.pop()
                assert row['entry'] == '0x19af0'
                after = rx.receive_state(t)
                for actual, expected in [('deadlines', 'expected_deadlines'),
                                         ('fresh', 'expected_fresh'), ('faults', 'expected_faults')]:
                    assert after[actual] == row[expected]
                expected_fault = (1 << record) if tick == period or tick == period+1 and not recovery else 0
                assert after['faults'] == expected_fault
                if tick in [0, period-1, period, period+1]:
                    rows.append(dict(tick=tick, received=fresh, fault=after['faults'],
                                     deadline=after['deadlines'][record]))
            chains.append(dict(index=index, record=record, recovery=recovery, rows=rows))
    out = dict(status='PASS', scope=__doc__, whole_ram_isr_prefix_cases=count,
               receipt_expiry_recovery_chains=chains)
    out['logical_indices'] = list(indices)
    (ROOT/filename).write_text(json.dumps(out, indent=2)+'\n')
    print('PASS', count, 'wholeRAMprefix cases;', len(chains), 'expiry/recovery chains')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extended', action='store_true')
    args = parser.parse_args()
    if args.extended:
        main(tuple(rx.SLOTS), 'tcu-receive-recovery-prefix-verification.json')
    else:
        main()
