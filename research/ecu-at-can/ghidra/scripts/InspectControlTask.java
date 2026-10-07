// Read-only function-containment evidence for traction task ordering.
// Argument: output TSV. No analysis database mutation.
import java.nio.file.*;
import java.util.*;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;

public class InspectControlTask extends GhidraScript {
    @Override public void run() throws Exception {
        if (!currentProgram.getName().equals("LFFEEE-stock.bin"))
            throw new IllegalArgumentException("Expected ECU image");
        if (!currentProgram.getExecutableSHA256().equals("7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"))
            throw new IllegalArgumentException("Unexpected ROM");
        List<String> lines = new ArrayList<>();
        lines.add("address\tcontaining_entry\tname\tbody_ranges");
        for (long value : new long[]{0x1b14e,0x1693e,0x199bc,0x77f62,0x77f12,0x77f46,0x6cfd8}) {
            Function f = getFunctionContaining(toAddr(value));
            if (f == null) lines.add(Long.toHexString(value)+"\tNONE\t\t");
            else lines.add(Long.toHexString(value)+"\t"+f.getEntryPoint()+"\t"+f.getName()+"\t"+f.getBody());
        }
        Files.write(Paths.get(getScriptArgs()[0]), lines);
        println("CONTROL_TASK_INSPECT_OK " + (lines.size()-1));
    }
}
