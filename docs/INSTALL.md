# Install and use the AI Factory skill, step by step

*Version française : [INSTALL.fr.md](INSTALL.fr.md)*

This guide is for everyone, including people who have never installed a skill and never used a terminal. Follow the part that matches you. Each step says where to click.

The menus on claude.ai change from time to time. If a label below is slightly different on your screen, look for the closest one: the order of the steps stays the same.

---

## Contents

1. [What you are installing](#1-what-you-are-installing)
2. [Which part is for you](#2-which-part-is-for-you)
3. [Download the skill file](#3-download-the-skill-file)
4. [Team or Enterprise plan: what the owner does once](#4-team-or-enterprise-plan-what-the-owner-does-once)
5. [Pro or Max plan: turn on code execution](#5-pro-or-max-plan-turn-on-code-execution)
6. [Upload the skill to your account](#6-upload-the-skill-to-your-account)
7. [Check that it worked](#7-check-that-it-worked)
8. [Use it in Claude Code on the web](#8-use-it-in-claude-code-on-the-web)
9. [On your phone](#9-on-your-phone)
10. [Other ways to install](#10-other-ways-to-install)
11. [Update to a new version](#11-update-to-a-new-version)
12. [Remove it](#12-remove-it)
13. [Something went wrong](#13-something-went-wrong)

---

## 1. What you are installing

A **skill** is a set of instructions that Claude loads when it needs them. This one, called **ai-factory**, teaches Claude how to set up a professional work chain on a software project:

- your code is protected: nothing changes the live site without being checked first,
- every change is tested automatically, and reviewed by an AI,
- a test copy of the site (called **staging**) gets each change first,
- a person presses a button to put a change on the real site (called **production**),
- every release gets a dated number, and you can go back to the previous one in one click,
- a security review runs every night.

Claude does the work. It only stops when it needs you: to pay for something, to give an access right, to paste a secret key, or to press the production button. Each time, it tells you exactly where to click.

You install the skill **once**. After that, it is available in every Claude Code session you open.

## 2. Which part is for you

| Your situation | Read |
|---|---|
| Your company uses a Claude **Team** or **Enterprise** plan, and **you are an owner** (you manage the organisation) | Parts 3, 4, 6, 7, 8 |
| Your company uses a Claude **Team** or **Enterprise** plan, and **you are a member** (someone else manages it) | Ask your owner to do part 4 once, then parts 3, 6, 7, 8 |
| You pay for Claude yourself (**Pro** or **Max** plan) | Parts 3, 5, 6, 7, 8 |
| You use the **Free** plan | Claude Code on the web needs a paid plan (Pro, Max, Team or Enterprise). You can still upload the skill (parts 3, 5, 6) to read it in a normal chat, but it is made for Claude Code |
| You use Claude Code **in a terminal** or in an editor such as VS Code | Part 10 |

Not sure which plan you have? On claude.ai, click your name or initials at the bottom left. The plan is shown in the menu, or in **Settings**, **Billing**.

## 3. Download the skill file

1. Open https://github.com/vincentsider/ai-factory/releases/latest
2. At the bottom of the page, under **Assets**, click **ai-factory.zip**. The file downloads to your computer, usually into the **Downloads** folder.
3. **Do not open or unzip it.** Claude needs the zip file exactly as it is.

**Mac and Safari:** Safari often unzips downloaded files automatically. If your Downloads folder shows a folder called `ai-factory` instead of a file called `ai-factory.zip`, do one of these:
- download again with Chrome, Edge or Firefox, or
- in Safari, open **Safari**, **Settings**, **General**, untick **Open "safe" files after downloading**, then download again, or
- right-click the `ai-factory` folder in Finder and choose **Compress "ai-factory"**. This creates `ai-factory.zip` again, with the right content.

## 4. Team or Enterprise plan: what the owner does once

Only an **owner** of the Claude organisation can do this. It takes two minutes and is done once for everyone.

1. On claude.ai, click your name or initials at the bottom left, then **Organization settings** (sometimes called **Admin settings**).
2. Open **Plugins & skills**, then the **Policy** tab.
3. Turn on **Cloud code execution and file creation**.
4. Turn on **Skills**.
5. Make sure **Claude Code** is allowed for your members (in **Organization settings**, **Claude Code**). On Team plans it is included in members' seats.

Optional, for owners who want to give the skill to everyone at once: in **Organization settings**, **Skills**, you can add a skill for the whole organisation. Members then see it with a team badge and can switch it on or off. If you do this, members can skip part 6.

If you are a member and you do not see these menus, that is normal: send this part to your owner.

## 5. Pro or Max plan: turn on code execution

1. On claude.ai, click your name or initials at the bottom left, then **Settings**.
2. Open **Capabilities**.
3. Turn on **Code execution and file creation**.

## 6. Upload the skill to your account

1. On claude.ai, open **Customize** in the left sidebar, then **Skills**.
2. Click the **+** button, then **Create skill**, then **Upload a skill**.
3. Choose the file **ai-factory.zip** from your Downloads folder.
4. Wait a few seconds. The skill appears in your list with the name **ai-factory**.
5. Check that its switch is **on**.

The skill belongs to your own account. Each person who wants it uploads it once, unless the owner added it for the whole organisation (part 4).

## 7. Check that it worked

- In **Customize**, **Skills**, you see **ai-factory**, switched on.
- In a new chat on claude.ai, ask: *"Which skills do you have? Is ai-factory one of them?"* Claude should say yes and describe it in one sentence.

If not, see [part 13](#13-something-went-wrong).

## 8. Use it in Claude Code on the web

Claude Code on the web lives at **https://claude.ai/code**. It works on your project's code, which is stored on **GitHub**.

### 8.1 The first time only: connect GitHub

1. Open https://claude.ai/code
2. If asked, click **Connect GitHub** and sign in to GitHub.
3. GitHub asks you to install the **Claude** app. Choose where your project lives:
   - your own GitHub account, or
   - your company's **organisation** on GitHub. If the project was moved from a personal account to the organisation, you must choose the organisation here. This is a common reason why a project does not appear.
4. Choose **Only select repositories** and tick your project, or **All repositories**.
5. If GitHub says the request is waiting for approval, an owner of the GitHub organisation approves it: on GitHub, the organisation, **Settings**, **GitHub Apps**.

### 8.2 Start the skill

1. On https://claude.ai/code, start a new session and pick your project's repository. Pick **only that one repository**: some of the skill's protections only load when the session has a single repository.
2. Type:

   ```
   /ai-factory
   ```

   or, in plain words: *"Mets en place le pipeline AI Factory sur ce dépôt"* (French) or *"Set up the AI Factory pipeline on this repository"* (English).
3. Claude replies in the language you write in.

### 8.3 What happens next

- **First**, Claude looks at your project without changing anything. It writes a short report: what exists, what is missing, what it proposes, and a list of questions for you. It opens a **pull request** with that report. A pull request is a proposal of changes that you can read before accepting it.
- **Then**, phase by phase, it builds the chain. One pull request per phase.
- **When it needs you**, it stops and says, in plain words, what to do and where to click. For example: buy GitHub Team, paste a key in GitHub settings, or press the **Promote to production** button.
- **At the end**, it makes a small real change go all the way to production, then back, to prove everything works. Then it writes a guide for your team.

Plan a few hours for the whole setup. You can stop at any time and continue later in the same session: Claude keeps a log in `docs/cicd/setup-log.md`.

A few things Claude never does, on purpose: it never puts the site online itself, it never presses the production button, and it never asks you to paste a secret key in the chat. Secret keys go into GitHub's settings, where Claude cannot see them.

## 9. On your phone

In the **Claude** app (iPhone or Android), open the **Code** tab. You can follow a running session, answer Claude's questions, and start new ones. The skill is available there too, because it is attached to your account.

To press the production button from a phone: open your project on github.com in the phone's browser, then **Actions**, **Promote to production**, **Run workflow**.

## 10. Other ways to install

### 10.1 In a terminal or an editor (Claude Code CLI, VS Code, JetBrains)

As a plugin, which keeps it updated:

```
/plugin marketplace add vincentsider/ai-factory
/plugin install ai-factory@ai-factory
```

Or as a personal skill for every project on this computer:

```bash
curl -fsSL https://raw.githubusercontent.com/vincentsider/ai-factory/main/install.sh | bash -s -- --user
```

Then open Claude Code in a project and type `/ai-factory`.

### 10.2 Inside one repository, with no upload

Useful when you cannot upload skills (for example your organisation has not turned skills on yet). The skill is then saved inside the project, and anyone who opens a Claude Code session on it gets it.

In a Claude Code session on the repository (web or terminal), write:

> Run `curl -fsSL https://raw.githubusercontent.com/vincentsider/ai-factory/main/install.sh | bash` and open a pull request that adds `.claude/skills/ai-factory`.

Accept the pull request, then start a new session and type `/ai-factory`.

## 11. Update to a new version

New versions are listed at https://github.com/vincentsider/ai-factory/releases

- **Uploaded skill (claude.ai):** download the new `ai-factory.zip`. In **Customize**, **Skills**, open **ai-factory**, delete it (or use **Replace** if you see that option), then upload the new zip as in part 6.
- **Plugin:** `/plugin marketplace update ai-factory`, then restart Claude Code.
- **Personal skill installed with the script:** run the same `install.sh --user` command again.
- **Inside a repository:** ask Claude to run the install command again and open a pull request.

Projects already set up keep working: the skill only matters while Claude sets things up or changes them.

## 12. Remove it

- **Uploaded skill:** **Customize**, **Skills**, **ai-factory**, switch it off or delete it.
- **Plugin:** `/plugin uninstall ai-factory@ai-factory`.
- **Personal skill:** delete the folder `~/.claude/skills/ai-factory`.
- **Inside a repository:** delete `.claude/skills/ai-factory` through a pull request.

Removing the skill does not undo anything in your projects. The checks, the buttons and the protections stay, because they live in each project's GitHub settings and files.

## 13. Something went wrong

| What you see | What to do |
|---|---|
| No **Skills** in Customize, or no **Upload a skill** button | Team or Enterprise: the owner has not done part 4 yet. Pro or Max: do part 5. Free plan: see part 2 |
| "Missing required skill.md file" | The zip was unzipped and re-zipped wrongly, or it is not the right file. Download it again (part 3, read the Safari note) |
| "Skill folder name doesn't match the skill name" | The folder inside the zip was renamed. Download the original `ai-factory.zip` again and do not rename anything |
| "ZIP file exceeds size limits" | You uploaded something else. The right file is about 40 KB |
| The skill is uploaded but Claude Code does not know `/ai-factory` | Check its switch is on (part 7). Start a **new** session on claude.ai/code: sessions opened before the upload do not see it. If it still fails, use part 10.2 |
| Your project does not appear in claude.ai/code | The Claude GitHub app is not installed where the project lives. Redo part 8.1 and choose the **organisation** if the project belongs to one |
| GitHub says "waiting for approval" | An owner of the GitHub organisation approves the Claude app: GitHub, the organisation, **Settings**, **GitHub Apps** |
| Claude says it cannot change a GitHub setting | Normal on the web. Claude will tell you which buttons to click. Some settings need you to be an admin of the repository |
| Claude asks you to buy GitHub Team or GitHub Pro | Needed to protect a **private** project on GitHub. About 4 dollars per person per month. Public projects do not need it |
| Anything else | Open an issue at https://github.com/vincentsider/ai-factory/issues and describe what you see. Never paste a password or a secret key in it |
