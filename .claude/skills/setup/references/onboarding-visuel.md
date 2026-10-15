# Onboarding visuel : appliquer un bloc `CUTAI-REGLAGES`

Le client a rempli la page `demarrer.html` (prénom, style, sous-titres, cadrage, appel à l'action,
première vidéo) et colle le résultat dans la conversation. Tu appliques tout, sans le questionner
sur ce qu'il a déjà choisi.

## 0. Le message d'accueil (quand tu ouvres la page)

Parle comme un guide qui accueille quelqu'un chez lui : chaleureux, imagé, simple. **Jamais** de nom
de fichier, de code ni de mot technique (« bloc », « config », « JSON », « CUTAI-REGLAGES »). Dis ce
qui se passe, ce que la personne fait, combien de temps, et qu'elle ne peut pas se tromper. Modèle,
à adapter à sa langue et à sa situation (jamais recopié mot pour mot à chaque fois) :

> Ta page de réglages vient de s'ouvrir dans ton navigateur. C'est ton atelier : tu y choisis le look de
> tes Reels, un peu comme tu choisirais la déco d'une pièce.
>
> **À toi, trois minutes :**
> 1. Clique sur ce qui te plaît : ton style, tes couleurs, tes sous-titres. Le téléphone à droite change
>    en direct, tu vois tout de suite ce que ça donne.
> 2. En bas de la page, clique sur **« Copier mes réglages »**.
> 3. Reviens ici, colle (Cmd+V sur Mac, Ctrl+V sous Windows) et envoie.
>
> Je m'occupe du reste. Tu hésites ? Garde ce qui est déjà choisi : ça rend déjà bien, et rien n'est
> définitif, tu pourras tout changer quand tu veux. Et si tu préfères voir une vidéo sortir d'abord,
> dis-le-moi, on commence par là.

Si la page ne s'est pas ouverte, dis-le simplement et propose de l'ouvrir autrement (double-clic sur
`demarrer.html` dans le dossier, ou ton navigateur). Pas de liste de vérifications techniques dans ta réponse.

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
| `visual.accent` (hex), `visual.accent2` (hex, couleur secondaire), `visual.fontDisplay`, `visual.fontCaptions` (noms de polices livrées : Anton, ArchivoBlack, Inter, Teachers) | `visual.accent`, `visual.accent2`, `visual.fontDisplay`, `visual.fontCaptions` : ces valeurs gagnent sur le preset ; `null` = celle du preset. Une police de sous-titres doit être dans `templates/style-presets.json` avec un `measureFile` |
| `visual.captionsSkin` (`soft`, `block`, `outline`, `plate`, `shadow`, `underline`) | `visual.captionsSkin` |
| `montage.defaultLayout` (`split` ou `faceplein`), `montage.layouts` (un ou deux) | `montage.defaultLayout` ; si `layouts` contient les deux, ajoute aussi à `montage.preferences` (après son OK implicite, sans le redemander) : « Alterner écran coupé et plein écran selon les phrases : plein écran pour l'accroche et les phrases fortes, écran coupé quand une animation aide. » |
| `cta.types` (`keyword-dm`, `follow`, `share`, `none`), `defaultKeyword`, `dmTool` | `cta.types`, `cta.defaultKeyword`, `cta.dmTool` |
| `audio.musique` = `mp3` | rien à écrire : demande-lui son MP3 à l'étape musique ; `aucune` = pas de musique |

Puis `setup.styleChosen = true` et ajoute `A`, `C`, `D` à `setup.completedBlocks`. Ne touche pas à
`setup.firstVideoDone`. Lance `node scripts/sync.mjs` et vérifie qu'il ne signale pas d'erreur.

## 3. Confirmer en une ligne

« C'est en place : ton look {nom du style}, tes sous-titres {skin}, {cadrage}. On passe à ta première vidéo ? » Pas de tableau, pas de rappel
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

## 4 bis. Un bloc `CUTAI-SCRIPTS`

S'il est collé (10 à 15 scripts, `### Script n`), c'est le corpus de la voix : suis le bloc B du skill
(`references/voice-extraction.md`). Moins de 10 scripts, ou des scripts qui se ressemblent (même
accroche, même sujet) : dis-le en une phrase et demande d'autres scripts différents ; ne devine pas.

## 5. Règles

- Aucune question sur ce que le bloc contient déjà (style, cadrage, appel à l'action).
- La voix (bloc B) n'est pas demandée dans le chat : elle vient du bloc `CUTAI-SCRIPTS` ou s'apprend au débrief.
- Un bloc collé une seconde fois = il change d'avis : réapplique, confirme en une ligne.
- Ne montre jamais les chemins ni le JSON au client, sauf demande.
