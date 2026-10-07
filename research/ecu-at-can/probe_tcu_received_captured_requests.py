"""ECU-producedCAN201/215 + captures -> completeTCU task -> CAN216/ECU.

ECU sender model sources are explicit inputs; original encoders execute.
Receive-buffer delivery, secondary wrapper and capture/task ratio are supplied,
not physical HCAN delivery/admission. No internal TCUgate/request/age writes.
"""
from fractions import Fraction
import probe_tcu_captured_requests as capture
import verify_tcu_paired_input as primary
import verify_tcu_comparison_input as comparison
from verify_tcu_qualification_limit import phase_for_code
from verify_tcu_transition_classification import pending_model
from verify_can201_byte6 import ecu_payload, receive as receive201, w, r
from verify_can215_feedback import receive as receive215

PAYLOAD201 = ecu_payload(78, 78, 0)
PAYLOAD215 = primary.packet(25, Fraction(195, 2))


class Received(capture.Captured):
    def instruction(self, pc):
        if self.input_pending and self.input_pending[-1][0] == pc:
            _, expected, model, entry = self.input_pending.pop()
            for a in model.OUTPUT_WORDS+model.OUTPUT_BYTES:
                size = 1 if a in model.OUTPUT_BYTES else 2
                assert r(self, a, size) == expected[a], (hex(entry), hex(a), r(self, a, size), expected[a])
            self.input_checks.append(dict(entry=hex(entry), return_pc=hex(pc)))
        if pc in [0x22F46, 0x230F0]:
            model = primary if pc == 0x22F46 else comparison
            expected = model.snap(self)
            if pc == 0x22F46:
                model.producer_model(expected)
            else:
                model.producer_model(expected, pending_model(self), phase_for_code(self, expected[0x8089]))
            self.input_pending.append((self.pr, expected, model, pc))
        return super().instruction(pc)


def fixture():
    t = capture.fixture()
    t.__class__ = Received
    t.input_pending = []
    t.input_checks = []
    return t


def before_task(t, call):
    t.input_checks = []
    assert not t.input_pending
    capture.before_task(t, call)
    receive201(t, PAYLOAD201)
    receive215(t, PAYLOAD215)
    # Explicit disabled secondary frame, followed by its original full wrapper.
    # The wrapper's freshness/interrupt admission is outside this experiment.
    for i in range(7):
        w(t, 0x8F0D+i, 0)
    t.run(0x1ADD0)


def after_task(t, call):
    assert not t.input_pending
    row = capture.after_task(t, call)
    row['input_checks'] = t.input_checks
    row['received_ecu201'] = list(PAYLOAD201)
    row['received_ecu215'] = list(PAYLOAD215)
    return row


def main():
    capture.task.main(cycles=128, timer=True,
                      filename='tcu-received-captured-requests-probe.json',
                      machine_factory=fixture, before_task=before_task,
                      after_task=after_task, scope=__doc__)


if __name__ == '__main__':
    main()
