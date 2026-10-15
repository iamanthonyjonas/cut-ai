# Composants de tiers

Cut AI s'appuie sur des composants de tiers qui gardent leurs propres licences. Leurs textes sont dans le dossier `licences/`
ou accessibles à l'adresse indiquée. Cette liste ne remplace pas la licence de Cut AI (fichier `LICENSE`).

| Composant | Où | Licence | Source |
|---|---|---|---|
| HyperFrames (CLI et skills : `hyperframes`, `hyperframes-*`, `animejs`, `css-animations`, `lottie`, `three`, `waapi`, `tailwind`, `typegpu`, `media-use`, `motion-doctrine`, `seam-craft`, `cut-the-curve`, `contribute-catalog`, `remotion-to-hyperframes`, `website-to-hyperframes`) | `.claude/skills/`, `skills-avances/`, dépendance npm `hyperframes` | Apache License 2.0 | https://github.com/heygen-com/hyperframes (`licences/Apache-2.0-hyperframes.txt`) |
| Skill `text-to-lottie` | `.claude/skills/text-to-lottie/` | MIT | https://github.com/diffusionstudio/lottie (`licences/MIT-diffusionstudio-lottie.txt`) |
| Skill `thesvg` | `.claude/skills/thesvg/` | MIT | https://github.com/glincker/thesvg (`licences/MIT-glincker-thesvg.txt`) |
| GSAP et CustomEase 3.14 | `assets/vendor/` | Licence standard GreenSock | https://gsap.com/standard-license |
| Polices Inter, Anton, Archivo Black, Bodoni Moda et autres | `assets/fonts/` | SIL Open Font License 1.1 | voir `assets/fonts/LICENSE.md` |
| Sons de démarrage | `assets/sfx/starter/` | CC0 (domaine public) | voir `assets/sfx/starter/README.md` |
| Logos Cut et L'Écosystème | `assets/cut/` | marques de leurs titulaires, usage prévu par la charte Cut | charte graphique Cut |

## Modifications apportées aux composants sous Apache 2.0

Les skills HyperFrames sont livrés tels qu'ils ont été téléchargés (`skills-lock.json` en donne la version et l'empreinte) ;
Cut AI y ajoute ses propres skills et outils à côté, sans les modifier. Certains skills avancés ont été déplacés dans
`skills-avances/` sans changement de contenu.

## Marques

Les noms et logos des services cités (Instagram, TikTok, YouTube, ManyChat, Google, etc.) appartiennent à leurs titulaires.
Cut AI n'est ni affilié ni approuvé par ces services.
