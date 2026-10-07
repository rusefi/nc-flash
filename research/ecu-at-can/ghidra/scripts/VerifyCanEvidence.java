// Reopen saved programs read-only, verify labels/comments, export decompilation.
// Arguments: annotations.tsv output-directory [decompile-timeout-seconds]
import java.nio.file.*;
import java.util.*;
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.Symbol;

public class VerifyCanEvidence extends GhidraScript {
    @Override public void run() throws Exception {
        String name = currentProgram.getName();
        int timeout = getScriptArgs().length > 2 ? Integer.parseInt(getScriptArgs()[2]) : 60;
        if (timeout <= 0) throw new IllegalArgumentException("Timeout must be positive");
        Path out = Path.of(getScriptArgs()[1]);
        Files.createDirectories(out);
        List<String> report = new ArrayList<>();
        report.add("program\t" + name);
        report.add("sha256\t" + currentProgram.getExecutableSHA256());
        report.add("language\t" + currentProgram.getLanguageID());
        report.add("functions\t" + currentProgram.getFunctionManager().getFunctionCount());
        DecompInterface decompiler = new DecompInterface();
        decompiler.openProgram(currentProgram);
        int count = 0;
        int incomplete = 0;
        try {
            for (String line : Files.readAllLines(Path.of(getScriptArgs()[0]))) {
                if (line.isBlank() || line.startsWith("#")) continue;
                String[] c = line.split("\t", 5);
                if (!c[0].equals(name)) continue;
                Address a = toAddr(Long.parseUnsignedLong(c[2], 16));
                Symbol s = currentProgram.getSymbolTable().getPrimarySymbol(a);
                String comment = getPlateComment(a);
                if (s == null || !s.getName().equals(c[3]) || !c[4].equals(comment))
                    throw new IllegalStateException("Saved annotation mismatch at " + a);
                report.add(c[2] + "\t" + c[1] + "\t" + s.getName());
                if (c[1].equals("function")) {
                    Function f = getFunctionAt(a);
                    DecompileResults d = decompiler.decompileFunction(f, timeout, monitor);
                    if (d.decompileCompleted()) Files.writeString(
                        out.resolve(name + "__" + c[3] + ".c"),
                        "/* Ghidra analysis output; verify against original SH instructions. */\n"
                        + d.getDecompiledFunction().getC());
                    else {
                        Files.deleteIfExists(out.resolve(name + "__" + c[3] + ".c"));
                        report.add("DECOMPILE_INCOMPLETE\t" + c[3] + "\t" + d.getErrorMessage());
                        incomplete++;
                    }
                }
                count++;
            }
        } finally { decompiler.dispose(); }
        report.add("verified_annotations\t" + count);
        Files.write(out.resolve(name + ".readback.tsv"), report);
        if (incomplete != 0)
            throw new IllegalStateException("Incomplete decompilation exports: " + incomplete);
        println("READBACK_OK " + name + " annotations=" + count);
    }
}
