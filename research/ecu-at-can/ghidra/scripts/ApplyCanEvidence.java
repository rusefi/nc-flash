// Import memory context and conservative labels from the paired-ROM evidence.
// Arguments: annotations.tsv
import java.nio.file.*;
import java.util.*;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.*;
import ghidra.program.model.listing.Function;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.SourceType;

public class ApplyCanEvidence extends GhidraScript {
    private Address at(long value) { return toAddr(value); }
    private void defineTable(long start, DataType element, int count) throws Exception {
        Address first = at(start), last = at(start + element.getLength() * count - 1);
        List<Function> mistaken = new ArrayList<>();
        for (Function f : currentProgram.getFunctionManager().getFunctions(first, true)) {
            if (f.getEntryPoint().compareTo(last) > 0) break;
            if (f.getSymbol().getSource() == SourceType.USER_DEFINED)
                throw new IllegalStateException("User function overlaps known table: " + f);
            mistaken.add(f);
        }
        for (Function f : mistaken) removeFunction(f);
        clearListing(first, last);
        createData(first, new ArrayDataType(element, count, element.getLength()));
    }
    @Override public void run() throws Exception {
        String name = currentProgram.getName();
        boolean ecu = name.equals("LFFEEE-stock.bin");
        boolean tcu = name.equals("LFG1TF000.bin");
        if (!ecu && !tcu) throw new IllegalArgumentException("Unexpected image: " + name);
        String expected = ecu
            ? "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"
            : "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6";
        if (!expected.equals(currentProgram.getExecutableSHA256()))
            throw new IllegalArgumentException("Unexpected ROM SHA256");
        long ramStart = ecu ? 0xffff0000L : 0xffff8000L;
        long ramSize = ecu ? 0xc000 : 0x6000;
        if (currentProgram.getMemory().getBlock(at(ramStart)) == null) {
            MemoryBlock ram = currentProgram.getMemory().createUninitializedBlock(
                "Analysis_RAM", at(ramStart), ramSize, false);
            ram.setRead(true); ram.setWrite(true); ram.setExecute(false);
            ram.setComment("Analysis range covering observed RAM references; not a complete hardware memory map.");
        }
        if (tcu) currentProgram.getProgramContext().setValue(
            currentProgram.getRegister("gbr"), at(0x10000), at(0x7ffff),
            java.math.BigInteger.valueOf(0xffff8000L));
        if (tcu && currentProgram.getMemory().getBlock(at(0xffff6000L)) == null) {
            MemoryBlock history = currentProgram.getMemory().createUninitializedBlock(
                "Analysis_Low_RAM", at(0xffff6000L), 0x2000, false);
            history.setRead(true); history.setWrite(true); history.setExecute(false);
            history.setComment("Observed diagnostic list/status references near6188; analysis coverage only, not chip RAM or EEPROM identification.");
        }
        // Known data must not remain as speculative functions from auto-analysis.
        if (ecu) {
            StructureDataType timer = new StructureDataType("Output_TimerChannel", 0);
            timer.add(new PointerDataType(WordDataType.dataType, 4), "down_counter", null);
            timer.add(new PointerDataType(WordDataType.dataType, 4), "compare", null);
            timer.add(WordDataType.dataType, "channel_mask", null);
            timer.add(WordDataType.dataType, "reserved", null);
            defineTable(0x11228, timer, 4);
            defineTable(0x2f370, WordDataType.dataType, 16);
            StructureDataType mode = new StructureDataType("Output_SchedulerMode", 0);
            mode.add(DWordDataType.dataType, "window_max", null);
            mode.add(DWordDataType.dataType, "window_min", null);
            mode.add(new PointerDataType(null, 4), "update_callback", null);
            mode.add(new PointerDataType(null, 4), "admit_callback", null);
            defineTable(0x2f394, mode, 2);
            defineTable(0x2f3b4, DWordDataType.dataType, 4);
            defineTable(0x2f3c4, ByteDataType.dataType, 4);
            defineTable(0x2f3c8, ByteDataType.dataType, 4);
            // Verified float-map descriptors and referenced data, encoding0 only.
            StructureDataType map = new StructureDataType("Model_FloatMap2D", 0);
            map.add(WordDataType.dataType, "x_count", null);
            map.add(WordDataType.dataType, "y_count", null);
            map.add(new PointerDataType(FloatDataType.dataType, 4), "x_axis", null);
            map.add(new PointerDataType(FloatDataType.dataType, 4), "y_axis", null);
            map.add(new PointerDataType(FloatDataType.dataType, 4), "values", null);
            map.add(ByteDataType.dataType, "encoding", "Verified0: float values");
            map.add(new ArrayDataType(ByteDataType.dataType, 3, 1), "reserved", null);
            for (long a : new long[]{0xa223c,0xa2250,0xa2264,0xa22a0,0xa22dc,0xa2318,
                    0xa228c,0xa22c8,0xa2304,0xa2278,0xa22b4,0xa22f0,0xa232c,0xa25cc,0xa25e0}) {
                int nx = getShort(at(a)) & 0xffff, ny = getShort(at(a+2)) & 0xffff;
                long xp = getInt(at(a+4)) & 0xffffffffL, yp = getInt(at(a+8)) & 0xffffffffL;
                long vp = getInt(at(a+12)) & 0xffffffffL;
                defineTable(a, map, 1);
                defineTable(xp, FloatDataType.dataType, nx);
                defineTable(yp, FloatDataType.dataType, ny);
                defineTable(vp, FloatDataType.dataType, nx*ny);
            }
            StructureDataType curve = new StructureDataType("Model_FloatCurve", 0);
            curve.add(WordDataType.dataType, "count", null);
            curve.add(ByteDataType.dataType, "encoding", "Verified0: float values");
            curve.add(ByteDataType.dataType, "reserved", null);
            curve.add(new PointerDataType(FloatDataType.dataType, 4), "axis", null);
            curve.add(new PointerDataType(FloatDataType.dataType, 4), "values", null);
            for (long a : new long[]{0xa2218,0xa2224,0xa2230,0xa2484,0xa2490,0xa36ac,0xa36b8,0xa36c4,0xa36d0,0xa36dc,0xa36e8}) {
                int n = getShort(at(a)) & 0xffff;
                long xp = getInt(at(a+4)) & 0xffffffffL, vp = getInt(at(a+8)) & 0xffffffffL;
                defineTable(a, curve, 1);
                defineTable(xp, FloatDataType.dataType, n);
                defineTable(vp, FloatDataType.dataType, n);
            }
            StructureDataType descriptor = new StructureDataType("CAN_Descriptor", 0);
            descriptor.add(DWordDataType.dataType, "can_id", null);
            descriptor.add(ByteDataType.dataType, "direction", "0 TX, 1 RX");
            descriptor.add(ByteDataType.dataType, "mailbox", null);
            descriptor.add(ByteDataType.dataType, "dlc", null);
            descriptor.add(ByteDataType.dataType, "reserved", null);
            descriptor.add(DWordDataType.dataType, "buffer_address", null);
            descriptor.add(DWordDataType.dataType, "option", null);
            defineTable(0x378cc, descriptor, 9);
            defineTable(0x379cc, descriptor, 8);
        } else {
            // Executed discrete-output slot mask, nominal rows and descriptors.
            defineTable(0x5cce8, ByteDataType.dataType, 11);
            defineTable(0x70014, new ArrayDataType(ByteDataType.dataType, 6, 1), 12);
            defineTable(0x5f7dc, new PointerDataType(null, 4), 15);
            // Executed periodic task phase tables: three independent rows of 8.
            defineTable(0x5cc28, new PointerDataType(null, 4), 8);
            defineTable(0x5cc48, new PointerDataType(null, 4), 8);
            defineTable(0x5cc68, new PointerDataType(null, 4), 8);
            defineTable(0x5c0f0, new PointerDataType(null, 4), 16);
            defineTable(0x5c130, new PointerDataType(null, 4), 16);
            defineTable(0x76cbc, new PointerDataType(null, 4), 26);
            defineTable(0x5d3bc, ByteDataType.dataType, 40);
            defineTable(0x5d3e4, ByteDataType.dataType, 15);
            defineTable(0x5d3f4, new PointerDataType(null, 4), 8);
            defineTable(0x5d414, new PointerDataType(null, 4), 3);
            defineTable(0x5d464, new PointerDataType(null, 4), 4);
            defineTable(0x5d474, ByteDataType.dataType, 12 * 3);
            defineTable(0x70a8a, ByteDataType.dataType, 7 * 5);
            defineTable(0x70aee, WordDataType.dataType, 12);
            defineTable(0x70b14, ByteDataType.dataType, 14);
            defineTable(0x70b22, ByteDataType.dataType, 2);
            defineTable(0x700c8, ByteDataType.dataType, 7 * 11);
            defineTable(0x70000, WordDataType.dataType, 7);
            defineTable(0x70116, WordDataType.dataType, 5);
            defineTable(0x76e20, WordDataType.dataType, 3);
            defineTable(0x5d420, ByteDataType.dataType, 8);
            defineTable(0x5c864, WordDataType.dataType, 5);
            defineTable(0x5c86e, ByteDataType.dataType, 5);
            defineTable(0x5c874, DWordDataType.dataType, 5);
            defineTable(0x5c8c0, WordDataType.dataType, 12);
            defineTable(0x5c8d8, ByteDataType.dataType, 12);
            defineTable(0x5c8e4, ByteDataType.dataType, 12);
            defineTable(0x5c8f0, DWordDataType.dataType, 12);
            StructureDataType validity = new StructureDataType("CAN_ValidityDiagnosticRecord", 0);
            validity.add(new PointerDataType(ByteDataType.dataType, 4), "validity", null);
            validity.add(ByteDataType.dataType, "group", null);
            validity.add(new ArrayDataType(ByteDataType.dataType, 3, 1), "reserved", null);
            defineTable(0x5f198, validity, 5);
            defineTable(0x5dea0, new PointerDataType(null, 4), 3);
            defineTable(0x5e1ac, ByteDataType.dataType, 60);
            defineTable(0x5e1e8, ByteDataType.dataType, 36);
            defineTable(0x75144, ByteDataType.dataType, 17);
            defineTable(0x75155, ByteDataType.dataType, 17);
            defineTable(0x75166, ByteDataType.dataType, 7);
            defineTable(0x5cd1c, ByteDataType.dataType, 13);
            defineTable(0x5c80e, ByteDataType.dataType, 4);
            defineTable(0x5c59c, ByteDataType.dataType, 4);
            defineTable(0x5c826, ByteDataType.dataType, 4);
            defineTable(0x5c5c0, ByteDataType.dataType, 4);
            defineTable(0x70320, ByteDataType.dataType, 7);
            defineTable(0x70327, ByteDataType.dataType, 5);
            defineTable(0x7032c, ByteDataType.dataType, 5);
            defineTable(0x70331, ByteDataType.dataType, 43);
            defineTable(0x7035c, ByteDataType.dataType, 19);
            defineTable(0x7036f, ByteDataType.dataType, 19);
            defineTable(0x70382, ByteDataType.dataType, 31);
            defineTable(0x70b24, ByteDataType.dataType, 9);
            defineTable(0x70b2d, ByteDataType.dataType, 7);
            defineTable(0x70b34, ByteDataType.dataType, 5);
            defineTable(0x70b39, ByteDataType.dataType, 7);
            defineTable(0x70b40, ByteDataType.dataType, 9);
            defineTable(0x70b49, ByteDataType.dataType, 9);
            defineTable(0x5cd0c, ByteDataType.dataType, 5);
            defineTable(0x5fcc0, ByteDataType.dataType, 4);
            defineTable(0x5e418, new PointerDataType(null, 4), 18);
            defineTable(0x763fc, ByteDataType.dataType, 8 * 15);
            defineTable(0x7656c, ByteDataType.dataType, 8 * 50);
            defineTable(0x766fc, ByteDataType.dataType, 5 * 9);
            defineTable(0x5e20c, new PointerDataType(null, 4), 51);
            defineTable(0x5e3f8, ByteDataType.dataType, 32);
            defineTable(0x70a20, ByteDataType.dataType, 7 * 5);
            defineTable(0x76474, ByteDataType.dataType, 16 * 11);
            defineTable(0x76524, ByteDataType.dataType, 8 * 9);
            defineTable(0x5e4cc, new PointerDataType(null, 4), 17);
            defineTable(0x76738, WordDataType.dataType, 5);
            defineTable(0x76805, ByteDataType.dataType, 5 * 50);
            defineTable(0x76913, ByteDataType.dataType, 5 * 9);
            defineTable(0x76742, WordDataType.dataType, 5 * 6);
            defineTable(0x767d8, ByteDataType.dataType, 5 * 9);
            defineTable(0x768ff, ByteDataType.dataType, 5 * 2);
            defineTable(0x76909, ByteDataType.dataType, 5 * 2);
            defineTable(0x773f0, ByteDataType.dataType, 5);
            defineTable(0x7677e, ByteDataType.dataType, 5 * 9);
            defineTable(0x767ab, ByteDataType.dataType, 5 * 9);
            defineTable(0x70a6c, ByteDataType.dataType, 5 * 6);
            defineTable(0x70b06, ByteDataType.dataType, 5 * 2);
            defineTable(0x70b10, ByteDataType.dataType, 2 * 2);
            // Twelve source-policy families, five 48-byte word curves each.
            defineTable(0x7533c, WordDataType.dataType, 12 * 5 * 24);
            defineTable(0x7532c, WordDataType.dataType, 5);
            defineTable(0x75336, ByteDataType.dataType, 5);
            // Four threshold producers and nine banks of ten 48-byte curves.
            defineTable(0x5de90, new PointerDataType(null, 4), 4);
            defineTable(0x73c34, ByteDataType.dataType, 6);
            defineTable(0x73c3a, WordDataType.dataType, 370);
            defineTable(0xffff9b68L, WordDataType.dataType, 60);
            defineTable(0x73f20, ByteDataType.dataType, 3);
            defineTable(0x73f24, WordDataType.dataType, 144);
            defineTable(0x77314, WordDataType.dataType, 8);
            defineTable(0x5deac, WordDataType.dataType, 6);
            defineTable(0x7512c, WordDataType.dataType, 10);
            defineTable(0xffff9c14L, WordDataType.dataType, 30);
            defineTable(0x7404c, WordDataType.dataType, 9 * 10 * 24);
        }
        int count = 0;
        for (String line : Files.readAllLines(Path.of(getScriptArgs()[0]))) {
            if (line.isBlank() || line.startsWith("#")) continue;
            String[] c = line.split("\t", 5);
            if (!c[0].equals(name)) continue;
            Address address = at(Long.parseUnsignedLong(c[2], 16));
            if (c[1].equals("function")) {
                disassemble(address);
                Function f = getFunctionAt(address);
                if (f == null) f = createFunction(address, c[3]);
                if (f == null) throw new IllegalStateException("Cannot create function at " + address);
                f.setName(c[3], SourceType.USER_DEFINED);
            } else {
                createLabel(address, c[3], true, SourceType.USER_DEFINED);
                DataType type = switch(c[1]) {
                    case "u8" -> ByteDataType.dataType;
                    case "u16" -> WordDataType.dataType;
                    case "u32" -> DWordDataType.dataType;
                    case "f32" -> FloatDataType.dataType;
                    default -> null;
                };
                if (type != null && getDataAt(address) == null) createData(address, type);
            }
            setPlateComment(address, c[4]);
            count++;
        }
        println("APPLIED " + name + " labels=" + count + " sha256=" + expected);
    }
}
