#!/usr/bin/env node
// Runs dictate_test.html in headless Chrome (through shoot.mjs) against a static server on the repository root.
//   node dictate_test.mjs [src ...]     src: module paths relative to acceptance/ (default ../../dhi_orbit/ui/js/dictate.js)
// Prints one JSON line per src and exits 1 if any fails.
import { spawn, execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const port = 9900 + Math.floor(Math.random() * 90);
const srv = spawn("python3", ["-m", "http.server", String(port), "--bind", "127.0.0.1"], { cwd: join(here, "..", ".."), stdio: "ignore" });
const srcs = process.argv.slice(2).length ? process.argv.slice(2) : ["../../dhi_orbit/ui/js/dictate.js"];
const dir = mkdtempSync(join(tmpdir(), "dictate-test-"));
let bad = 0;
try {
  await new Promise((r) => setTimeout(r, 700));
  const specs = srcs.map((s, i) => ({ url: `http://127.0.0.1:${port}/tools/acceptance/dictate_test.html?src=${encodeURIComponent(s)}`, out: join(dir, `${i}.png`),
    width: 800, height: 600, wait: 1500, eval: "window.__result || JSON.stringify({pass:false, error:'no result'})" }));
  writeFileSync(join(dir, "specs.json"), JSON.stringify(specs));
  const lines = execFileSync("node", [join(here, "shoot.mjs"), join(dir, "specs.json")], { encoding: "utf8" }).trim().split("\n");
  for (const l of lines) {
    const r = JSON.parse(l);
    const res = JSON.parse(r.eval);
    if (!res.pass || r.errors.length) bad++;
    console.log(JSON.stringify({ ...res, errors: r.errors }));
  }
} finally { srv.kill(); }
process.exit(bad ? 1 : 0);
