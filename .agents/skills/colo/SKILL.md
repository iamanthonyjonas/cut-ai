---
name: colo
description: >-
  Colorimétrie du visage d'un Reel : reproduire un look de référence (capture d'un Reel, réglages
  Final Cut, LUT .cube) sur la vidéo du créateur. Use when the user shows a reference color grade
  ("regarde la colo", "même rendu que ça", "mets ma LUT", "plus ciné", "plus chaud", "plus sombre")
  or asks to change the look of his face video. Sortie : un filtre `montage.grade` testé et des
  vidéos du visage regradées par tools/build_faces.py.
---
<!-- Copie générée — éditer .claude/skills/colo/ puis npm run sync -->

# Colorimétrie (look du visage)

La couleur du visage se pose **une seule fois**, au pré-cadrage : `tools/build_faces.py` applique
le filtre ffmpeg de `brand.config.json` → `montage.grade` en fabriquant `visage-split.mp4` et
`visage-plein.mp4`. Les animations ne sont jamais touchées (l'habillage ne filtre jamais le visage,
et la couleur ne filtre jamais l'habillage).

## 1. Partir de la vraie recette, pas d'une imitation

Une capture de Final Cut (« LUT personnalisée », « Mixage ») donne la recette exacte :
- **Chercher la LUT sur le Mac** avant d'imiter quoi que ce soit :
  `mdfind -name "<nom>" | grep -i "\.cube$"` (Final Cut les range dans
  `~/Library/Application Support/ProApps/Custom LUTs/`).
- La copier dans `assets/luts/` du dossier Cut AI (nom court, sans espace ni accent : le
  chemin entre dans un filtre ffmpeg).
- **Mixage < 100 %** → fabriquer la LUT dosée : `python3 tools/lut_mix.py assets/luts/<lut>.cube <pourcentage>`.
  Jamais `split` + `blend` dans `montage.grade` : ça casse dans la chaîne de `build_faces.py`.
- Une LUT à 0 % (ex. `_Basematte` à 0 %) ne fait rien : l'ignorer.
- « Roues des couleurs » (valeurs non visibles sur la capture) → les approcher avec `colorbalance`
  et `curves`, en comparant à la référence (étape 3).

Aucune LUT n'est livrée : dépose la tienne (`.cube`) dans `assets/luts/`.

## 2. Les briques du filtre (ordre conseillé)

| Brique | Rôle | Exemple |
|---|---|---|
| `lut3d=../../assets/luts/x.cube` | le look de base (chemin relatif au Reel) | `ma-lut.cube` |
| `eq=contrast=…:gamma=…` | densité générale | `contrast=1.10:gamma=0.99` |
| `colorbalance=rs/gs/bs (ombres) rm/gm/bm (tons moyens) rh/bh (hautes lumières)` | peau chaude, ombres neutres | `rm=0.07:bm=-0.05` |
| `curves=all='…'` | ombres profondes, hautes lumières douces | `'0/0.02 0.2/0.15 0.5/0.48 0.8/0.82 1/0.95'` |
| `hue=s=…` | calmer les couleurs criardes (casquette, fond) | `s=0.94` |
| `vignette=angle=…` | assombrir les bords, regard au centre | `angle=0.55` |

Pas de `split`, pas d'étiquette `[a][b]` : un seul filtre en chaîne.

## 3. Tester sur une image, comparer, puis seulement regrader

1. Extraire une image du dérush (`derush/<cut>_enhanced.mp4`) et la référence au même format :
   `ffmpeg -ss 20 -i derush/<cut>_enhanced.mp4 -frames:v 1 -update 1 -vf "scale=540:960,<filtre>" work/colo/test.png`
2. Planche côte à côte : `ffmpeg -i ref.png -i actuel.png -i test.png -filter_complex hstack=3 -frames:v 1 -update 1 work/colo/planche.jpg`
   (2-3 variantes au plus). **Regarder la planche** : peau (chaude, pas orange), noirs (profonds,
   pas bouchés), blancs du pull (pas gris), couleurs vives calmées.
3. Écrire le filtre retenu dans `montage.grade`, puis `python3 tools/build_faces.py`. Vérifier une
   image de `assets/video/visage-plein.mp4` contre la planche : elles doivent être identiques.
4. Pas besoin de `build_master.py` (les fichiers du visage gardent leur nom) ; l'export suivant
   prend la nouvelle couleur.

## 4. Pour ce Reel seulement, ou pour toutes les vidéos ?

`montage.grade` est un réglage de la maison, partagé par tous les Reels (et une préférence
apprise : « chaud ciné »). Demander au client :
- **Toutes ses vidéos** → garder le nouveau filtre dans `montage.grade`, mettre à jour la
  préférence « Colorimétrie » de `montage.preferences` après son OK sur la formulation, puis
  `node scripts/sync.mjs`.
- **Ce Reel seulement** → écrire le filtre le temps de `build_faces.py`, puis remettre l'ancienne
  valeur (noter le filtre utilisé dans `work/` du Reel pour pouvoir le refaire).

Une vidéo tournée avec une autre caméra (Sony 25 im/s, iPhone HDR) peut demander d'autres dosages :
toujours tester sur une image du Reel en cours, jamais réappliquer un filtre à l'aveugle.
