#!/usr/bin/env python3
"""LUT DOSEE : fabrique une copie d'une LUT .cube melangee a l'identite (le « Mixage » de Final Cut).

Usage (depuis le dossier Cut AI ou un Reel) :
    python3 tools/lut_mix.py <lut.cube> <pourcentage> [sortie.cube]
    python3 tools/lut_mix.py assets/luts/ma-lut.cube 35.69     # -> assets/luts/ma-lut-36.cube

Pourquoi : `lut3d` d'ffmpeg applique une LUT a 100 %. Le melange split + blend marche dans une
commande isolee mais casse dans la chaine de tools/build_faces.py (filtre simple). Melanger la LUT
avec l'identite donne exactement le meme resultat que le curseur « Mixage » de Final Cut, dans un
seul filtre `lut3d=...`.
"""
import pathlib
import sys


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1])
    mix = float(sys.argv[2]) / 100
    out = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else src.with_name(f"{src.stem}-{round(mix * 100)}.cube")
    lines, n, i = [], None, 0
    for l in src.read_text(encoding="utf-8", errors="replace").splitlines():
        t = l.strip()
        parts = t.split()
        if t.startswith("LUT_3D_SIZE"):
            n = int(parts[1])
            lines.append(l)
            continue
        if t.startswith("TITLE"):
            lines.append(f'TITLE "{src.stem} {round(mix * 100)}"')
            continue
        if n and len(parts) == 3:
            try:
                v = [float(x) for x in parts]
            except ValueError:
                lines.append(l)
                continue
            # ordre .cube : rouge varie le plus vite, puis vert, puis bleu
            idn = [(i % n) / (n - 1), ((i // n) % n) / (n - 1), (i // (n * n)) / (n - 1)]
            i += 1
            lines.append(" ".join(f"{a * (1 - mix) + c * mix:.6f}" for a, c in zip(idn, v)))
        else:
            lines.append(l)
    if not n or i != n ** 3:
        sys.exit(f"ERREUR : {src} n'est pas une LUT 3D .cube lisible ({i} valeurs pour une taille {n}).")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{out} : {src.name} a {mix * 100:.2f} % (LUT {n}x{n}x{n})")


if __name__ == "__main__":
    main()
