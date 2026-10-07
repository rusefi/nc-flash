"""Observe relevant initializer writes and verify subsequent activity boundaries.

Original1619A then five explicit event2 deliveries, without fabricated CA94
sampling. Zero RAM versus seeded activity counters distinguish writes from
zero fixture state. This is not full reset, physical boot or cadence proof.
"""
import hashlib
import json
from pathlib import Path
from sh_control_initialize_syscr import SystemStartup
from verify_control_activity_conditions import expected as condition_expected
from verify_control_activity_hold import expected as hold_expected, expected_timer
from verify_control_raw_inputs import application
from verify_control_contributions import ECU, r, w

ROOT = Path(__file__).resolve().parent
FIELDS = {0x9158:2, 0x915E:1, 0x915C:1, 0x8FD4:2, 0x8FD6:1, 0x8FD7:1,
          0x8FD8:1, 0x8FDF:1, 0x8FE0:1, 0x9125:1, 0x6604:1, 0x6605:1,
          0x6606:1, 0x660C:2, 0x660E:1, 0x660F:1, 0x6610:1, 0x6611:1,
          0x7358:1, 0x735A:1, 0x735B:1, 0x735C:1, 0x9149:1, 0x44A2:2,
          0x651C:1, 0x5360:1}


def fields(e):
    return {hex(a):r(e, a, size) for a, size in FIELDS.items()}


def validate_rows(rows):
    assert [row['seeded'] for row in rows] == [False, True]
    for row in rows:
        assert row['status'] == 'returned' and len(row['tasks']) == 5
        assert len(row['checked']) == 6
        unchanged = ['0x9158', '0x915e', '0x915c']
        assert all(row['initialized'][key] == row['before'][key] for key in unchanged)
        assert not any(set(item['after']) & set(unchanged) for item in row['writes'] if item['stage'] == 'initializer')
        reload_value = min(65535, sum(int.from_bytes(ECU[a:a+2], 'big') for a in [0xE0862, 0xE0864, 0xE0866]))
        assert row['initialized']['0x8fd4'] == reload_value
        assert row['initialized']['0x8fd6'] == row['initialized']['0x8fd7'] == ECU[0xE0860]
        assert all(item['0x9158'] == row['before']['0x9158'] and item['0x915e'] == row['before']['0x915e'] for item in row['tasks'])
        assert row['tasks'][0]['0x915c'] == 0 and row['tasks'][0]['0x9149'] == 1
        assert [item['0x651c'] for item in row['tasks']] == [1, 2, 3, 4, 0]


class InitializedActivity(SystemStartup):
    def __init__(self):
        super().__init__()
        self.stage = 'fixture'
        self.activity_writes = []
        self.activity_pending = []
        self.activity_checked = []

    def write(self, address, value, size):
        result = super().write(address, value, size)
        targets = [a for a, n in FIELDS.items() if address < 0xFFFF0000+a+n and 0xFFFF0000+a < address+size]
        if targets and self.stage != 'fixture':
            self.activity_writes.append(dict(stage=self.stage, pc=getattr(self, 'instruction_pc', self.pc),
                branch_pc=self.pc, address=address, value=value, size=size,
                after={hex(a):r(self,a,FIELDS[a]) for a in targets}))
        return result

    def instruction(self, pc):
        self.instruction_pc = pc
        while self.activity_pending and pc == self.activity_pending[-1]['return_pc']:
            item = self.activity_pending.pop()
            assert application(self) == item.pop('expected'), (hex(item['entry']), self.stage)
            item['after'] = fields(self)
            self.activity_checked.append(item)
        if pc in [0x6F2C8, 0x6F34C, 0x74ED2, 0x74D62, 0x6F422]:
            if pc in [0x6F2C8, 0x6F34C, 0x74ED2]:
                want = condition_expected(self, pc)
            elif pc == 0x74D62:
                want = hold_expected(self)[0]
            else:
                want = expected_timer(self)[0]
            self.activity_pending.append(dict(entry=pc, return_pc=self.pr, expected=want,
                                               before=fields(self), stage=self.stage))
        return super().instruction(pc)


def main():
    rows = []
    for seeded in [False, True]:
        e = InitializedActivity(); e.registers[0xFFFFF74E] = 1
        if seeded:
            for a, val in [(0x9158,0xA55A),(0x915E,0x5A),(0x915C,0xA5),
                           (0x8FD4,0x1234),(0x8FD6,0xA5),(0x8FD7,0x5A)]:
                w(e,a,val,FIELDS[a])
        row = dict(seeded=seeded, before=fields(e), tasks=[])
        try:
            e.stage = 'initializer'; saved=e.r[8:16].copy();gbr=e.gbr
            e.run(0x1619A,limit=2000000)
            assert e.r[8:16] == saved and e.gbr == gbr and not e.activity_pending
            row['initialized'] = fields(e)
            e.stage='fixture';e.write(0xFFFFD800,2,4)
            for call in range(5):
                e.stage=f'event2-{call}';saved=e.r[8:16].copy();gbr=e.gbr
                e.run(0x2BCE6,0xFFFFD800,limit=1000000)
                assert e.r[8:16] == saved and e.gbr == gbr and not e.activity_pending
                row['tasks'].append(fields(e))
            row['status'] = 'returned'
        except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
            row.update(status=type(exc).__name__+': '+str(exc),stage=e.stage,pc=e.pc,tail=e.tail)
        row.update(writes=e.activity_writes,checked=e.activity_checked,
                   bank=e.bank_checked,selftest_returns=e.selftest_returns)
        rows.append(row)
        (ROOT/'control-initialized-activity-verification.json').write_text(json.dumps(dict(
            rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,rows=rows),indent=2)+'\n')
        print('seeded',seeded,row['status'],'task returns',len(row['tasks']),
              'boundaries',len(e.activity_checked),flush=True)
    validate_rows(rows)
    path = ROOT/'control-initialized-activity-verification.json'
    result = json.loads(path.read_text()); result['postconditions_verified'] = True
    path.write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
