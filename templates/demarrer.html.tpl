<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Démarrer avec Cut AI</title>
<style>
/*CUT_BRAND*/
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; overflow-x: hidden; } body { margin: 0; line-height: 1.5; overflow-wrap: anywhere; } img { max-width: 100%; }
.wrap { max-width: 1140px; margin: 0 auto; padding: 0 var(--space-4); }
header.top { padding-block: var(--space-6) var(--space-4); }
header.top img.logo { height: 28px; width: auto; display: block; margin-bottom: var(--space-6); }
h1 { font-family: var(--font-display); font-weight: 600; letter-spacing: -0.045em; line-height: 1.04; font-size: clamp(36px, 6vw, 64px); margin: 12px 0 var(--space-4); }
.sub { font-size: 19px; line-height: 1.55; color: var(--ink-2); max-width: 62ch; margin: 0; }
.steps { display: flex; gap: var(--space-2); margin: var(--space-5) 0 0; flex-wrap: wrap; }
.steps .cut-pill.done { color: var(--ink); } .steps .cut-pill.done::before { content: ""; width: 8px; height: 5px; border-left: 2px solid var(--ink); border-bottom: 2px solid var(--ink); transform: rotate(-45deg) translateY(-1px); }
.layout { display: grid; grid-template-columns: minmax(0, 1fr) 340px; gap: var(--space-7); align-items: start; padding-bottom: var(--space-8); }
@media (max-width: 900px) { .layout { grid-template-columns: 1fr; } .preview { position: static !important; order: -1; } }
section.step { background: var(--surface); border-radius: var(--radius-md); box-shadow: var(--shadow-card); padding: var(--space-5); margin-bottom: var(--space-5); }
section.step h2 { font-family: var(--font-display); font-weight: 600; letter-spacing: -0.035em; font-size: 28px; line-height: 1.12; margin: 0 0 var(--space-2); }
section.step h2 .n { display: inline-grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--ink); color: var(--canvas); font-family: var(--font-code); font-size: 13px; margin-right: 12px; vertical-align: 4px; letter-spacing: 0; }
.hint { color: var(--ink-2); margin: 0 0 var(--space-5); max-width: 65ch; }
label.f { display: block; font-size: 14px; font-weight: 600; color: var(--ink-2); margin: var(--space-4) 0 6px; }
input[type=text], select, textarea { width: 100%; font: inherit; font-size: 16px; color: var(--ink); background: var(--surface-2); border: 1px solid var(--line-strong); border-radius: var(--radius-sm); padding: 12px 14px; }
input:focus-visible, select:focus-visible, textarea:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
input::placeholder, textarea::placeholder { color: var(--ink-3); }
textarea { min-height: 96px; resize: vertical; line-height: 1.5; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); } @media (max-width: 560px) { .row { grid-template-columns: 1fr; } }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: var(--space-3); margin-top: var(--space-2); }
.opt { text-align: left; font: inherit; color: inherit; background: var(--surface-2); border: 1px solid var(--line-strong); border-radius: var(--radius-sm); padding: var(--space-3); cursor: pointer; transition: background-color .15s ease; }
.opt:hover { background: var(--surface); } .opt:focus-visible { outline: 2px solid var(--focus); outline-offset: 3px; }
.opt[aria-pressed=true] { border-color: var(--ink); box-shadow: inset 0 0 0 1px var(--ink); background: var(--surface); }
.opt b { display: block; font-family: var(--font-display); font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }
.opt small { display: block; color: var(--ink-3); font-size: 13px; line-height: 1.35; margin-top: 3px; }
.pv-mini { height: 96px; border-radius: 8px; margin-bottom: 9px; position: relative; overflow: hidden; border: 1px solid var(--line); }
.pv-mini .m { position: absolute; left: 8px; right: 8px; top: 8px; height: 30%; border-radius: 6px; }
.pv-mini .f { position: absolute; left: 0; right: 0; bottom: 0; height: 42%; background: linear-gradient(180deg,#8d7b66,#5b4d3d); }
.pv-mini .c { position: absolute; left: 6px; right: 6px; top: 52%; text-align: center; font-weight: 800; font-size: 10px; line-height: 1.1; }
.pv-mini .c span { padding: 1px 4px; }
.pv-mini .c.block span { background: var(--q-a); color: var(--q-b); }
.pv-mini .c.outline span, .pv-mini .c.soft span { color: var(--q-t); text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000; }
.pv-mini .c.plate span { background: rgba(0,0,0,.62); color: #fff; border-radius: 5px; }
.pv-mini .c.shadow span { color: var(--q-t); text-shadow: 2px 2px 0 var(--q-a); }
.pv-mini .c.underline span { color: var(--q-t); border-bottom: 2px solid var(--q-a); }
.pv-mini .c.soft span { text-shadow: 0 1px 6px rgba(0,0,0,.7); }
.counter { font-family: var(--font-code); font-size: 13px; margin: 8px 0 0; color: var(--ink-2); } .counter.bad { color: #b3261e; } .counter.good { color: var(--ink); font-weight: 700; }
.cost { width: 100%; border-collapse: collapse; font-size: 15px; margin-top: var(--space-3); } .cost th, .cost td { text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--line); vertical-align: top; } .cost th { font-size: 13px; color: var(--ink-3); font-weight: 600; }
.note { font-size: 14px; color: var(--ink-3); margin-top: var(--space-3); }
.hf { display: flex; gap: var(--space-4); align-items: center; flex-wrap: wrap; } .hf a.cut-btn { text-decoration: none; }
.sw { height: 54px; border-radius: 8px; margin-bottom: 9px; display: flex; align-items: flex-end; padding: 6px; gap: 5px; border: 1px solid var(--line); } .sw i { width: 18px; height: 18px; border-radius: 50%; display: block; }
.diag { height: 70px; border-radius: 8px; margin-bottom: 9px; background: var(--line); display: grid; overflow: hidden; }
.diag.split { grid-template-rows: 1fr 1fr; } .diag.split div:first-child { background: var(--ink-3); } .diag.split div:last-child { background: var(--ink); }
.diag.full { background: var(--ink); position: relative; } .diag.full::after { content: ""; position: absolute; left: 12px; right: 12px; top: 10px; height: 14px; border-radius: 4px; background: var(--ink-3); }
.panel { display: none; margin-top: var(--space-3); } .panel.on { display: block; }
.final.cut-slab { padding: var(--space-6); margin-bottom: var(--space-5); }
.final h2 { font-family: var(--font-display); font-weight: 600; letter-spacing: -0.035em; font-size: 28px; margin: 0 0 var(--space-2); color: var(--on-slab); }
.final .hint { color: var(--on-slab-2); }
.final pre { background: rgba(255,255,255,.06); color: var(--on-slab); border-radius: var(--radius-sm); padding: var(--space-4); font-family: var(--font-code); font-size: 13px; overflow: auto; max-height: 260px; margin: var(--space-4) 0; }
.todo { margin: var(--space-5) 0 0; padding-left: 20px; color: var(--on-slab-2); } .todo li { margin: 6px 0; } .todo b { color: var(--on-slab); font-weight: 600; }
.callout { margin-top: var(--space-5); padding: var(--space-4); border-radius: var(--radius-sm); border: 1px dashed var(--on-slab-2); font-size: 15px; color: var(--on-slab); } .callout a { color: var(--on-slab); font-weight: 700; text-underline-offset: 3px; }
.ok { color: var(--on-slab); font-size: 14px; font-weight: 600; display: none; margin-left: 12px; } .ok.on { display: inline; }
.preview { position: sticky; top: var(--space-5); }
.phone { width: 100%; max-width: 300px; margin: 0 auto; aspect-ratio: 9/16; border-radius: 34px; border: 7px solid #0b0a07; overflow: hidden; position: relative; box-shadow: var(--shadow-card); transition: background .25s; }
.phone .handle { position: absolute; top: 34px; left: 18px; font-size: 12px; font-weight: 700; display: flex; align-items: center; gap: 7px; z-index: 3; }
.phone .dot { width: 22px; height: 22px; border-radius: 50%; background: var(--p-accent); }
.phone .motion { z-index: 2; position: absolute; left: 16px; right: 16px; border-radius: 16px; padding: 14px; transition: all .25s; }
.phone .motion .bar { height: 8px; border-radius: 4px; margin: 7px 0; background: var(--p-accent); } .phone .motion .bar.s { width: 60%; opacity: .45; background: var(--p-text); }
.phone .face { position: absolute; left: 0; right: 0; bottom: 0; background: linear-gradient(180deg, #8d7b66, #5b4d3d); transition: all .25s; }
.phone .face::after { content: ""; position: absolute; left: 50%; top: 22%; width: 38%; aspect-ratio: 1; transform: translateX(-50%); border-radius: 50%; background: #d9bfa4; box-shadow: 0 90px 0 40px #b9a083; }
.phone .cap { position: absolute; left: 14px; right: 14px; text-align: center; font-weight: 800; font-size: 19px; line-height: 1.2; z-index: 3; transition: all .25s; }
.phone .cta { position: absolute; left: 50%; transform: translateX(-50%); bottom: 18px; z-index: 4; font-size: 12px; font-weight: 700; padding: 7px 12px; border-radius: 99px; background: var(--p-accent); color: var(--p-bg); white-space: nowrap; }
.cap.block span { background: var(--p-accent); color: var(--p-bg); padding: 2px 8px; }
.cap.outline span { color: var(--p-text); text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000, 0 3px 6px #000; }
.cap.plate span { background: rgba(0,0,0,.62); color: #fff; padding: 4px 12px; border-radius: 12px; }
.cap.shadow span { color: var(--p-text); text-shadow: 3px 3px 0 var(--p-accent); }
.cap.underline span { color: var(--p-text); border-bottom: 4px solid var(--p-accent); padding-bottom: 1px; }
.cap.soft span { color: var(--p-text); text-shadow: 0 2px 14px rgba(0,0,0,.55); font-weight: 800; } .cap.soft em { font-family: "Bodoni 72", "Bodoni MT", Didot, Georgia, serif; font-weight: 600; }
.pcap { text-align: center; color: var(--ink-3); font-size: 13px; margin-top: var(--space-3); }
footer.sig { padding-block: var(--space-6) var(--space-8); } footer.sig img { width: 140px; height: auto; display: block; }
</style>
</head>
<body class="cut-page cut-grid">
<header class="top wrap">
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/cut/cut-logo-blanc.svg"><img class="logo" src="assets/cut/cut-logo.svg" alt="Cut AI"></picture>
  <h1 id="hello">Salut. Faisons ton <span class="cut-em">style</span>.</h1>
  <p class="sub">Quelques étapes, cinq minutes. Tu cliques, tu vois le résultat à côté, et à la fin tu copies tes réglages pour les coller dans ta conversation. Rien ne part sur Internet.</p>
  <nav class="steps" id="nav">
    <a class="cut-pill" href="#s0">0 · HyperFrames</a><a class="cut-pill" href="#s1">1 · Toi</a><a class="cut-pill" href="#s2">2 · Ton style</a>
    <a class="cut-pill" href="#s3">3 · Ton appel à l'action</a><a class="cut-pill" href="#s4">4 · Ta première vidéo</a><a class="cut-pill" href="#s5">5 · Ta voix</a><a class="cut-pill" href="#s6">6 · Consommation</a><a class="cut-pill" href="#fin">Mes réglages</a>
  </nav>
</header>

<main class="layout wrap">
<div>
  <section class="step" id="s0">
    <h2><span class="n">0</span>Installe HyperFrames</h2>
    <p class="hint">C'est l'application gratuite qui te montre ton montage sur une timeline et exporte en un clic (Mac et Linux). Installe-la maintenant : tu en auras besoin pour voir ton Reel.</p>
    <div class="hf"><a class="cut-btn cut-btn--buy" href="https://hyperframes.dev/studio" target="_blank" rel="noopener">Télécharger HyperFrames</a><span class="note" style="margin:0">Déjà installée ? Passe à l'étape 1.</span></div>
  </section>

  <section class="step" id="s1">
    <h2><span class="n">1</span>Qui es-tu ?</h2>
    <p class="hint">Pour personnaliser tes textes, tes sous-titres et tes scripts.</p>
    <div class="row">
      <div><label class="f" for="firstName">Ton prénom</label><input type="text" id="firstName" placeholder="Camille" autocomplete="given-name"></div>
      <div><label class="f" for="handle">Ton @ Instagram</label><input type="text" id="handle" placeholder="@toncompte" autocapitalize="none"></div>
    </div>
    <div class="row">
      <div><label class="f" for="name">Nom de ton compte ou de ta marque</label><input type="text" id="name" placeholder="Ma marque"></div>
      <div><label class="f" for="language">Langue de tes vidéos</label>
        <select id="language"><option value="fr">Français</option><option value="es">Español</option><option value="en">English</option><option value="pt">Português</option><option value="it">Italiano</option><option value="de">Deutsch</option></select></div>
    </div>
    <label class="f" for="niche">Tu parles de quoi ? (quelques mots)</label>
    <input type="text" id="niche" placeholder="marketing, business, mindset…">
  </section>

  <section class="step" id="s2">
    <h2><span class="n">2</span>Ton style</h2>
    <p class="hint">Choisis une ambiance. Tu pourras tout changer plus tard en disant « change mon style ».</p>
    <div class="cards" id="presets"></div>
    <label class="f" style="margin-top:22px">Tes sous-titres</label>
    <div class="cards" id="skins"></div>
    <label class="f" style="margin-top:22px">Ton cadrage</label>
    <div class="cards" id="layouts">
      <button class="opt" data-v="split" aria-pressed="true"><div class="diag split"><div></div><div></div></div><b>Écran coupé</b><small>Toi en bas, l'animation en haut.</small></button>
      <button class="opt" data-v="faceplein" aria-pressed="false"><div class="diag full"></div><b>Toi en plein écran</b><small>Les animations passent par-dessus.</small></button>
    </div>
  </section>

  <section class="step" id="s3">
    <h2><span class="n">3</span>Ton appel à l'action</h2>
    <p class="hint">Comment finis-tu tes Reels ? Plusieurs réponses possibles.</p>
    <div class="cards multi" id="ctas">
      <button class="opt" data-v="keyword-dm" aria-pressed="true"><b>Commenter un mot</b><small>Et recevoir un message privé.</small></button>
      <button class="opt" data-v="follow" aria-pressed="false"><b>M'abonner</b><small>« Abonne-toi pour la suite ».</small></button>
      <button class="opt" data-v="share" aria-pressed="false"><b>Partager</b><small>« Envoie-le à quelqu'un ».</small></button>
      <button class="opt" data-v="none" aria-pressed="false"><b>Aucun</b><small>La phrase finale suffit.</small></button>
    </div>
    <div class="panel on" id="kwPanel">
      <div class="row">
        <div><label class="f" for="keyword">Ton mot-clé habituel (facultatif)</label><input type="text" id="keyword" placeholder="GUIDE"></div>
        <div><label class="f" for="dmTool">Ton outil de messages</label>
          <select id="dmTool"><option value="ManyChat">ManyChat</option><option value="autre">Un autre</option><option value="aucun">Aucun</option></select></div>
      </div>
    </div>
  </section>

  <section class="step" id="s4">
    <h2><span class="n">4</span>Ta première vidéo</h2>
    <p class="hint">Où en es-tu ?</p>
    <div class="cards" id="modes">
      <button class="opt" data-v="script" aria-pressed="true"><b>Je n'ai pas tourné</b><small>Écris-moi mon script, puis ma légende.</small></button>
      <button class="opt" data-v="video" aria-pressed="false"><b>J'ai ma vidéo</b><small>Je la glisse et tu la montes.</small></button>
    </div>
    <div class="panel on" id="topicPanel">
      <label class="f" for="topic">De quoi parle ta première vidéo ?</label>
      <textarea id="topic" placeholder="Une idée, un conseil, une histoire… même en vrac."></textarea>
    </div>
    <label class="f" style="margin-top:18px">Musique</label>
    <div class="cards" id="music">
      <button class="opt" data-v="aucune" aria-pressed="true"><b>Sans musique</b><small>Je l'ajoute dans Instagram.</small></button>
      <button class="opt" data-v="mp3" aria-pressed="false"><b>J'ai un MP3</b><small>Je te le donne plus tard.</small></button>
    </div>
  </section>

  <section class="step" id="s5">
    <h2><span class="n">5</span>Ta voix : 10 à 15 scripts</h2>
    <p class="hint">Pour que ton IA écrive comme toi, colle <b>10 à 15 scripts de Reels déjà faits</b> (le texte que tu dis face caméra). Ils doivent être <b>vraiment différents</b> : des sujets variés, des accroches différentes, pas dix fois la même idée. Sépare-les par une ligne contenant <code>---</code>. Pas encore 10 scripts ? Tu peux sauter cette étape : on affinera ta voix après tes premières vidéos.</p>
    <textarea id="scripts" style="min-height:220px" placeholder="Script 1&#10;---&#10;Script 2&#10;---&#10;…"></textarea>
    <p class="counter" id="scriptsCount">0 script</p>
    <button class="cut-btn" id="copyScripts" type="button" style="margin-top:12px">Copier mes scripts</button>
    <p class="note">À coller dans ta conversation, séparément de tes réglages. Tes scripts restent sur ton ordinateur.</p>
  </section>

  <section class="step" id="s6">
    <h2><span class="n">6</span>Ce que ça consomme</h2>
    <p class="hint">Ton IA travaille avec ton abonnement (Claude ou ChatGPT) : on parle donc de <b>tokens consommés</b>, pas d'une facture en plus. Voici des ordres de grandeur pour t'y repérer.</p>
    <table class="cost">
      <tr><th>Action</th><th>Consommation estimée</th></tr>
      <tr><td>Installation et réglages</td><td>faible (quelques minutes de travail)</td></tr>
      <tr><td>Script + légende</td><td>faible (une conversation courte)</td></tr>
      <tr><td>Premier Reel monté d'une traite (30 à 45 s)</td><td>élevée : compte une bonne part d'une session</td></tr>
      <tr><td>Retouches après le débrief</td><td>moyenne</td></tr>
      <tr><td>Reels suivants</td><td>moyenne : moins que le premier, tes goûts sont connus</td></tr>
    </table>
    <p class="note">Estimations, non mesurées sur ton compte : elles dépendent de la durée de ta vidéo et des retouches. Pour les voir en vrai, demande à ton IA « combien ce Reel a consommé ». Astuce : fais une étape lourde par conversation, et garde tes retouches groupées en un seul message.</p>
  </section>

  <section class="step final cut-slab" id="fin">
    <h2>Tes réglages<span class="ok" id="okmsg">Copié</span></h2>
    <p class="hint">Copie ce bloc et colle-le dans ta conversation avec ton IA (Claude Code ou Codex).</p>
    <pre id="out"></pre>
    <button class="cut-btn cut-btn--buy" id="copy">Copier mes réglages</button>
    <ol class="todo">
      <li><b>Colle</b> le bloc dans ta conversation et envoie (puis, séparément, tes scripts si tu en as 10).</li>
      <li>Ton IA règle ton style, puis <b>écrit ton script et ta légende</b> (ou attend ta vidéo).</li>
      <li>Tu tournes avec le script en main, puis tu glisses ta vidéo : « on monte celle-ci ».</li>
    </ol>
    <div class="callout"><b>L'app HyperFrames est gratuite.</b> Elle montre ton montage sur une timeline et exporte en un clic (Mac et Linux). <a href="https://hyperframes.dev/studio" target="_blank" rel="noopener">Télécharger l'app</a></div>
  </section>
</div>

<aside class="preview" aria-label="Aperçu">
  <div class="phone" id="phone">
    <div class="handle" id="pHandle"><i class="dot"></i><span>@toncompte</span></div>
    <div class="motion" id="pMotion"><div class="bar"></div><div class="bar s"></div><div class="bar s" style="width:40%"></div></div>
    <div class="face" id="pFace"></div>
    <div class="cap soft" id="pCap"><span>Ta phrase <em>forte</em> ici</span></div>
    <div class="cta" id="pCta">Commente GUIDE</div>
  </div>
  <div class="pcap">Aperçu : ton style en direct</div>
</aside>
</main>
<footer class="sig wrap"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/cut/lecosysteme-logo-blanc.svg"><img src="assets/cut/lecosysteme-logo.svg" alt="L'Écosystème"></picture></footer>

<script>
const PRESETS = __PRESETS__;
const SKINS = __SKINS__;
const $ = (s) => document.querySelector(s);
const state = { preset: "neutral", skin: "soft", layout: "split", ctas: ["keyword-dm"], mode: "script", music: "aucune" };
const FIELDS = ["scripts", "firstName", "handle", "name", "language", "niche", "keyword", "dmTool", "topic"];
const SKIN_LABEL = { soft: "Doux", block: "Bloc", outline: "Contour", plate: "Plaque", shadow: "Ombre", underline: "Souligné" };

function save() { try { localStorage.setItem("cutai-demarrer", JSON.stringify({ state, f: Object.fromEntries(FIELDS.map((k) => [k, $("#" + k).value])) })); } catch (e) {} }
function load() {
  try {
    const d = JSON.parse(localStorage.getItem("cutai-demarrer") || "null");
    if (!d) return;
    Object.assign(state, d.state);
    FIELDS.forEach((k) => { if (d.f && d.f[k] != null) $("#" + k).value = d.f[k]; });
  } catch (e) {}
}

function buildCards() {
  $("#presets").innerHTML = PRESETS.map((p) =>
    `<button class="opt" data-v="${p.id}"><div class="pv-mini" style="background:${p.bg};--q-a:${p.accent};--q-b:${p.bg};--q-t:${p.text}"><div class="m" style="background:${p.surface}"></div><div class="f"></div><div class="c ${p.skin}"><span>Ta phrase forte</span></div></div><b>${p.label.replace(/ \(.*\)/, "")}</b><small>${p.short}</small></button>`).join("");
  $("#skins").innerHTML = Object.keys(SKIN_LABEL).map((k) =>
    `<button class="opt" data-v="${k}"><b>${SKIN_LABEL[k]}</b><small>${SKINS[k] || ""}</small></button>`).join("");
}

function pick(groupId, key, multi) {
  const el = $("#" + groupId);
  el.addEventListener("click", (e) => {
    const b = e.target.closest(".opt"); if (!b) return;
    const v = b.dataset.v;
    if (multi) {
      const s = new Set(state[key]);
      if (v === "none") { s.clear(); s.add("none"); } else { s.delete("none"); s.has(v) ? s.delete(v) : s.add(v); }
      state[key] = [...s];
    } else {
      state[key] = v;
      if (key === "preset") state.skin = PRESETS.find((p) => p.id === v).skin;
    }
    refresh();
  });
}

function refresh() {
  const p = PRESETS.find((x) => x.id === state.preset);
  const mark = (id, test) => document.querySelectorAll("#" + id + " .opt").forEach((b) => b.setAttribute("aria-pressed", test(b.dataset.v)));
  mark("presets", (v) => v === state.preset); mark("skins", (v) => v === state.skin); mark("layouts", (v) => v === state.layout);
  mark("ctas", (v) => state.ctas.includes(v)); mark("modes", (v) => v === state.mode); mark("music", (v) => v === state.music);
  $("#kwPanel").classList.toggle("on", state.ctas.includes("keyword-dm"));
  $("#topicPanel").classList.toggle("on", state.mode === "script");
  // aperçu
  const ph = $("#phone"); ph.style.setProperty("--p-bg", p.bg); ph.style.setProperty("--p-accent", p.accent); ph.style.setProperty("--p-text", p.text); ph.style.background = p.bg; ph.style.color = p.text;
  const m = $("#pMotion"), f = $("#pFace"), c = $("#pCap");
  m.style.background = p.surface;
  if (state.layout === "split") { m.style.top = "78px"; m.style.height = "36%"; f.style.top = "52%"; f.style.height = "48%"; c.style.top = "50%"; c.style.transform = "translateY(-50%)"; }
  else { m.style.top = "78px"; m.style.height = "22%"; f.style.top = "0"; f.style.height = "100%"; c.style.top = "66%"; c.style.transform = "none"; }
  c.className = "cap " + state.skin;
  const hh = $("#handle").value.trim(); $("#pHandle span").textContent = hh ? (hh.startsWith("@") ? hh : "@" + hh) : "@toncompte";
  const kw = ($("#keyword").value.trim() || "GUIDE").toUpperCase();
  const cta = state.ctas.includes("keyword-dm") ? "Commente " + kw : state.ctas.includes("follow") ? "Abonne-toi" : state.ctas.includes("share") ? "Partage-le" : "";
  $("#pCta").textContent = cta; $("#pCta").style.display = cta ? "" : "none";
  const fn = $("#firstName").value.trim();
  $("#hello").innerHTML = (fn ? "Salut " + fn.replace(/[<>&]/g, "") + "." : "Salut.") + " Faisons ton <span class=\"cut-em\">style</span>.";
  // pastilles « fait »
  const ok = { s1: $("#firstName").value.trim() && $("#handle").value.trim(), s2: true, s3: state.ctas.length > 0, s4: state.mode === "video" || $("#topic").value.trim(), s0: true, s5: scriptList().length >= 10, s6: true };
  document.querySelectorAll("#nav .cut-pill").forEach((a) => a.classList.toggle("done", !!ok[a.getAttribute("href").slice(1)]));
  scriptsStatus();
  $("#out").textContent = build();
  save();
}

function scriptList() { return $("#scripts").value.split(/^\s*---+\s*$/m).map((x) => x.trim()).filter((x) => x.length > 40); }
function scriptsStatus() {
  const l = scriptList(), n = l.length, seen = new Set(); let dup = 0;
  l.forEach((x) => { const k = x.toLowerCase().replace(/\W+/g, " ").slice(0, 60); if (seen.has(k)) dup++; seen.add(k); });
  const el = $("#scriptsCount");
  let t = n + (n > 1 ? " scripts" : " script"), c = "";
  if (dup) { t += " · " + dup + " début(s) identique(s) : varie les accroches"; c = "bad"; }
  else if (n === 0) t += " · vise 10 à 15, tous différents";
  else if (n < 10) { t += " · encore " + (10 - n) + " pour arriver à 10"; c = "bad"; }
  else if (n > 15) { t += " · 15 suffisent : garde les 15 plus différents"; c = "bad"; }
  else { t += " · parfait"; c = "good"; }
  el.textContent = t; el.className = "counter " + c;
}
function build() {
  let h = $("#handle").value.trim(); if (h && !h.startsWith("@")) h = "@" + h;
  const kw = $("#keyword").value.trim().toUpperCase() || null;
  const data = {
    version: 1,
    brand: { firstName: $("#firstName").value.trim() || null, name: $("#name").value.trim() || null, handle: h || null, niche: $("#niche").value.trim() || null, language: $("#language").value },
    visual: { stylePreset: state.preset, captionsSkin: state.skin },
    montage: { defaultLayout: state.layout },
    cta: { types: state.ctas, defaultKeyword: state.ctas.includes("keyword-dm") ? kw : null, dmTool: state.ctas.includes("keyword-dm") ? $("#dmTool").value : null },
    audio: { musique: state.music },
    premiereVideo: { mode: state.mode, sujet: state.mode === "script" ? ($("#topic").value.trim() || null) : null },
  };
  return "CUTAI-REGLAGES v1\n" + JSON.stringify(data, null, 2);
}

buildCards(); load();
pick("presets", "preset"); pick("skins", "skin"); pick("layouts", "layout"); pick("ctas", "ctas", true); pick("modes", "mode"); pick("music", "music");
FIELDS.forEach((k) => $("#" + k).addEventListener("input", refresh));
$("#copy").addEventListener("click", async () => {
  const t = $("#out").textContent;
  try { await navigator.clipboard.writeText(t); } catch (e) { const r = document.createRange(); r.selectNodeContents($("#out")); const s = getSelection(); s.removeAllRanges(); s.addRange(r); document.execCommand("copy"); }
  $("#okmsg").classList.add("on"); setTimeout(() => $("#okmsg").classList.remove("on"), 2500);
});
$("#copyScripts").addEventListener("click", async () => {
  const t = "CUTAI-SCRIPTS v1\n" + scriptList().map((x, i) => "### Script " + (i + 1) + "\n" + x).join("\n\n");
  try { await navigator.clipboard.writeText(t); } catch (e) { const a = $("#scripts"); a.select(); document.execCommand("copy"); }
  $("#copyScripts").textContent = "Copié"; setTimeout(() => { $("#copyScripts").textContent = "Copier mes scripts"; }, 2500);
});
refresh();
</script>
</body>
</html>
