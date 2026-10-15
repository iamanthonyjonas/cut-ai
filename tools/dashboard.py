#!/usr/bin/env python3
"""DASHBOARD : une page qui montre tous tes Reels d'un coup d'oeil, avec leur avancement,
la vidéo finale, le script, la légende et le message privé, prêts à copier.

Usage (depuis le dossier Cut AI) :
    python3 tools/dashboard.py [--ouvrir]

Il écrit dashboard.html à la racine du dossier et l'ouvre avec --ouvrir (double-clic aussi).
Rien n'est envoyé nulle part : la page est un simple fichier local. Relance-le pour la mettre à jour.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lieux import MAISON  # noqa: E402

ETAPES = [("script", "Script"), ("legende", "Légende"), ("derush", "Dérush"),
          ("montage", "Montage"), ("export", "Export"), ("publie", "Publié")]


def lire(p: Path, limite: int = 6000) -> str:
    try:
        return p.read_text(encoding="utf-8")[:limite].strip()
    except OSError:
        return ""


def meta(reel: Path) -> dict:
    try:
        return json.loads((reel / "meta.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def videos_finales(reel: Path) -> list[Path]:
    """Les vidéos finales : tout mp4 de exports/, et dans renders/ seulement les exports de l'app
    (un fichier décrit par <id>.meta.json) ou nommés FINAL : le reste est intermédiaire."""
    trouvees = []
    if (reel / "exports").is_dir():
        trouvees += [p for p in (reel / "exports").glob("*.mp4") if p.is_file()]
    if (reel / "renders").is_dir():
        trouvees += [p for p in (reel / "renders").glob("*.mp4")
                     if p.is_file() and ("FINAL" in p.name.upper() or p.with_suffix(".meta.json").exists())]
    return sorted(trouvees, key=lambda p: p.stat().st_mtime, reverse=True)


def analyser(reel: Path) -> dict:
    m = (meta(reel).get("monteurIa") or {})
    script = lire(reel / "script.md") or lire(reel / "work" / "brief.md")
    publication = lire(reel / "publication.md")
    videos = videos_finales(reel)
    derush = (reel / "derush").is_dir() and any((reel / "derush").glob("*_cuts.json"))
    montage = (reel / "compositions").is_dir() and any((reel / "compositions").glob("*.html"))
    fait = {"script": bool(script), "legende": bool(publication), "derush": derush, "montage": montage,
            "export": bool(videos), "publie": m.get("etat") == "publie"}
    etape = "Idée"
    for cle, nom in ETAPES:
        if fait[cle]:
            etape = nom
    groupe = ("publie" if fait["publie"] else "pret" if fait["export"] else
              "montage" if (fait["derush"] or fait["montage"]) else "tourner")
    return {"nom": reel.name, "sujet": m.get("sujet") or reel.name.split(" · ")[0], "date": m.get("date", ""),
            "fait": fait, "etape": etape, "groupe": groupe, "script": script, "publication": publication,
            "video": videos[0] if videos else None, "dossier": reel}


def prochaine_etape(r: dict) -> tuple[str, str]:
    """Ce qu'il reste à faire sur ce Reel, et la phrase à dire à son IA."""
    f, s = r["fait"], r["sujet"]
    if f["publie"]:
        return "Reel publié ✓", ""
    if f["export"]:
        return "Relis la légende sur la vidéo finale, puis publie", f"J'ai publié le Reel « {s} »."
    if f["derush"] or f["montage"]:
        return "Continuer le montage", f"Continue le montage du Reel « {s} »."
    if f["script"] and f["legende"]:
        return "Tourne avec ton script, puis glisse ta vidéo", "On monte celle-ci."
    if f["script"]:
        return "Écrire la légende", f"Écris la légende et le message privé du Reel « {s} »."
    return "Écrire le script", f"Écris le script du Reel « {s} »."


def produits() -> list[dict]:
    """Les produits complémentaires et leur état (installé si leur skill est dans .claude/skills/)."""
    try:
        catalogue = json.loads((MAISON / "templates" / "produits.json").read_text(encoding="utf-8"))["produits"]
    except (OSError, ValueError, KeyError):
        return []
    return [{**p, "installe": (MAISON / ".claude" / "skills" / p["skill"] / "SKILL.md").is_file()} for p in catalogue]


def carte_produit(p: dict) -> str:
    e = html.escape
    if p["installe"]:
        etat = '<span class="badge publie">Installé</span>'
        action = f'<button class="copy" type="button" data-copy="{e(p.get("essai", ""))}">Copier une phrase d\'essai</button>'
    elif p.get("bientot"):
        etat, action = '<span class="badge">Bientôt</span>', ""
    else:
        etat = '<span class="badge pret">À installer</span>'
        action = (f'<p class="how">Récupère le dossier dans ta formation, puis dis à ton IA :</p>'
                  f'<button class="copy" type="button" data-copy="{e(p["phrase"])}">Copier : « {e(p["phrase"])} »</button>')
    return (f'<article class="prod"><div class="top"><h3>{e(p["nom"])}</h3>{etat}</div>'
            f'<p>{e(p["pitch"])}</p>{action}</article>')


def carrousels() -> list[dict]:
    """Les carrousels de carrousels/<nom>/ (créés par tools/carrousel.py)."""
    base = MAISON / "carrousels"
    out = []
    for d in sorted(base.iterdir()) if base.is_dir() else []:
        if not d.is_dir() or d.name.startswith("."):
            continue
        slides = sorted(d.glob("slide-*.png"))
        titre = d.name
        try:
            titre = json.loads((d / "carrousel.json").read_text(encoding="utf-8")).get("titre", d.name) or d.name
        except (OSError, ValueError):
            pass
        out.append({"nom": d.name, "titre": titre, "slides": slides, "legende": lire(d / "legende.md"),
                    "pdf": (d / "carrousel.pdf") if (d / "carrousel.pdf").is_file() else None, "dossier": d})
    return out


def carte_carrousel(c: dict) -> str:
    e = html.escape
    if c["slides"]:
        vignettes = "".join(f'<img src="{lien(s)}" alt="Slide {i}" loading="lazy">' for i, s in enumerate(c["slides"], 1))
        media = f'<div class="strip">{vignettes}</div>'
        etape = "Prêt" if c["legende"] else "Légende à écrire"
        phrase = "" if c["legende"] else f"Écris la légende du carrousel « {c['titre']} »."
    else:
        media = '<div class="novideo">Pas encore d\'images</div>'
        etape, phrase = "À rendre", f"Rends le carrousel « {c['titre']} »."
    bouton = (f'<button class="next copy" type="button" data-copy="{e(phrase)}">{e(etape)}<small>Copier la phrase pour ton IA</small></button>'
              if phrase else f'<div class="next done">{e(etape)}</div>')
    leg = (f'<details><summary>Légende</summary><pre>{e(c["legende"])}</pre><button class="copy" type="button">Copier</button></details>'
           if c["legende"] else "")
    pdf = f'<a class="lien" href="{lien(c["pdf"])}">Ouvrir le PDF</a>' if c["pdf"] else ""
    return (f'<article class="card carou">{media}<div class="body"><div class="top"><h3>{e(c["titre"])}</h3>'
            f'<span class="badge">{len(c["slides"])} slides</span></div>{bouton}{leg}{pdf}</div></article>')


def section_carrousels() -> str:
    cs = carrousels()
    if not cs:
        return ""
    return ('<div class="wrap"><h2 class="sect">Mes carrousels</h2><div class="grille">' + "".join(carte_carrousel(c) for c in cs) + "</div></div>")


def charte() -> str:
    try:
        return (MAISON / "templates" / "cut-brand.css").read_text(encoding="utf-8")
    except OSError:
        return ""


def logo(nom: str) -> str:
    """Logo Cut AI en données intégrées : la page marche d'où qu'on l'ouvre."""
    try:
        return "data:image/svg+xml;base64," + base64.b64encode((MAISON / "assets" / "cut" / nom).read_bytes()).decode()
    except OSError:
        return ""


def lien(p: Path) -> str:
    return "/".join(quote(part) for part in p.relative_to(MAISON).parts)


def carte(r: dict) -> str:
    e = html.escape
    pas = "".join(f'<li class="{"on" if r["fait"][c] else ""}">{n}</li>' for c, n in ETAPES)
    video = (f'<video controls preload="metadata" playsinline src="{lien(r["video"])}"></video>'
             if r["video"] else '<div class="novideo">Pas encore de vidéo exportée</div>')
    blocs = ""
    if r["script"]:
        blocs += f'<details><summary>Script</summary><pre>{e(r["script"])}</pre></details>'
    if r["publication"]:
        blocs += (f'<details><summary>Légende et message privé</summary><pre>{e(r["publication"])}</pre>'
                  f'<button class="copy" type="button">Copier</button></details>')
    texte, phrase = prochaine_etape(r)
    suite = (f'<button class="next copy" type="button" data-copy="{e(phrase)}">{e(texte)}'
             f'<small>Copier la phrase pour ton IA</small></button>' if phrase else f'<div class="next done">{e(texte)}</div>')
    return (f'<article class="card" data-g="{r["groupe"]}" data-t="{e((r["sujet"] + " " + r["nom"]).lower())}">'
            f'<div class="media">{video}</div><div class="body">'
            f'<div class="top"><h3>{e(r["sujet"])}</h3><span class="badge {r["groupe"]}">{e(r["etape"])}</span></div>'
            f'<div class="date">{e(r["date"])}</div><ol class="pas">{pas}</ol>{suite}{blocs}</div></article>')


PAGE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard Cut AI</title>
<style>
/*CUT_BRAND*/
*,*::before,*::after{box-sizing:border-box}html{overflow-x:hidden}body{margin:0;line-height:1.5;overflow-wrap:anywhere}img{max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 var(--space-4)}
header.hd{padding-block:var(--space-6) var(--space-2)}header.hd img.logo{height:26px;width:auto;display:block;margin-bottom:var(--space-5)}
h1{font-family:var(--font-display);font-weight:600;letter-spacing:-0.045em;line-height:1.04;font-size:clamp(34px,5vw,56px);margin:0 0 var(--space-3)}
.sub{color:var(--ink-2);margin:0 0 var(--space-4);font-size:17px;max-width:70ch}
.lane{max-width:420px;margin-bottom:var(--space-3)}
.bar{display:flex;gap:var(--space-2);flex-wrap:wrap;align-items:center;padding-block:var(--space-3) var(--space-5)}
.tab{font:inherit;font-size:14px;border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);border-radius:var(--radius-pill);padding:7px 16px;cursor:pointer}
.tab[aria-pressed=true]{background:var(--ink);color:var(--canvas);border-color:var(--ink)}.tab:focus-visible,.next:focus-visible,.copy:focus-visible,summary:focus-visible{outline:2px solid var(--focus);outline-offset:3px}
input[type=search]{font:inherit;font-size:15px;flex:1;min-width:180px;border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);border-radius:var(--radius-pill);padding:9px 18px}
input[type=search]:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
main{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:var(--space-5);padding-bottom:var(--space-7)}
.card{background:var(--surface);border-radius:var(--radius-md);box-shadow:var(--shadow-card);overflow:hidden;display:flex;flex-direction:column}
.media{background:#0b0a07;aspect-ratio:9/12;display:grid;place-items:center}.media video{width:100%;height:100%;object-fit:contain}
.novideo{color:#8d8678;font-size:14px;padding:20px;text-align:center}
.body{padding:var(--space-4) var(--space-5) var(--space-5)}.top{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
h3{margin:0;font-family:var(--font-display);font-weight:600;font-size:19px;letter-spacing:-0.02em;line-height:1.25}.date{margin:2px 0 var(--space-3)}
.badge{font-size:12px;font-weight:600;border-radius:var(--radius-pill);padding:4px 11px;white-space:nowrap;background:var(--surface-2);color:var(--ink);border:1px solid var(--line-strong)}
.badge.publie,.badge.pret{background:var(--ink);color:var(--canvas);border-color:var(--ink)}
.pas{list-style:none;display:flex;gap:4px;padding:0;margin:0 0 var(--space-3)}.pas li{flex:1;text-align:center;font-family:var(--font-code);font-size:10px;padding:6px 0;border-radius:6px;background:var(--surface-2);color:var(--ink-3);text-transform:uppercase;letter-spacing:.02em}
.pas li.on{background:var(--ink);color:var(--canvas)}
.next{display:block;width:100%;text-align:left;font-family:var(--font-display);font-size:15px;font-weight:600;border:1px solid var(--line-strong);background:var(--surface-2);color:var(--ink);border-radius:var(--radius-sm);padding:10px 14px;margin:0 0 var(--space-2);cursor:pointer}
.next small{display:block;font-family:var(--font-text);font-weight:400;color:var(--ink-3);font-size:12px;margin-top:2px}.next.done{cursor:default;color:var(--ink-3)}
details{border-top:1px solid var(--line);padding:var(--space-2) 0}summary{cursor:pointer;font-weight:600;font-size:14px}
pre{white-space:pre-wrap;font:13px/1.5 var(--font-code);background:var(--surface-2);border-radius:var(--radius-sm);padding:var(--space-3);margin:var(--space-2) 0;max-height:240px;overflow:auto}
.copy{font:inherit;font-size:14px;font-weight:600;border:1px solid var(--line-strong);border-radius:var(--radius-pill);padding:8px 16px;background:var(--surface);color:var(--ink);cursor:pointer}
h2.sect{font-family:var(--font-display);font-weight:600;letter-spacing:-0.035em;font-size:32px;margin:var(--space-7) 0 var(--space-4)}
.prods{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--space-5);padding-bottom:var(--space-8)}
.prod{background:var(--surface);border-radius:var(--radius-md);box-shadow:var(--shadow-card);padding:var(--space-5)}.prod p{color:var(--ink-2);font-size:15px;margin:var(--space-2) 0 var(--space-4)}.prod .how{margin:0 0 6px;font-size:13px;color:var(--ink-3)}
.prod .copy{width:100%;text-align:left;border-radius:var(--radius-sm)}
.strip{display:flex;gap:6px;overflow-x:auto;padding:var(--space-3);background:#0b0a07;scroll-snap-type:x mandatory}.strip img{height:260px;width:auto;border-radius:8px;flex:none;scroll-snap-align:start}
.lien{display:inline-block;margin-top:var(--space-2);font-size:14px;font-weight:600;color:var(--ink);text-underline-offset:3px}
.grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:var(--space-5)}
.vide{grid-column:1/-1;text-align:center;color:var(--ink-3);padding:60px 20px}
footer.sig{padding-block:var(--space-5) var(--space-8)}footer.sig img{width:140px;height:auto;display:block}
</style></style></head><body class="cut-page cut-grid">
<header class="hd wrap"><picture><source media="(prefers-color-scheme: dark)" srcset="__LOGO_BLANC__"><img class="logo" src="__LOGO__" alt="Cut AI"></picture><h1>Tes <span class="cut-em">Reels</span></h1><p class="sub">__RESUME__</p><div class="cut-lane lane" aria-hidden="true"><i style="left:4%;width:30%"></i><i style="left:38%;width:18%"></i><i style="left:60%;width:28%"></i><span class="cut-playhead cut-playhead--run"></span></div></header>
<div class="bar wrap"><input type="search" id="q" placeholder="Chercher un Reel">
<button class="tab" data-g="tous" aria-pressed="true">Tous (__N__)</button>
<button class="tab" data-g="tourner" aria-pressed="false">À tourner</button>
<button class="tab" data-g="montage" aria-pressed="false">En montage</button>
<button class="tab" data-g="pret" aria-pressed="false">Prêts à publier</button>
<button class="tab" data-g="publie" aria-pressed="false">Publiés</button></div>
<main id="grid" class="wrap">__CARTES__</main>
__CARROUSELS__<div class="wrap"><h2 class="sect">Mes produits</h2><div class="prods">__PRODUITS__</div></div>
<footer class="sig wrap"><picture><source media="(prefers-color-scheme: dark)" srcset="__ECS_BLANC__"><img src="__ECS__" alt="L'Écosystème"></picture></footer>
<script>
let g="tous";const cards=[...document.querySelectorAll(".card")];
function f(){const q=document.getElementById("q").value.trim().toLowerCase();let n=0;
cards.forEach(c=>{const ok=(g==="tous"||c.dataset.g===g)&&(!q||c.dataset.t.includes(q));c.style.display=ok?"":"none";if(ok)n++});}
document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>{g=b.dataset.g;document.querySelectorAll(".tab").forEach(x=>x.setAttribute("aria-pressed",x===b));f()}));
document.getElementById("q").addEventListener("input",f);
document.querySelectorAll(".copy").forEach(b=>b.addEventListener("click",async()=>{const t=b.dataset.copy||b.parentElement.querySelector("pre").textContent;
try{await navigator.clipboard.writeText(t)}catch(e){}const o=b.innerHTML;b.textContent="Copié ✓";setTimeout(()=>b.innerHTML=o,2000)}));
</script></body></html>
"""


def main() -> None:
    p = argparse.ArgumentParser(description="Génère dashboard.html : tous tes Reels d'un coup d'oeil.")
    p.add_argument("--ouvrir", action="store_true", help="ouvre la page dans ton navigateur")
    a = p.parse_args()
    dossier = MAISON / "reels"
    reels = [analyser(d) for d in sorted(dossier.iterdir()) if d.is_dir() and not d.name.startswith(".")] if dossier.is_dir() else []
    reels.sort(key=lambda r: (r["date"], r["nom"]), reverse=True)
    n = {g: sum(1 for r in reels if r["groupe"] == g) for g in ("tourner", "montage", "pret", "publie")}
    resume = (f'{len(reels)} Reel(s) : {n["pret"]} prêt(s) à publier, {n["montage"]} en montage, '
              f'{n["tourner"]} à tourner, {n["publie"]} publié(s). Mis à jour le '
              f'{datetime.now().strftime("%d/%m/%Y à %H:%M")}.')
    cartes = "\n".join(carte(r) for r in reels) or '<div class="vide">Aucun Reel pour l\'instant : dis à ton IA « écris mon script » ou glisse ta vidéo.</div>'
    sortie = MAISON / "dashboard.html"
    sortie.write_text(PAGE.replace("/*CUT_BRAND*/", charte()).replace("__LOGO_BLANC__", logo("cut-logo-blanc.svg")).replace("__LOGO__", logo("cut-logo.svg"))
                      .replace("__ECS_BLANC__", logo("lecosysteme-logo-blanc.svg")).replace("__ECS__", logo("lecosysteme-logo.svg"))
                      .replace("__RESUME__", html.escape(resume)).replace("__N__", str(len(reels)))
                      .replace("__CARTES__", cartes).replace("__PRODUITS__", "".join(carte_produit(p) for p in produits()))
                      .replace("__CARROUSELS__", section_carrousels()), encoding="utf-8")
    print(f"✅ {sortie}  ({len(reels)} Reel(s))")
    if a.ouvrir:
        cmd = ["open"] if sys.platform == "darwin" else ["cmd", "/c", "start", ""] if sys.platform == "win32" else ["xdg-open"]
        subprocess.run(cmd + [str(sortie)], check=False)


if __name__ == "__main__":
    main()
