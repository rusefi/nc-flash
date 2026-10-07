"""Check retained startup results and byte-identical regression artifacts.

This verifies recorded outputs; rerun the firmware probes separately to
reproduce execution. State projection equality is not whole-RAM equality.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'tcu-readiness-admission-verification.json':
        'db4849a92f29757c856af6a683218ddddd3264f84fba2bb26c69844f45c8f363',
    'tcu-diagnostic-timer-verification.json':
        'ea2c938791fec667402fdaf93fc6d6a862766fac7dc20b6ff0ae894b5df0cc8f',
    'tcu-diagnostic-timeline-prefix8.json':
        '08b0c7be5580e563eafb610e27f7ad4b6486b35e216e7d60dbd78dd3ce8b5308',
    'tcu-diagnostic-observer-reuse-prefix8.json':
        '08b0c7be5580e563eafb610e27f7ad4b6486b35e216e7d60dbd78dd3ce8b5308',
}


def main():
    for name, digest in EXPECTED.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    old = json.loads((ROOT / 'tcu-readiness-admission-verification.json').read_text())
    new = json.loads((ROOT / 'tcu-diagnostic-startup-verification.json').read_text())
    keys = ['phi', 'rank', 'kind', 'ordinal', 'state']
    summaries = []
    assert len(old['scenarios']) == len(new['scenarios']) == 3
    for prior, current in zip(old['scenarios'], new['scenarios']):
        assert prior['status'] == current['status'] == 'PASS'
        assert (prior['poll_period'], prior['timestamp_epoch']) == (
            current['poll_period'], current['timestamp_epoch'])
        rows = [r for r in current['rows']
                if r['phi'] <= 3000000 and r['kind'] != 'diagnostic']
        project = lambda rs: [{k: r[k] for k in keys} for r in rs]
        assert project(rows) == project(prior['rows'])
        diagnostics = [r for r in current['rows'] if r['kind'] == 'diagnostic']
        assert len(diagnostics) == 8
        for index, row in enumerate(diagnostics):
            event = row['event']
            changes = {a: [v, event['after'][a]]
                       for a, v in event['before'].items() if v != event['after'][a]}
            expected = ({'0x8006': [1, 3], **{a: [0, 1] for a in
                        ['0xa936', '0xa978', '0xa98e', '0xa98d', '0xa98f']}}
                        if index == 5 else {})
            assert changes == expected, (index, changes)
            assert event['admitted'] == (index == 5)
            assert event['differential_application_ram_checked']
            assert event['registers_checked']
        summaries.append(current['summary'])
    totals = {key: sum(s[key] for s in summaries) for key in [
        'cmt0_interrupts', 'application_interrupts', 'foreground_ram_checks',
        'capture_return_ram_checks', 'command_pin_return_checks',
        'diagnostic_interrupts', 'diagnostic_actual_return_ram_checks']}
    assert list(totals.values()) == [600, 144, 224, 93, 288, 24, 13]
    result = dict(status='PASS', scenarios=3, totals=totals,
                  byte_identical_regressions=EXPECTED,
                  unchanged_prior_row_fields=keys,
                  limits='Recorded-output validation; not firmware reexecution or whole-RAM equivalence.')
    (ROOT / 'tcu-diagnostic-startup-records-verification.json').write_text(
        json.dumps(result, indent=2) + '\n')
    print(result)


if __name__ == '__main__':
    main()
