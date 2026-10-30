# Installer et utiliser le skill AI Factory, pas à pas

*English version: [INSTALL.md](INSTALL.md)*

Ce guide s'adresse à tout le monde, y compris aux personnes qui n'ont jamais installé de skill ni utilisé de terminal. Suivez la partie qui correspond à votre situation. Chaque étape indique où cliquer.

Les menus de claude.ai changent de temps en temps. Si un libellé est un peu différent sur votre écran, cherchez le plus proche : l'ordre des étapes reste le même. Les libellés sont donnés en anglais, car l'interface de Claude est souvent en anglais ; s'il est affiché en français chez vous, la traduction est entre parenthèses quand elle est utile.

---

## Sommaire

1. [Ce que vous installez](#1-ce-que-vous-installez)
2. [Quelle partie vous concerne](#2-quelle-partie-vous-concerne)
3. [Télécharger le fichier du skill](#3-télécharger-le-fichier-du-skill)
4. [Offre Team ou Enterprise : ce que fait le propriétaire, une seule fois](#4-offre-team-ou-enterprise--ce-que-fait-le-propriétaire-une-seule-fois)
5. [Offre Pro ou Max : activer l'exécution de code](#5-offre-pro-ou-max--activer-lexécution-de-code)
6. [Ajouter le skill à votre compte](#6-ajouter-le-skill-à-votre-compte)
7. [Vérifier que ça a marché](#7-vérifier-que-ça-a-marché)
8. [L'utiliser dans Claude Code sur le web](#8-lutiliser-dans-claude-code-sur-le-web)
9. [Sur votre téléphone](#9-sur-votre-téléphone)
10. [Les autres façons d'installer](#10-les-autres-façons-dinstaller)
11. [Passer à une nouvelle version](#11-passer-à-une-nouvelle-version)
12. [Le retirer](#12-le-retirer)
13. [En cas de problème](#13-en-cas-de-problème)

---

## 1. Ce que vous installez

Un **skill** est un ensemble d'instructions que Claude charge quand il en a besoin. Celui-ci, nommé **ai-factory**, apprend à Claude à mettre en place une chaîne de travail professionnelle sur un projet logiciel :

- votre code est protégé : rien ne change sur le site en ligne sans avoir été vérifié avant,
- chaque changement est testé automatiquement et relu par une IA,
- une copie de test du site (le **staging**) reçoit chaque changement en premier,
- une personne appuie sur un bouton pour mettre un changement sur le vrai site (la **production**),
- chaque mise en ligne reçoit un numéro daté, et on peut revenir à la précédente en un clic,
- une revue de sécurité tourne chaque nuit.

C'est Claude qui fait le travail. Il ne s'arrête que quand il a besoin de vous : pour un paiement, un droit d'accès, une clé secrète à coller, ou le bouton de mise en production. À chaque fois, il vous dit exactement où cliquer.

Vous installez le skill **une seule fois**. Ensuite, il est disponible dans toutes vos sessions Claude Code.

## 2. Quelle partie vous concerne

| Votre situation | À lire |
|---|---|
| Votre entreprise a une offre Claude **Team** ou **Enterprise**, et **vous êtes propriétaire** (vous gérez l'organisation) | Parties 3, 4, 6, 7, 8 |
| Votre entreprise a une offre Claude **Team** ou **Enterprise**, et **vous êtes membre** (quelqu'un d'autre la gère) | Demandez à votre propriétaire de faire la partie 4 une fois, puis parties 3, 6, 7, 8 |
| Vous payez Claude vous-même (offre **Pro** ou **Max**) | Parties 3, 5, 6, 7, 8 |
| Vous utilisez l'offre **Free** (gratuite) | Claude Code sur le web demande une offre payante (Pro, Max, Team ou Enterprise). Vous pouvez quand même ajouter le skill (parties 3, 5, 6) pour le lire dans une conversation normale, mais il est fait pour Claude Code |
| Vous utilisez Claude Code **dans un terminal** ou dans un éditeur comme VS Code | Partie 10 |

Vous ne savez pas quelle offre vous avez ? Sur claude.ai, cliquez sur votre nom ou vos initiales en bas à gauche. L'offre est indiquée dans le menu, ou dans **Settings** (Paramètres), **Billing** (Facturation).

## 3. Télécharger le fichier du skill

1. Ouvrez https://github.com/vincentsider/ai-factory/releases/latest
2. En bas de la page, sous **Assets**, cliquez sur **ai-factory.zip**. Le fichier arrive sur votre ordinateur, en général dans le dossier **Téléchargements**.
3. **Ne l'ouvrez pas et ne le décompressez pas.** Claude a besoin du fichier zip tel quel.

**Mac et Safari :** Safari décompresse souvent les fichiers téléchargés tout seul. Si votre dossier Téléchargements contient un dossier `ai-factory` au lieu d'un fichier `ai-factory.zip`, faites l'une de ces trois choses :
- téléchargez à nouveau avec Chrome, Edge ou Firefox, ou
- dans Safari, ouvrez **Safari**, **Réglages**, **Général**, décochez **Ouvrir les fichiers « fiables » après téléchargement**, puis téléchargez à nouveau, ou
- dans le Finder, faites un clic droit sur le dossier `ai-factory` et choisissez **Compresser « ai-factory »**. Cela recrée `ai-factory.zip`, avec le bon contenu.

## 4. Offre Team ou Enterprise : ce que fait le propriétaire, une seule fois

Seul un **propriétaire** de l'organisation Claude peut le faire. Cela prend deux minutes et vaut pour tout le monde.

1. Sur claude.ai, cliquez sur votre nom ou vos initiales en bas à gauche, puis **Organization settings** (Paramètres de l'organisation, parfois **Admin settings**).
2. Ouvrez **Plugins & skills**, puis l'onglet **Policy**.
3. Activez **Cloud code execution and file creation** (exécution de code et création de fichiers).
4. Activez **Skills**.
5. Vérifiez que **Claude Code** est autorisé pour vos membres (dans **Organization settings**, **Claude Code**). Avec l'offre Team, il est inclus dans les places des membres.

En option, pour donner le skill à tout le monde d'un coup : dans **Organization settings**, **Skills**, le propriétaire peut ajouter un skill pour toute l'organisation. Les membres le voient alors avec un badge d'équipe et peuvent l'activer ou non. Dans ce cas, les membres peuvent sauter la partie 6.

Si vous êtes membre et que vous ne voyez pas ces menus, c'est normal : envoyez cette partie à votre propriétaire.

## 5. Offre Pro ou Max : activer l'exécution de code

1. Sur claude.ai, cliquez sur votre nom ou vos initiales en bas à gauche, puis **Settings** (Paramètres).
2. Ouvrez **Capabilities** (Fonctionnalités).
3. Activez **Code execution and file creation** (exécution de code et création de fichiers).

## 6. Ajouter le skill à votre compte

1. Sur claude.ai, ouvrez **Customize** (Personnaliser) dans la barre de gauche, puis **Skills**.
2. Cliquez sur le bouton **+**, puis **Create skill**, puis **Upload a skill** (Importer un skill).
3. Choisissez le fichier **ai-factory.zip** dans votre dossier Téléchargements.
4. Attendez quelques secondes. Le skill apparaît dans la liste sous le nom **ai-factory**.
5. Vérifiez que son interrupteur est **activé**.

Le skill appartient à votre propre compte. Chaque personne qui le veut l'ajoute une fois, sauf si le propriétaire l'a ajouté pour toute l'organisation (partie 4).

## 7. Vérifier que ça a marché

- Dans **Customize**, **Skills**, vous voyez **ai-factory**, activé.
- Dans une nouvelle conversation sur claude.ai, demandez : *« Quels skills as-tu ? Est-ce que ai-factory en fait partie ? »* Claude doit répondre oui et le décrire en une phrase.

Sinon, voir la [partie 13](#13-en-cas-de-problème).

## 8. L'utiliser dans Claude Code sur le web

Claude Code sur le web se trouve à l'adresse **https://claude.ai/code**. Il travaille sur le code de votre projet, qui est rangé sur **GitHub**.

### 8.1 La première fois seulement : connecter GitHub

1. Ouvrez https://claude.ai/code
2. Si on vous le demande, cliquez sur **Connect GitHub** et connectez-vous à GitHub.
3. GitHub vous propose d'installer l'application **Claude**. Choisissez où se trouve votre projet :
   - votre compte GitHub personnel, ou
   - l'**organisation** GitHub de votre entreprise. Si le projet a été transféré d'un compte personnel vers l'organisation, il faut choisir l'organisation ici. C'est une raison fréquente pour laquelle un projet n'apparaît pas.
4. Choisissez **Only select repositories** et cochez votre projet, ou **All repositories**.
5. Si GitHub indique que la demande attend une approbation, un propriétaire de l'organisation GitHub l'approuve : sur GitHub, l'organisation, **Settings**, **GitHub Apps**.

### 8.2 Lancer le skill

1. Sur https://claude.ai/code, ouvrez une nouvelle session et choisissez le dépôt de votre projet. Choisissez **un seul dépôt** : certaines protections du skill ne se chargent que si la session ne contient qu'un dépôt.
2. Écrivez :

   ```
   /ai-factory
   ```

   ou, en mots simples : *« Mets en place le pipeline AI Factory sur ce dépôt. »*
3. Claude répond dans la langue dans laquelle vous écrivez.

### 8.3 Ce qui se passe ensuite

- **D'abord**, Claude regarde votre projet sans rien modifier. Il écrit un court rapport : ce qui existe, ce qui manque, ce qu'il propose, et une liste de questions pour vous. Il ouvre une **pull request** avec ce rapport. Une pull request est une proposition de changements que vous pouvez lire avant de l'accepter.
- **Ensuite**, étape par étape, il construit la chaîne. Une pull request par étape.
- **Quand il a besoin de vous**, il s'arrête et vous dit, en mots simples, quoi faire et où cliquer. Par exemple : acheter GitHub Team, coller une clé dans les réglages de GitHub, ou appuyer sur le bouton **Promote to production**.
- **À la fin**, il fait passer un petit changement réel jusqu'à la production, puis revient en arrière, pour prouver que tout marche. Puis il écrit un guide pour votre équipe.

Prévoyez quelques heures pour toute la mise en place. Vous pouvez vous arrêter à tout moment et reprendre plus tard dans la même session : Claude tient un journal dans `docs/cicd/setup-log.md`.

Quelques choses que Claude ne fait jamais, exprès : il ne met jamais le site en ligne lui-même, il n'appuie jamais sur le bouton de mise en production, et il ne vous demande jamais de coller une clé secrète dans la conversation. Les clés secrètes vont dans les réglages de GitHub, où Claude ne peut pas les voir.

## 9. Sur votre téléphone

Dans l'application **Claude** (iPhone ou Android), ouvrez l'onglet **Code**. Vous pouvez suivre une session en cours, répondre aux questions de Claude et en lancer de nouvelles. Le skill y est aussi disponible, car il est rattaché à votre compte.

Pour appuyer sur le bouton de mise en production depuis un téléphone : ouvrez votre projet sur github.com dans le navigateur du téléphone, puis **Actions**, **Promote to production**, **Run workflow**.

## 10. Les autres façons d'installer

### 10.1 Dans un terminal ou un éditeur (Claude Code en ligne de commande, VS Code, JetBrains)

En plugin, ce qui le garde à jour :

```
/plugin marketplace add vincentsider/ai-factory
/plugin install ai-factory@ai-factory
```

Ou en skill personnel, pour tous les projets de cet ordinateur :

```bash
curl -fsSL https://raw.githubusercontent.com/vincentsider/ai-factory/main/install.sh | bash -s -- --user
```

Puis ouvrez Claude Code dans un projet et tapez `/ai-factory`.

### 10.2 Dans un seul dépôt, sans rien importer

Utile si vous ne pouvez pas importer de skill (par exemple si votre organisation n'a pas encore activé les skills). Le skill est alors enregistré dans le projet, et toute personne qui ouvre une session Claude Code dessus en profite.

Dans une session Claude Code sur le dépôt (web ou terminal), écrivez :

> Lance `curl -fsSL https://raw.githubusercontent.com/vincentsider/ai-factory/main/install.sh | bash` et ouvre une pull request qui ajoute `.claude/skills/ai-factory`.

Acceptez la pull request, ouvrez une nouvelle session et tapez `/ai-factory`.

## 11. Passer à une nouvelle version

Les nouvelles versions sont listées sur https://github.com/vincentsider/ai-factory/releases

- **Skill importé (claude.ai) :** téléchargez le nouveau `ai-factory.zip`. Dans **Customize**, **Skills**, ouvrez **ai-factory**, supprimez-le (ou utilisez **Replace** si vous voyez cette option), puis importez le nouveau zip comme à la partie 6.
- **Plugin :** `/plugin marketplace update ai-factory`, puis redémarrez Claude Code.
- **Skill personnel installé avec le script :** relancez la même commande `install.sh --user`.
- **Dans un dépôt :** demandez à Claude de relancer la commande d'installation et d'ouvrir une pull request.

Les projets déjà équipés continuent de fonctionner : le skill ne sert que pendant que Claude met les choses en place ou les modifie.

## 12. Le retirer

- **Skill importé :** **Customize**, **Skills**, **ai-factory**, désactivez-le ou supprimez-le.
- **Plugin :** `/plugin uninstall ai-factory@ai-factory`.
- **Skill personnel :** supprimez le dossier `~/.claude/skills/ai-factory`.
- **Dans un dépôt :** supprimez `.claude/skills/ai-factory` par une pull request.

Retirer le skill n'annule rien dans vos projets. Les contrôles, les boutons et les protections restent, car ils vivent dans les réglages GitHub et les fichiers de chaque projet.

## 13. En cas de problème

| Ce que vous voyez | Que faire |
|---|---|
| Pas de **Skills** dans Customize, ou pas de bouton **Upload a skill** | Team ou Enterprise : le propriétaire n'a pas encore fait la partie 4. Pro ou Max : faites la partie 5. Offre Free : voir la partie 2 |
| « Missing required skill.md file » | Le zip a été décompressé puis mal recompressé, ou ce n'est pas le bon fichier. Téléchargez-le à nouveau (partie 3, lisez la remarque sur Safari) |
| « Skill folder name doesn't match the skill name » | Le dossier à l'intérieur du zip a été renommé. Téléchargez à nouveau le `ai-factory.zip` d'origine, sans rien renommer |
| « ZIP file exceeds size limits » | Vous avez importé un autre fichier. Le bon fichier pèse environ 40 Ko |
| Le skill est importé mais Claude Code ne connaît pas `/ai-factory` | Vérifiez qu'il est activé (partie 7). Ouvrez une **nouvelle** session sur claude.ai/code : les sessions ouvertes avant l'import ne le voient pas. Si ça ne marche toujours pas, utilisez la partie 10.2 |
| Votre projet n'apparaît pas dans claude.ai/code | L'application Claude n'est pas installée sur GitHub là où se trouve le projet. Refaites la partie 8.1 en choisissant l'**organisation** si le projet lui appartient |
| GitHub indique « waiting for approval » | Un propriétaire de l'organisation GitHub approuve l'application Claude : GitHub, l'organisation, **Settings**, **GitHub Apps** |
| Claude dit qu'il ne peut pas changer un réglage GitHub | Normal sur le web. Claude vous dira sur quels boutons cliquer. Certains réglages demandent d'être administrateur du dépôt |
| Claude vous demande d'acheter GitHub Team ou GitHub Pro | Nécessaire pour protéger un projet **privé** sur GitHub. Environ 4 dollars par personne et par mois. Les projets publics n'en ont pas besoin |
| Autre chose | Ouvrez une issue sur https://github.com/vincentsider/ai-factory/issues en décrivant ce que vous voyez. N'y collez jamais de mot de passe ni de clé secrète |
