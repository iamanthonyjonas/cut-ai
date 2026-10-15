# Style « Apple » : écran partagé blanc, vraies interfaces, 3D douce

Un des styles d'animation proposés. Actif quand `visual.motionStyle = "apple"`. Ces règles
**remplacent** le « fond toujours `var(--brand-bg)` » du §4 du SKILL. Retenu parce qu'il tient bien
sur un visage : du **blanc pur**, de **vraies interfaces** et des **entrées douces en 3D**.

## Mise en page

- **Écran partagé** par défaut (`montage.defaultLayout = "split"`) : panneau motion 1080×920 en
  haut, visage en bas. Cadrage du visage : `montage.splitTransform` (le cadrage d'un iPhone posé
  sur le bureau).
- **Plein visage** seulement pour l'accroche et les phrases fortes (punchlines, transitions
  d'idée), avec des **punch-in** (voir Rythme).
- Contenu à **y ≥ 170 px** dans le panneau, à **≥ 100 px** des bords. La jointure (y=920) accueille
  le sous-titre (`Y_SPLIT = 950`).

## Couleurs et matières (`brand/apple.css`, généré depuis `templates/apple.css`)

Chaque compo charge `brand/apple.css` après `brand/tokens.css`. Le master le charge aussi :
`build_master.py` s'en occupe. Aucune couleur en dur : tout dérive des tokens par `color-mix`.

| Classe / variable | Rôle |
|---|---|
| `.ap-bg` | fond du panneau : blanc qui glisse vers un gris très léger (jamais de crème ni de halo coloré) |
| `.ap-card` | carte / fenêtre blanche, bord 1 px, ombre douce en 3 couches |
| `.ap-floor` | ombre de sol diffuse sous les objets (reculée en 3D, sinon elle traverse les cartes) |
| `--ap-ink` / `-2` / `-3` | texte principal (presque noir) / secondaire / tertiaire |
| `--ap-fill` | gris système clair (bulle iMessage, champ de saisie, case) |
| `--ap-line` | filet fin entre deux lignes |

- **Rayons** très arrondis : 40 à 48 px pour une carte, 20 à 22 px pour une puce, pilule pour un bouton.
- **Bouton principal** : noir (`--ap-ink`) avec texte blanc. Le bouton secondaire est gris
  `--ap-fill`.
- **L'accent orange** ne sert qu'**une fois par moment** : un point, un événement, un anneau. Les
  seules autres couleurs viennent des **vrais logos** (theSVG).
- Police : celle du corps, **Inter** (`visual.fontBody`). Graisse 600 pour les titres, 400 pour le
  texte, `letter-spacing` négatif (-0,3 à -0,8 px). Casse normale, pas de MAJUSCULES.

## Contenu : de vraies interfaces

Chaque idée devient un objet que le spectateur reconnaît :
- fenêtre façon macOS (3 points gris, titre centré) avec un message qui se tape ;
- notifications iOS qui s'empilent (icône d'app, titre, ligne grise, « maintenant ») ;
- semaine Google Agenda (barre de couleur à gauche des événements) ;
- liste Google Tâches qui se coche ;
- champ commentaire Instagram + bouton « Publier », puis notification DM ;
- alerte façon iOS ;
- carrousel de cartes façon Cover Flow : une carte au centre, la précédente pivote sur le côté.

Les contenus montrés (tâches, événements) illustrent **sa** vie à partir de ce qu'il dit. Jamais
de chiffre inventé.

## Mouvement

- **Entrée** = du flou vers le net : `opacity 0→1`, `scale 0.82-0.9→1`, `filter: blur(18-24px)→0`,
  légère bascule 3D (`rotationX` 20-40° ou `rotationY` 24-40° qui se redresse). Durée 0,9-1,2 s,
  ease `expo.out`.
- **Glissement** (carrousel, colonnes, tâches qui vont à leur place) : `power4.inOut`, 0,7-0,8 s.
- **Caméra** : un conteneur `.cam` (avec `transform-style: preserve-3d`) pousse lentement de
  `scale 0.97` à `1.03` sur toute la section (`ease: none`).
- **Jamais de rebond** (`back.out` interdit) ni de secousse. Un mot qui se tape : chaque mot arrive
  du flou (stagger 0,1-0,16 s).
- Une `perspective` de 1500 à 1800 px sur `.stage`.
- Au moins **2-3 temps forts par section**, calés sur les vrais mots (`<cut>_words.json`).

## Rythme : zooms du visage (`tools/zooms.py`, branché dans `build_master.py`)

- `FULL` : en plein visage, une **dérive lente** (`to`, `ease: none`) puis un **punch-in net**
  (`set`, 1,16 → 1,30) sur le mot fort. On respire (`to` vers 1,04, `expo.out`) avant de repartir.
- Split : à chaque entrée, le visage arrive à 1,14 et recule à 1,0 (automatique). `SPLIT_PUNCH` :
  un punch-in sur le mot fort de la section.
- On anime `.zoom-full` / `.zoom-split`, jamais la `<video>`.

## Sous-titres

Skin `soft` (texte blanc, ombre douce), police Inter Black, casse normale (`captionsCase: none`).
Le **mot-clé** de chaque phrase s'écrit `*mot*` dans `MANUAL` de `tools/montage_captions.py` : il
passe en **italique Bodoni** (`visual.fontCaptionsEmphasis`, règle `.cap em`). Un mot-clé par
chunk au plus, pas sur chaque chunk.

## Son

Bruitages riches (voir `sfx-musique.md`) : montée qui finit pile sur la fin de l'accroche,
whoosh à chaque transition (en alternant les variantes), un son sur chaque apparition importante :
notification pour une notif, clavier pour une frappe, petit tic par créneau, clic pour une coche,
ding pour le DM. Contrôle avec `build_sfx.py --probe` : chaque son ≥ +4 dB au-dessus de la musique.

## Colorimétrie

`montage.grade` (filtre ffmpeg, posé par `tools/build_faces.py`) : « chaud ciné » = contraste et
saturation légèrement montés, ombres un peu relevées, peau plus chaude.
