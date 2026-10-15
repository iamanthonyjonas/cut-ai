# Onboarding visuel : appliquer un bloc `CUTAI-REGLAGES`

Le client a rempli la page `demarrer.html` (prénom, style, sous-titres, cadrage, appel à l'action,
première vidéo) et colle le résultat dans la conversation. Tu appliques tout, sans le questionner
sur ce qu'il a déjà choisi.

## 1. Lire le bloc

Il commence par `CUTAI-REGLAGES v1`, suivi d'un JSON. Trop abîmé pour être lu : demande-lui de le
recopier depuis la page (bouton « Copier mes réglages »). Une valeur `null` ou absente = non
renseignée : ne l'écris pas et ne la redemande pas.

## 2. Écrire `brand.config.json`

Crée-le depuis `brand.config.example.json` s'il manque ; sinon fusionne : les valeurs du bloc
remplacent les anciennes (c'est un choix explicite), tout le reste est gardé.

| Dans le bloc | Dans `brand.config.json` |
|---|---|
| `brand.firstName`, `name`, `handle` (commence par `@`), `niche`, `language` | `brand.*` ; copie aussi `language` dans `derush.whisperLanguage` |
| `visual.stylePreset` (`neutral`, `midnight`, `pulse`, `forest`, `ink`, `mono`) | `visual.stylePreset` |
| `visual.captionsSkin` (`soft`, `block`, `outline`, `plate`, `shadow`, `underline`) | `visual.captionsSkin` |
| `montage.defaultLayout` (`split` ou `faceplein`) | `montage.defaultLayout` |
| `cta.types` (`keyword-dm`, `follow`, `share`, `none`), `defaultKeyword`, `dmTool` | `cta.types`, `cta.defaultKeyword`, `cta.dmTool` |
| `audio.musique` = `mp3` | rien à écrire : demande-lui son MP3 à l'étape musique ; `aucune` = pas de musique |

Puis `setup.styleChosen = true` et ajoute `A`, `C`, `D` à `setup.completedBlocks`. Ne touche pas à
`setup.firstVideoDone`. Lance `node scripts/sync.mjs` et vérifie qu'il ne signale pas d'erreur.

## 3. Confirmer en une ligne

« C'est réglé : style {nom du style}, sous-titres {skin}, {cadrage}. » Pas de tableau, pas de rappel
des champs. S'il y a un mot-clé : « et ton mot-clé habituel : {MOT} ».

## 4. Enchaîner sur la première vidéo (`premiereVideo.mode`)

- **`script`** (il n'a pas encore tourné). Avec `sujet` : crée le Reel
  (`python3 tools/nouveau_reel.py "<sujet en 2 à 4 mots>" --brief "<sujet complet>"`, avec
  `--ouvrir` s'il travaille dans l'app HyperFrames), charge le skill `reel-script` et écris **le script,
  puis la légende** (et le message privé si le CTA est un mot-clé), dans cet ordre. Range le script dans
  `script.md` du Reel et la légende (+ DM) dans `publication.md`. Sans `sujet` : une seule question,
  « De quoi parle ta première vidéo ? ». Termine par : « Tourne avec ce script. Quand c'est fait, glisse
  ta vidéo ici et dis "on monte celle-ci". »
- **`video`** : « Glisse ta vidéo brute ici et dis "on monte celle-ci". » La première vidéo se monte
  d'une traite (fichier agent, section 🟢), avec **son style et son cadrage** quand ils sont réglés.

## 5. Règles

- Aucune question sur ce que le bloc contient déjà (style, cadrage, appel à l'action).
- La voix (bloc B) n'est pas demandée ici : elle s'apprend au débrief ou sur `/setup voix`.
- Un bloc collé une seconde fois = il change d'avis : réapplique, confirme en une ligne.
- Ne montre jamais les chemins ni le JSON au client, sauf demande.
