#!/usr/bin/env python3
"""SONS HEYGEN PAR L'API : la bibliothèque de bruitages HeyGen, hors de l'app HyperFrames.

Dans l'app, l'agent a `find_sound_effect`. Ailleurs (Claude Code, Codex, terminal), cet outil
interroge la même bibliothèque (GET /v3/audio/sounds, type=sound_effects), télécharge les
meilleurs résultats et les mesure : durée, peakOffset (début du fichier -> impact), niveaux.
Le son se pose ensuite comme un son de l'app : un event de tools/build_sfx.py, donc un clip de la
timeline HyperFrames et le bouton Export sort la vidéo complète.

Usage (depuis le dossier du Reel) :
    python3 tools/heygen_sfx.py "fast whoosh transition"          # 3 meilleurs -> assets/heygen/
    python3 tools/heygen_sfx.py "mouse click" -n 5 --min-score 0.6
    python3 tools/heygen_sfx.py "cash register" --chercher         # liste sans télécharger
Depuis la racine du dossier Cut AI : rangé dans assets/sfx/heygen/ (partagé par tous les
Reels, à nommer "heygen/<fichier>" dans EVENTS).

Connexion : celle de HyperFrames (`npx hyperframes auth login`, une fois par ordinateur, dans le
navigateur ; rangée dans ~/.heygen/credentials). Sinon HEYGEN_API_KEY (environnement ou .env du
dossier Cut AI). Jamais affichée. Requête en anglais qui décrit le geste, comme pour find_sound_effect.
Chaque téléchargement est noté dans sons-heygen.json (même dossier) : requête, score, mesures.
"""
from __future__ import annotations

import argparse
import array
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lieux import MAISON, REEL

API = (os.environ.get("HEYGEN_API_URL") or "https://api.heygen.com").rstrip("/") + "/v3/audio/sounds"
TAUX = 48000   # mesures en 48 kHz (en 16 kHz, les aigus disparaissent : sfx-musique.md)


def die(msg):
    print("ERREUR :", msg)
    sys.exit(1)


def _env_fichier() -> str | None:
    for dossier in filter(None, (REEL, MAISON)):
        env = dossier / ".env"
        if env.is_file():
            for ligne in env.read_text(encoding="utf-8").splitlines():
                m = re.match(r"\s*(?:export\s+)?HEYGEN_API_KEY\s*=\s*(.*)$", ligne)
                if m and m.group(1).strip().strip("'\""):
                    return m.group(1).strip().strip("'\"")
    return None


def _store() -> dict:
    """~/.heygen/credentials, écrit par `hyperframes auth login` (partagé avec heygen-cli)."""
    p = pathlib.Path(os.environ.get("HEYGEN_CONFIG_DIR") or pathlib.Path.home() / ".heygen") / "credentials"
    try:
        brut = p.read_text(encoding="utf-8").strip()
    except OSError:
        return {}
    if brut.startswith("{"):
        try:
            return json.loads(brut)
        except ValueError:
            die(f"{p} illisible : relance npx hyperframes auth login.")
    return {"api_key": brut} if brut else {}


def _expire(oauth: dict) -> bool:
    try:
        fin = datetime.fromisoformat(str(oauth.get("expires_at", "")).replace("Z", "+00:00"))
    except ValueError:
        return False
    return fin - timedelta(seconds=60) < datetime.now(timezone.utc)


def entetes() -> dict:
    """Mêmes règles que `hyperframes auth` : HEYGEN_API_KEY, HYPERFRAMES_API_KEY, puis la connexion
    HyperFrames (OAuth, renouvelée si elle a expiré), puis HEYGEN_API_KEY d'un .env. Jamais affichée."""
    source = {"X-HeyGen-Client-Source": "hyperframes"}
    cle_ = (os.environ.get("HEYGEN_API_KEY") or os.environ.get("HYPERFRAMES_API_KEY") or "").strip()
    if cle_:
        return {"x-api-key": cle_, **source}
    store = _store()
    oauth = store.get("oauth") or {}
    if oauth.get("access_token") and _expire(oauth) and oauth.get("refresh_token"):
        subprocess.run(["npx", "--no-install", "hyperframes", "auth", "refresh"], cwd=MAISON,
                       capture_output=True, shell=(os.name == "nt"))
        oauth = _store().get("oauth") or {}
    if oauth.get("access_token") and not _expire(oauth):
        return {"authorization": f"Bearer {oauth['access_token']}", "X-HeyGen-Source": "cli", **source}
    if store.get("api_key"):
        return {"x-api-key": store["api_key"], **source}
    if (cle_ := _env_fichier()):
        return {"x-api-key": cle_, **source}
    die("pas connecté à HeyGen. Connecte-toi une fois par HyperFrames (navigateur) : "
        "npx hyperframes auth login" + (" (la connexion a expiré)" if oauth else ""))


def chercher(requete: str, n: int, min_score: float) -> list[dict]:
    params = urllib.parse.urlencode({"query": requete, "type": "sound_effects",
                                     "limit": max(1, min(n, 50)), "min_score": min_score})
    req = urllib.request.Request(f"{API}?{params}", headers={
        **entetes(), "accept": "application/json", "user-agent": "monteur-ia/heygen_sfx"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            page = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            die(f"HeyGen refuse la connexion (HTTP {e.code}) : relance npx hyperframes auth login.")
        die(f"API HeyGen : HTTP {e.code} {e.read()[:300].decode('utf-8', 'replace')}")
    except urllib.error.URLError as e:
        die(f"API HeyGen injoignable ({e.reason}) : vérifie la connexion.")
    return [s for s in page.get("data", []) if s.get("type", "sound_effects") == "sound_effects"][:n]


def slug(texte: str) -> str:
    texte = re.sub(r":\s*\w+$", "", texte or "son")          # « Cinematic Whoosh: 7f2e91ac »
    return re.sub(r"[^a-z0-9]+", "-", texte.lower()).strip("-")[:40] or "son"


def telecharger(url: str, cible: pathlib.Path):
    req = urllib.request.Request(url, headers={"user-agent": "monteur-ia/heygen_sfx"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r, open(cible, "wb") as f:
            f.write(r.read())
    except urllib.error.URLError as e:
        die(f"téléchargement raté ({getattr(e, 'code', '')} {getattr(e, 'reason', e)}) : "
            "les liens HeyGen expirent vite, relance la recherche.")


def mesurer(path: pathlib.Path) -> dict:
    """Durée, peakOffset (échantillon le plus fort), niveaux moyen/max (volumedetect)."""
    brut = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(TAUX),
                           "-f", "s16le", "-"], capture_output=True).stdout
    ech = array.array("h")
    ech.frombytes(brut[: len(brut) // 2 * 2])
    if sys.byteorder == "big":
        ech.byteswap()
    if not ech:
        die(f"son illisible : {path}")
    pic = max(range(len(ech)), key=lambda i: abs(ech[i]))
    # volumedetect logue en info : surtout pas -v error (CLAUDE.md, checklist dérush)
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-ar", str(TAUX), "-af", "volumedetect",
                          "-f", "null", "-"], capture_output=True, encoding="utf-8", errors="replace").stderr
    db = lambda cle_: float(m.group(1)) if (m := re.search(rf"{cle_}:\s*(-?[\d.]+) dB", log)) else None
    return {"duration": round(len(ech) / TAUX, 3), "peakOffset": round(pic / TAUX, 3),
            "meanDb": db("mean_volume"), "maxDb": db("max_volume")}


def main():
    ap = argparse.ArgumentParser(description="Bruitages HeyGen par l'API -> assets du Reel.")
    ap.add_argument("requete", help="description en anglais du geste (« fast whoosh transition »)")
    ap.add_argument("-n", type=int, default=3, help="nombre de résultats (défaut 3)")
    ap.add_argument("--min-score", type=float, default=0.5, help="similarité minimale 0-1 (défaut 0.5)")
    ap.add_argument("--chercher", action="store_true", help="lister sans télécharger")
    a = ap.parse_args()

    sons = chercher(a.requete, a.n, a.min_score)
    if not sons:
        die(f"aucun son au-dessus de {a.min_score} pour « {a.requete} » : reformule (anglais, le geste) "
            "ou baisse --min-score.")
    if a.chercher:
        for s in sons:
            print(f"{s.get('score', 0):.2f}  {s.get('duration', 0):>4.1f} s  {s.get('name')}  : {s.get('description', '')}")
        return

    dossier = (REEL / "assets/heygen") if REEL else (MAISON / "assets/sfx/heygen")
    dossier.mkdir(parents=True, exist_ok=True)
    journal_p = dossier / "sons-heygen.json"
    journal = json.loads(journal_p.read_text(encoding="utf-8")) if journal_p.exists() else []
    connus = {e["id"]: e for e in journal}

    for s in sons:
        ext = pathlib.Path(urllib.parse.urlparse(s["audio_url"]).path).suffix or ".wav"
        fichier = dossier / f"{slug(s.get('name'))}-{s['id'][:8]}{ext}"
        if not fichier.exists():
            telecharger(s["audio_url"], fichier)
        m = mesurer(fichier)
        connus[s["id"]] = {"id": s["id"], "file": fichier.name, "name": s.get("name"),
                           "description": s.get("description"), "query": a.requete,
                           "score": s.get("score"), **m}
        ref = (f"assets/heygen/{fichier.name}" if REEL else f"heygen/{fichier.name}")
        print(f"\n✅ {ref}  (score {s.get('score', 0):.2f})\n   {s.get('description', '')}\n"
              f"   durée {m['duration']} s · impact à {m['peakOffset']} s · moyen {m['meanDb']} dB · max {m['maxDb']} dB\n"
              f"   EVENTS : (\"{ref}\", <instant_visé> - {m['peakOffset']}, <volume_dB>, <trim|None>)")

    journal_p.write_text(json.dumps(list(connus.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nNoté dans {journal_p.relative_to(MAISON)}. Sons non calibrés : volume à régler par niveau perçu "
          "(--probe de build_sfx.py), queue longue à rogner avec trim.")


if __name__ == "__main__":
    main()
