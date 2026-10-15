#!/usr/bin/env python3
"""ZOOMS du visage (punch-in / zoom arriere).

╔══════════════════════════════════════════════════════════════════════════════╗
║ CE FICHIER EST ADAPTE A CHAQUE REEL : remplis FULL et SPLIT_PUNCH.             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Lu par tools/build_master.py : les tweens sont ajoutes a la timeline "main" du master et animent
deux conteneurs autour des <video> visage (jamais la <video> elle-meme) :
  .zoom-full  -> visage plein ecran (sections "face")
  .zoom-split -> visage en bas (sections "split")

Temps ABSOLUS, cales sur les vrais mots (derush/organiser_words.json). Un punch-in = un `set`
(saut de cadre net, comme un jump-cut) ; une derive = un `to` lent. A chaque entree en split, le
visage arrive un peu zoome et recule (zoom arriere) : ca relance le rythme a chaque changement.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sections

ORIGIN_FULL = "50% 38%"    # point fixe du zoom plein ecran (le visage)
ORIGIN_SPLIT = "50% 70%"   # point fixe du zoom en split (le visage, moitie basse)

# (temps, "set"|"to", echelle, duree, ease)
FULL = [
    # Exemple (a remplacer, temps des vrais mots de TON Reel) :
    # (0.00, "set", 1.00, 0, None), (0.00, "to", 1.06, 1.3, "none"),   # derive lente
    # (1.34, "set", 1.18, 0, None),                                     # punch-in sur un mot fort
]

# punch-in sur un mot fort dans les sections split (temps absolus)
SPLIT_PUNCH = {
    # "s4-claude": 16.16,   # id de section split -> instant du punch-in (mot fort)
}


def js():
    out = []
    for t, kind, s, d, ease in FULL:
        if kind == "set":
            out.append(f'tl.set(".zoom-full", {{scale:{s}}}, {t});')
        else:
            out.append(f'tl.to(".zoom-full", {{scale:{s}, duration:{d}, ease:"{ease}"}}, {t});')
    for sec in sections.sections():
        if sec["fmt"] != "split":
            continue
        st, en = sec["start"], sec["end"]
        out.append(f'tl.fromTo(".zoom-split", {{scale:1.14}}, {{scale:1.0, duration:0.6, ease:"expo.out", immediateRender:false}}, {st});')
        p = SPLIT_PUNCH.get(sec["id"])
        if p:
            out.append(f'tl.to(".zoom-split", {{scale:1.04, duration:{round(p - st - 0.6, 3)}, ease:"none"}}, {round(st + 0.6, 3)});')
            out.append(f'tl.set(".zoom-split", {{scale:1.13}}, {p});')
            out.append(f'tl.to(".zoom-split", {{scale:1.17, duration:{round(en - p, 3)}, ease:"none"}}, {p});')
        else:
            out.append(f'tl.to(".zoom-split", {{scale:1.06, duration:{round(en - st - 0.6, 3)}, ease:"none"}}, {round(st + 0.6, 3)});')
    return "\n      ".join(out)


if __name__ == "__main__":
    print(js())
