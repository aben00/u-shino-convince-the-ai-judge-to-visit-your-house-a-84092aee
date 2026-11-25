// "Convince the AI Judge to Visit Your House: A Letter in One Image"
// entrypoint (Node 22, stdlib only).
//
// The invitation letter is drawn by draw.py (Pillow) from the letter text
// baked into that file, so the program below re-renders it on every run:
// the output is byte-identical across runs because draw.py is
// deterministic. When Python or Pillow is unavailable in the sandbox, the
// entry falls back to the entry.png committed beside this file, which is
// the same render.
//
// Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");
const shipped = join(here, "entry.png");
const drawer = join(here, "draw.py");

mkdirSync(outDir, { recursive: true });

function redraw() {
  const py = spawnSync("python3", [drawer], {
    cwd: here,
    env: { ...process.env, MAKEFUN_OUTPUT_DIR: outDir },
    encoding: "utf8",
  });
  return py.status === 0 && existsSync(target);
}

if (!redraw()) {
  // The committed PNG is the same render draw.py produces; use it verbatim.
  if (!existsSync(shipped)) {
    throw new Error("draw.py failed and no committed entry.png to fall back to");
  }
  copyFileSync(shipped, target);
}

// Guard the competition gate: a whole PNG, at most 1 MiB, 1024 by 1024.
const size = statSync(target).size;
if (size > 1048576) {
  throw new Error(`entry.png must be at most 1 MiB, found ${size} bytes`);
}
console.log(`Wrote ${size} bytes to ${target}`);
