"""Original receive ISR prefixes -> original fulltask dispatch/watchdog/request.

HCAN register samples and receipt/capture/task interleave remain fixtures.
Stop each ISR at restored-register pre-RTE boundary. Full126EC returns normally.
No injected payload buffers, pending bits, freshness bits or callback dispatch.
CAN mode8F6C=8 is an explicit setup input; no fullboot/physical bus claim.
"""
import tcu_receive_fixture as rx
from verify_can201_byte6 import w


def fixture():
    t = rx.fixture()
    w(t, 0x8F6C, 8)
    return t


def before_task(t, call):
    assert not t.numeric_pending and not t.input_pending and not t.rx_pending
    t.numeric_checks, t.input_checks = [], []
    t.rx_boundaries, t.rx_callbacks = [], []
    rx.phase.received.capture.before_task(t, call)
    if getattr(t, 'advance_receive_tick', False):
        t.run(0x11864)
    t.rx_receipts = [rx.receipt(t, index, payload) for index, payload in
                     [(8, rx.phase.received.PAYLOAD201), (6, rx.phase.received.PAYLOAD215),
                      (1, bytes(8))]
                    if not (getattr(t, 'omit_can201', False) and index == 8 and 96 <= call < 112)]


def after_task(t, call):
    assert not t.rx_pending
    row = rx.phase.after_task(t, call)
    row.update(receive_boundaries=t.rx_boundaries, receive_callbacks=t.rx_callbacks,
               receive_prefixes=t.rx_receipts, final_receive_state=rx.receive_state(t))
    return row


def expiry_fixture():
    t = fixture()
    t.advance_receive_tick = t.omit_can201 = True
    # Explicit initialized-recovery gate, not execution of full15574 startup.
    w(t, 0x868C, 1)
    return t


def main(cycles=32, filename='tcu-admitted-requests-probe.json', machine_factory=fixture):
    rx.phase.received.capture.task.main(cycles=cycles, timer=True, filename=filename,
        machine_factory=machine_factory, before_task=before_task, after_task=after_task, scope=__doc__)


if __name__ == '__main__':
    main()
