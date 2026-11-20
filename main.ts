// main.ts — Node 22 entrypoint for the gta6-meme-x-01 entry.
// Its one job: copy POST.json from the repository root into the output
// directory the house gives us ($MAKEFUN_OUTPUT_DIR, /output by default).
const fs = require("node:fs");
const path = require("node:path");

const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const source = path.join(__dirname, "POST.json");
const destination = path.join(outputDir, "POST.json");

fs.mkdirSync(outputDir, { recursive: true });
fs.copyFileSync(source, destination);

console.log(`POST.json copied to ${destination}`);
