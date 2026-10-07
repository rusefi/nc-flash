"""Check native diagnostic admission and communication-policy task traces.

Receive watchdog expectations are recomputed from each saved entry state.
Admission whole-RAM equality is checked during execution, not reconstructed
from the selected snapshots here. Other diagnostic bodies are coverage only.
"""
import json
from collections import Counter
from pathlib import Path
from tcu_receive_fixture import watchdog_state_model
from verify_tcu_captured_requests import verify

ROOT = Path(__file__).resolve().parent


def check(name, count, baseline=False):
    rows = json.loads((ROOT/name).read_text())["rows"]
    assert len(rows) == count
    counts = Counter()
    transitions = []
    prior = None
    for call, row in enumerate(rows):
        assert row["call"] == call and row["status"] == "returned", row.get("error")
        e = row["extra"]
        assert [p["index"] for p in e["receive_prefixes"]] == [8, 6, 1]
        assert all(p["whole_application_ram_checked"] and p["admitted"] for p in e["receive_prefixes"])
        assert e["receive_callbacks"] == ["0x1c10e", "0x1c20a", "0x1c264"]
        dispatch, watchdog = e["receive_boundaries"]
        assert dispatch["entry"] == "0x1bd10" and watchdog["entry"] == "0x19af0"
        assert dispatch["after"]["pending"] == 0 and dispatch["after"]["bitmap"] == [0, 0]
        predicted = watchdog_state_model(watchdog["before"])
        for field in ["deadlines", "fresh", "faults"]:
            assert watchdog["after"][field] == predicted["expected_"+field]
        d = e["after_diagnostic"]
        assert d["0x84d0"] == 100*(call+1)
        assert d["0xa936"] == 1 and d["0xa939"] == int(call >= 24)
        assert d["0x8ee2"] == 0x2785
        bs = e["diagnostic_boundaries"]
        diag = [b["entry"] for b in bs if b["entry"] not in ["0x1a598", "0x56b06"]]
        assert diag == ["0x56658", "0x57f50", "0x570f6", "0x57258", "0x56f80"]
        gates = [b for b in bs if b["entry"] == "0x56b06"]
        assert len(gates) == int(call % 4 == 0)
        assert all(b["whole_application_ram_checked"] for b in gates)
        calls = [b for b in bs if b["entry"] == "0x1a598" and b["arguments"][0] == 1]
        assert [b["arguments"][1] for b in calls] == [0x36, 0x37, 0x38]
        counts.update(b["entry"] for b in bs)
        if baseline:
            assert d["0x9415"] == int(call >= 4)
            assert d["0xa76c"] == d["0xa722"] == 0
            assert d["0xa978"] == d["0xa98e"] == 1
            assert d["0x80e8"] == 10240 and d["0x9454"] == 1
        else:
            # Native pulse clears in phase0 at36, after this task's producer.
            # The next producer starts500 ticks of enabled CAN200 absence.
            assert d["0x9415"] == int(4 <= call < 36)
            assert d["0xa76c"] == (0 if call < 37 else 1 if call < 42 else 7)
            assert d["0xa722"] == (0 if call < 42 else 4)
            assert d["0xa978"] == d["0xa98e"] == (1 if call < 42 else 0x1C)
            assert bool(d["0x92c9"] & 0x40) == (call >= 44)
            assert d["0x80e8"] == (10240 if call < 46 else 20480)
            assert d["0x9454"] == int(call < 46)
        assert bool(e["wire"]["payload"][7] & 0x20) == bool(d["0x9454"])
        assert row["acks"] == [b["arguments"] for b in row["ack_checks"]]
        keys = ["0x9415", "0xa939", "0xa76c", "0xa722", "0xa978", "0xa98e",
                "0x92c9", "0x80e8", "0x9454"]
        state = {k: d[k] for k in keys}
        if state != prior:
            transitions.append(dict(call=call, tick=d["0x84d0"], state=state))
            prior = state
    if baseline:
        verify(name, count)
    return dict(task_pairs=count, whole_ram_receive_prefixes=3*count,
                whole_ram_admission_returns=counts["0x56b06"],
                diagnostic_boundary_coverage=dict(counts), transitions=transitions)


def main():
    result = dict(status="PASS", scope=__doc__,
                  baseline=check("tcu-qualified-receive-probe.json", 64, True),
                  wheel8=check("tcu-qualified-receive-wheel8.json", 96))
    (ROOT/"tcu-qualified-receive-verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
