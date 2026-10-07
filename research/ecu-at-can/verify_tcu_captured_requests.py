"""Verify callback/task freshness and pairedCAN216 decoding from saved traces.

Measurement expected values come from an independent24-slot timestamp model,
not the observer's expected-result fields. Local execution/fixture scope only.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def verify(name, count, frames=False, interval=None):
    data = json.loads((ROOT/name).read_text())
    rows = data['rows']
    assert len(rows) == count and all(row['status'] == 'returned' for row in rows)
    history = [18*4096]*24
    head = 0
    ack_count = 0
    input_checks = 0
    creations = []
    requests = []
    measured_timestamp = 0
    for call, row in enumerate(rows):
        extra = row['extra']
        boundaries = extra['source_boundaries']
        expected_order = ['0x179a8', '0x17a58', '0x2124c']
        if call % 4 == 0:
            expected_order += ['0x2086c', '0x2117c']
        assert [v['entry'] for v in boundaries] == expected_order
        measured_interval = interval(call) if interval is not None else 5890 if call < 48 else 6490
        measured_timestamp += measured_interval
        assert extra['capture_intervals'] == [12160, measured_interval]
        assert boundaries[0]['argument'] == 12160*(call+1)
        assert boundaries[1]['argument'] == measured_timestamp
        expected_age = 255 if call == 0 else int(call % 2 == 0)
        assert boundaries[1]['before']['0x810c'] == expected_age
        assert boundaries[1]['after']['0x810c'] == 0
        assert boundaries[1]['after']['0x9244'] == expected_age
        if call == 0:
            value, period = 0, 0x7FFFFFFF
        else:
            head = (head+1) % 24
            history[head] = measured_interval//10
            period = sum(history)
            value = min(32767, 153600000//period)
        measured = boundaries[2]
        assert measured['measurement_checked']
        assert measured['after']['0x80ee'] == value
        assert measured['after']['0x9238'] == period
        assert measured['after']['0x800d'] == head
        sources = extra['final_sources']
        assert sources['0x80ee'] == value
        if call >= 20:
            assert sources['0x80ea'] == sources['0x80ec'] == 153600000//(18*1216)
        payload = extra['wire']['payload']
        source = sources['0x915a']
        signed = source-65536 if source & 32768 else source
        first = 65534 if source == 32767 else max(0, (signed >> 5)+512)
        assert int.from_bytes(bytes(payload[:2]), 'big') == first
        assert extra['wire']['normalized'] == first-512
        assert payload[4] == (255 if sources['0x92c6'] & 32 else min(254, value//96))
        if source != 32767:
            requests.append(dict(call=call, source=source, word=first,
                                 normalized=extra['wire']['normalized']))
        if frames:
            assert extra['received_ecu201'][6] == 156
            assert extra['received_ecu215'][6] == 195
            assert sources['0x809a'] == 24960 and sources['0x809c'] == 19968
            assert sources['0x9410'] == 7
            expected_checks = ['0x22f46', '0x230f0'] if call % 4 == 0 else []
            assert [v['entry'] for v in extra['input_checks']] == expected_checks
            input_checks += len(extra['input_checks'])
        assert row['acks'] == [v['arguments'] for v in row['ack_checks']]
        ack_count += len(row['ack_checks'])
        creations.extend(dict(call=call, payload=v['payload']) for v in row['creations'])
    return dict(task_calls=count, capture_returns=2*count, measurement_checks=count,
                paired_packet_decode_checks=count, whole_ram_ack_checks=ack_count,
                existing_whole_ram_command_checks=2*count,
                selected_gate_checks=sum(len(row['checks']) for row in rows),
                input_producer_checks=input_checks, creations=creations,
                admitted_numeric_requests=requests)


def main():
    result = dict(status='PASS', scope=__doc__,
                  capture_only=verify('tcu-captured-requests-probe.json', 96),
                  received=verify('tcu-received-captured-requests-probe.json', 128, True),
                  extended=verify('tcu-received-captured-requests-extended.json', 256, True))
    first = json.loads((ROOT/'tcu-received-captured-requests-probe.json').read_text())
    extended = json.loads((ROOT/'tcu-received-captured-requests-extended.json').read_text())
    assert first['rows'] == extended['rows'][:128]
    assert result['extended']['admitted_numeric_requests'] == [
        dict(call=call, source=306, word=521, normalized=9.0) for call in [167, 168]]
    result['identical_128_call_prefix'] = True
    (ROOT/'tcu-captured-requests-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS capture96, received128/256 and identical128 prefix')


if __name__ == '__main__':
    main()
