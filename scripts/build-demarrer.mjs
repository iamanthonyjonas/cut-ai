#!/usr/bin/env node
/**
 * build-demarrer.mjs : génère demarrer.html (la page d'accueil visuelle de l'onboarding) à la racine,
 * depuis templates/demarrer.html.tpl et les styles de templates/style-presets.json.
 * Relancé par `npm run demarrer` quand un style change. Node pur, zéro dépendance.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const presets = JSON.parse(fs.readFileSync(path.join(ROOT, "templates", "style-presets.json"), "utf8"));
const premiere = (s) => (s || "").split(/(?<=[.!?])\s/)[0].replace(/\.$/, "");

const PRESETS = presets.presets.map((p) => ({
  id: p.id, label: p.label, short: premiere(p.description).slice(0, 90),
  bg: p.visual.bg, surface: p.visual.surface, text: p.visual.text, accent: p.visual.accent,
  skin: p.visual.captionsSkin || "soft",
}));
const SKINS = Object.fromEntries(Object.entries(presets.captionSkins).filter(([k]) => !k.startsWith("_"))
  .map(([k, v]) => [k, premiere(v).slice(0, 80)]));

const tpl = fs.readFileSync(path.join(ROOT, "templates", "demarrer.html.tpl"), "utf8");
const charte = fs.readFileSync(path.join(ROOT, "templates", "cut-brand.css"), "utf8");
const page = tpl.replace("/*CUT_BRAND*/", () => charte).replace("__PRESETS__", JSON.stringify(PRESETS)).replace("__SKINS__", JSON.stringify(SKINS));
// logos en données intégrées : la page marche d'où qu'on l'ouvre
fs.writeFileSync(path.join(ROOT, "demarrer.html"), page.replace(/assets\/cut\/([\w-]+\.svg)/g, (m, f) => {
  const p = path.join(ROOT, "assets", "cut", f);
  return fs.existsSync(p) ? `data:image/svg+xml;base64,${fs.readFileSync(p).toString("base64")}` : m;
}));
console.log(`demarrer.html généré (${PRESETS.length} styles).`);
