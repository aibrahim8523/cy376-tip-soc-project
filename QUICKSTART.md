# Quick Reference — Pushing to GitHub

## Your repo will be at:
**`https://github.com/aibrahim8523/cy376-tip-soc-project`**

## The three commands you need to run (one-time):

```bash
cd ~/cy376-tip-soc-project

# 1. Create the empty repo on github.com first, then:
git remote add origin https://github.com/aibrahim8523/cy376-tip-soc-project.git

# 2. Push everything
git push -u origin main
```

## If asked for credentials:

GitHub no longer accepts your account password. Use a **Personal Access Token**:

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name: `CY376 laptop`
4. Expiration: 90 days (or your choice)
5. Scopes: tick only **`repo`**
6. Click **Generate token** → **copy the token immediately** (GitHub shows it only once)
7. When git prompts for password, paste the token

## Future updates:

```bash
cd ~/cy376-tip-soc-project
# Edit your files, then:
git add .
git commit -m "Describe what you changed"
git push
```

## Submission link to send your lecturer:

`https://github.com/aibrahim8523/cy376-tip-soc-project`

or the direct PDF link:

`https://github.com/aibrahim8523/cy376-tip-soc-project/blob/main/report/TIP_Integration_Project.pdf`
