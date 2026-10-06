"""Read-only verification; run from any directory. Prints JSON, never edits a ROM."""
import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
sys.path.insert(0, str(ROOT))
from src.ecu.checksum import mazda_checksum
from src.ecu.constants import CHECKSUM_TABLE_OFFSET, CHECKSUM_TABLE_END, CHECKSUM_ENTRY_SIZE
from src.ecu.crc_database import CRCDatabase

db = CRCDatabase.from_file(BASE / "sources/romdrop.crc")
results = {}
for name, path, selector, ratios, dfco in [
    ("LFFEEE_AT", ROOT / "examples/LFFEEE-stock.bin", 0xB8296, 0xC1200, 0xCDDD8),
    ("LF9VEB_MT", ROOT / "examples/lf9veb.bin", 0xB858E, 0xC14F8, 0xCD90C),
]:
    data = path.read_bytes()
    cal_id = data[0xB8046:0xB804C]
    normalized = bytearray(data)
    normalized[0xFFB00:0xFFB08] = b"\xff" * 8
    crc = zlib.crc32(normalized[0x2000:]) & 0xFFFFFFFF
    expected_crc = db.get_factory_crc(cal_id)
    entries = []
    for offset in range(CHECKSUM_TABLE_OFFSET, CHECKSUM_TABLE_END, CHECKSUM_ENTRY_SIZE):
        start, end, stored = struct.unpack_from(">III", data, offset)
        if start >= len(data):
            break
        assert start <= end < len(data), (name, offset, start, end)
        calculated = mazda_checksum(data, start, end + 1)
        entries.append({"start": hex(start), "end_inclusive": hex(end),
                        "stored": hex(stored), "calculated": hex(calculated),
                        "passes": stored == calculated})
    values = struct.unpack_from(">7f", data, ratios)
    results[name] = {
        "path": str(path.relative_to(ROOT)), "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "internal_id": cal_id.decode("ascii"),
        "factory_calibration_crc": hex(crc),
        "database_factory_crc": hex(expected_crc) if expected_crc is not None else None,
        "factory_crc_matches": crc == expected_crc,
        "checksum_entries": entries,
        "all_checksums_pass": bool(entries) and all(e["passes"] for e in entries),
        "configuration_selector_address": hex(selector),
        "configuration_selector_value": data[selector],
        "final_drive_address": hex(ratios), "final_drive": values[0],
        "gear_ratios": list(values[1:]),
        "dfco_at_timer_active_address": hex(dfco),
        "dfco_at_timer_active_value": struct.unpack_from(">f", data, dfco)[0],
    }
print(json.dumps(results, indent=2))
