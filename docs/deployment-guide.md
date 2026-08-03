# Deploying this project to GitHub

Step-by-step instructions to push the project to your GitHub account so you
can submit the repository URL to your lecturer.

---

## One-time setup (do this once on your laptop)

### 1. Install Git

```bash
# Ubuntu / Debian
sudo apt install -y git

# macOS (with Homebrew)
brew install git

# Windows: download from https://git-scm.com/download/win
```

Verify:

```bash
git --version
```

### 2. Tell Git who you are

Replace with your real name and the email tied to your GitHub account:

```bash
git config --global user.name  "Ibrahim Abdul Aziz"
git config --global user.email "your-github-email@example.com"
git config --global init.defaultBranch main
```

### 3. (Optional) Set up SSH so you don't have to type your password every push

```bash
ssh-keygen -t ed25519 -C "your-github-email@example.com"
# Press Enter at every prompt (default location, no passphrase)
cat ~/.ssh/id_ed25519.pub
# Copy the entire output
```

Then on GitHub: **Settings → SSH and GPG keys → New SSH key** → paste and save.

---

## Creating the GitHub repository

1. Go to https://github.com/new
2. **Repository name:** `cy376-tip-soc-project`
3. **Description:** `Building a TIP integration for a simulated SOC — CY376 Blue Team project`
4. **Public** (lecturer needs to view it)
5. **DO NOT** tick "Add a README file" — we already have one
6. **DO NOT** tick "Add .gitignore" — we already have one
7. Click **Create repository**

GitHub will show a "Quick setup" page with the remote URL. Copy the HTTPS or
SSH URL — for example:

* HTTPS: `https://github.com/aibrahim8523/cy376-tip-soc-project.git`
* SSH:   `git@github.com:aibrahim8523/cy376-tip-soc-project.git`

---

## Pushing the project

From inside the `cy376-tip-soc-project/` folder, run these commands in order:

```bash
# 1. Link your local repo to the GitHub repo you just created
#    (replace the URL with the one you copied)
git remote add origin https://github.com/aibrahim8523/cy376-tip-soc-project.git

# 2. Push the initial commit
git push -u origin main
```

If this is your first push, GitHub will prompt for credentials (username +
[Personal Access Token](https://github.com/settings/tokens) — GitHub no longer
accepts account passwords for `git push` over HTTPS as of August 2021). The
token only needs the `repo` scope.

### If you get `error: failed to push some refs`

The remote has a commit you don't have (e.g. a README from GitHub's
"initialize this repository with a README" option, which you should have
**unchecked**). Fix it with:

```bash
git pull --rebase origin main
git push -u origin main
```

---

## Verifying the deployment

Visit `https://github.com/aibrahim8523/cy376-tip-soc-project` in your browser
and check that:

* [x] `README.md` renders nicely on the repo homepage
* [x] `report/TIP_Integration_Project.pdf` is downloadable from the repo
* [x] All 24 PNGs in `screenshots/` are visible
* [x] The license, configs, and command reference are present
* [x] No `.env` files, secrets, or `.vmdk` files were accidentally pushed
  (the `.gitignore` should prevent this — verify with `git ls-files | grep -E '(\.env|\.vmdk)'`)

---

## Sharing the link with your lecturer

Once the push is successful, give your lecturer the URL:

> `https://github.com/aibrahim8523/cy376-tip-soc-project`

The PDF inside the repo is the main submission artefact:
> `https://github.com/aibrahim8523/cy376-tip-soc-project/blob/main/report/TIP_Integration_Project.pdf`

The latter link is a direct download for the report.
