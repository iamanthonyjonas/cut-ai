#!/usr/bin/env node
/**
 * doctor.mjs : le diagnostic. Dit en clair ce qui marche, ce qui manque et quoi faire.
 *
 *   npm run doctor                 (ou : node scripts/doctor.mjs)
 *   npm run doctor -- --partager   résumé anonyme à coller au support
 *
 * Il ne modifie rien. Node pur, zéro dépendance. Code de sortie 1 s'il y a un blocage (❌).
 */
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const WIN = process.platform === "win32";
const lignes = [];
const ajoute = (etat, titre, aide = "") => lignes.push({ etat, titre, aide });

function essaie(cmd, args, options = {}) {
  try {
    return execFileSync(cmd, args, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], timeout: 15000, ...options }).trim();
  } catch {
    return null;
  }
}
const lireJSON = (p) => {
  try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; }
};
const trouver = (nom) => essaie(WIN ? "where" : "which", [nom])?.split(/\r?\n/)[0] || null;

// 1. Node
const major = Number(process.versions.node.split(".")[0]);
major >= 22 ? ajoute("ok", `Node.js ${process.versions.node}`)
  : ajoute("ko", `Node.js ${process.versions.node} (trop ancien)`, "Installe la version LTS depuis https://nodejs.org puis relance.");

// 2. Python + Pillow
const py = [WIN ? "python" : "python3", "py"].find((c) => essaie(c, ["--version"]));
if (!py) ajoute("ko", "Python introuvable", "Dis à ton IA « installe Python » : c'est elle qui s'en occupe.");
else {
  const v = essaie(py, ["--version"]);
  const pil = essaie(py, ["-c", "import PIL"]) !== null;
  pil ? ajoute("ok", v) : ajoute("warn", `${v}, mais la bibliothèque d'images manque`, `Dis à ton IA « installe Pillow » (commande : ${py} -m pip install --user pillow).`);
}

// 3. FFmpeg
for (const outil of ["ffmpeg", "ffprobe"]) {
  const chemin = trouver(outil);
  chemin ? ajoute("ok", `${outil} trouvé`) : ajoute("ko", `${outil} introuvable`, "Le traitement vidéo en dépend : dis à ton IA « installe ffmpeg ».");
}

// 4. Configuration, transcription
const config = lireJSON(path.join(ROOT, "brand.config.json"));
if (!config) ajoute("warn", "Pas encore de réglages personnels", "Ouvre demarrer.html (double-clic) et colle le résultat à ton IA.");
else {
  const b = config.brand || {};
  b.firstName && b.handle ? ajoute("ok", `Réglages de ${b.firstName} (${b.handle})`)
    : ajoute("warn", "Réglages incomplets (prénom ou @ manquant)", "Ouvre demarrer.html et colle le résultat à ton IA.");
}
const env = (config && config.env) || {};
const whisper = (env.whisperCli && fs.existsSync(env.whisperCli) && env.whisperCli) || trouver("whisper-cli");
whisper ? ajoute("ok", "Transcription (Whisper) trouvée") : ajoute("ko", "Transcription (Whisper) introuvable", "Dis à ton IA « installe la transcription ».");
let modele = env.whisperModel && fs.existsSync(env.whisperModel) ? env.whisperModel : null;
if (!modele) {
  const cache = path.join(os.homedir(), ".cache");
  try {
    for (const d of fs.readdirSync(cache)) {
      const w = path.join(cache, d, "whisper");
      if (fs.existsSync(w)) { const f = fs.readdirSync(w).find((n) => /^ggml-.*\.bin$/.test(n)); if (f) modele = path.join(w, f); }
    }
  } catch { /* pas de cache */ }
}
modele ? ajoute("ok", "Modèle de transcription présent") : ajoute("ko", "Modèle de transcription absent (environ 1,6 Go)", "Dis à ton IA « télécharge le modèle de transcription » (garde ta connexion active).");

// 5. Moteur de montage
fs.existsSync(path.join(ROOT, "node_modules")) ? ajoute("ok", "Moteur de montage installé")
  : ajoute("ko", "Moteur de montage non installé", "Dis à ton IA « fais npm install ».");
const hf = path.join(ROOT, "node_modules", ".bin", WIN ? "hyperframes.cmd" : "hyperframes");
if (fs.existsSync(hf)) {
  const dr = essaie(hf, ["doctor"], { cwd: ROOT, timeout: 60000 });
  dr === null ? ajoute("warn", "Le contrôle HyperFrames n'a pas répondu", "Relance dans une minute, ou dis à ton IA « lance hyperframes doctor ».")
    : /Chrome|chrome/.test(dr) ? ajoute("ok", "Export vidéo (HyperFrames) prêt") : ajoute("warn", "Export vidéo à vérifier", "Dis à ton IA « lance hyperframes doctor et explique-moi ».");
}

// 6. Application HyperFrames (gratuite, Mac et Linux)
if (!WIN) {
  const installee = process.platform === "darwin"
    ? fs.existsSync("/Applications") && fs.readdirSync("/Applications").some((n) => /hyperframes/i.test(n))
    : !!trouver("hyperframes-studio");
  installee ? ajoute("ok", "App HyperFrames installée")
    : ajoute("warn", "App HyperFrames pas encore installée (gratuite)", "Télécharge-la : https://hyperframes.dev/studio");
}

// 7. Agent IA
const agents = ["claude", "codex"].filter((a) => trouver(a));
agents.length ? ajoute("ok", `Agent IA : ${agents.join(" et ")}`) : ajoute("warn", "Agent IA en ligne de commande non détecté", "Pas grave si tu utilises l'application Claude ou ChatGPT.");

// 8. Emplacement du dossier et place disque
const synchro = /(\/|\\)(Documents|Desktop|Bureau|iCloud|OneDrive|Dropbox)(\/|\\)/i.test(ROOT) || /Mobile Documents/.test(ROOT);
synchro ? ajoute("warn", "Dossier dans un espace synchronisé (Documents, Bureau, iCloud, OneDrive)", "Déplace-le dans Vidéos : les montages seront plus rapides.")
  : ajoute("ok", "Emplacement du dossier adapté");
if (!WIN) {
  const df = essaie("df", ["-k", ROOT]);
  const libre = df ? Number(df.split("\n").pop().trim().split(/\s+/)[3]) * 1024 : null;
  if (libre) {
    const go = libre / 1e9;
    go >= 15 ? ajoute("ok", `Place disque : ${Math.round(go)} Go libres`)
      : ajoute(go >= 5 ? "warn" : "ko", `Place disque : ${go.toFixed(1)} Go libres`, "Un Reel demande plusieurs Go : libère de la place.");
  }
}

// 9. Produits complémentaires (affichés seulement s'il y en a un d'installé)
const catalogue = lireJSON(path.join(ROOT, "templates", "produits.json"))?.produits || [];
const installes = catalogue.filter((p) => fs.existsSync(path.join(ROOT, ".claude", "skills", p.skill, "SKILL.md")));
const versionDe = (p) => { try { return fs.readFileSync(path.join(ROOT, ".claude", "skills", p.skill, "VERSION"), "utf8").trim(); } catch { return ""; } };
if (installes.length) ajoute("ok", `Produits installés : ${installes.map((p) => p.nom + (versionDe(p) ? " " + versionDe(p) : "")).join(", ")}`);

// mode « partager » : un résumé sans aucune donnée personnelle (ni nom, ni chemin) à coller au support
const CLES = [[/Node/, "node"], [/Python/, "python"], [/ffmpeg/, "ffmpeg"], [/ffprobe/, "ffprobe"], [/Réglages/, "reglages"],
  [/Transcription/, "transcription"], [/Modèle/, "modele"], [/Moteur/, "moteur"], [/Export vidéo/, "export"],
  [/App HyperFrames/, "app_hyperframes"], [/Agent IA|Agent/, "agent"], [/Dossier|Emplacement/, "emplacement"], [/Place disque/, "disque"]];
if (process.argv.includes("--partager")) {
  const etat = { ok: "ok", warn: "à améliorer", ko: "BLOQUANT" };
  const sortie = [`Diagnostic Cut AI (anonyme) | ${process.platform} ${process.arch} | Node ${process.versions.node}`];
  for (const l of lignes) {
    const cle = CLES.find(([re]) => re.test(l.titre))?.[1];
    if (cle) sortie.push(`${cle}: ${etat[l.etat]}`);
  }
  sortie.push(`produits: ${installes.map((p) => p.id + (versionDe(p) ? " " + versionDe(p) : "")).join(", ") || "aucun"}`);
  console.log("\nCopie ce bloc et colle-le à ton support (il ne contient ni ton nom ni aucun chemin) :\n");
  console.log(sortie.join("\n"));
  process.exit(lignes.some((l) => l.etat === "ko") ? 1 : 0);
}

// affichage
const icone = { ok: "✅", warn: "⚠️ ", ko: "❌" };
console.log("\nDiagnostic Cut AI\n");
for (const l of lignes) console.log(`${icone[l.etat]} ${l.titre}${l.aide ? `\n     → ${l.aide}` : ""}`);
const ko = lignes.filter((l) => l.etat === "ko").length;
const warn = lignes.filter((l) => l.etat === "warn").length;
console.log(ko ? `\n❌ ${ko} point(s) bloquant(s). Dis à ton IA « fais le diagnostic et répare ce qui bloque ».`
  : warn ? `\n✅ Rien ne bloque. ${warn} point(s) à améliorer (voir ⚠️).` : "\n✅ Tout est prêt.");
process.exit(ko ? 1 : 0);
