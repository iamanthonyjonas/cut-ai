#!/usr/bin/env node
/** Lance tools/dashboard.py avec le Python de la machine (python3, python ou py selon le système). */
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const candidats = process.platform === "win32" ? ["python", "py"] : ["python3", "python"];
for (const py of candidats) {
  const r = spawnSync(py, [path.join(ROOT, "tools", "dashboard.py"), "--ouvrir", ...process.argv.slice(2)], { stdio: "inherit" });
  if (!r.error) process.exit(r.status ?? 0);
}
console.error("Python est introuvable : dis à ton IA « installe Python ».");
process.exit(1);
