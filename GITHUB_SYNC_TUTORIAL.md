# GitHub Synchronization Tutorial

Complete step-by-step guide to synchronize your local folder with the GitHub repository.

**Local folder:** `C:\Users\dpolo\Documents\202510-CFE`
**GitHub repository:** `https://github.com/dpolonia/202510-CFE`

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Git installed** - Check with `git --version` in terminal
  - If not installed, download from https://git-scm.com/download/win
- [ ] **GitHub account** with access to `dpolonia/202510-CFE` repository
- [ ] **Repository created** on GitHub (https://github.com/dpolonia/202510-CFE)
- [ ] **Terminal access** (Git Bash, PowerShell, or Command Prompt)

---

## Step 1: Open Terminal in Project Folder

**Option A: Using File Explorer**
1. Navigate to `C:\Users\dpolo\Documents\202510-CFE`
2. Right-click in the folder (not on a file)
3. Select "Git Bash Here" or "Open in Terminal"

**Option B: Using Command Line**
```bash
cd C:\Users\dpolo\Documents\202510-CFE
```

---

## Step 2: Initialize Git Repository (First Time Only)

Check if Git is already initialized:
```bash
git status
```

If you see "fatal: not a git repository", initialize Git:
```bash
git init
```

You should see: `Initialized empty Git repository in C:/Users/dpolo/Documents/202510-CFE/.git/`

---

## Step 3: Configure Git User (First Time Only)

Set your Git identity (use your GitHub email):
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

To verify configuration:
```bash
git config user.name
git config user.email
```

---

## Step 4: Add Remote Repository

Connect your local folder to the GitHub repository:
```bash
git remote add origin https://github.com/dpolonia/202510-CFE.git
```

Verify the remote was added:
```bash
git remote -v
```

You should see:
```
origin  https://github.com/dpolonia/202510-CFE.git (fetch)
origin  https://github.com/dpolonia/202510-CFE.git (push)
```

---

## Step 5: Stage Files for Commit

Check current status:
```bash
git status
```

Add all files (respecting .gitignore):
```bash
git add .
```

Verify what will be committed:
```bash
git status
```

**Important:** You should see files staged for commit, but NOT the `data/` folder (excluded by .gitignore). If you see data/ folder, check your .gitignore file.

---

## Step 6: Create Initial Commit

```bash
git commit -m "Initial commit: PhD research data collection project"
```

You should see output showing files committed.

---

## Step 7: Set Up Authentication

GitHub requires authentication for pushing. Choose **Option A** (recommended) or **Option B**:

### Option A: Personal Access Token (PAT)

1. **Generate token on GitHub:**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Select scopes: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again)

2. **Use token when pushing:**
   - When prompted for password, paste your token (not your GitHub password)

3. **Cache credentials** (optional, to avoid repeated entry):
   ```bash
   git config credential.helper store
   ```

### Option B: GitHub CLI (gh)

1. **Install GitHub CLI:**
   - Download from https://cli.github.com/
   - Or use winget: `winget install GitHub.cli`

2. **Authenticate:**
   ```bash
   gh auth login
   ```
   - Follow prompts to authenticate via browser

---

## Step 8: Push to GitHub

Push your local repository to GitHub:
```bash
git push -u origin main
```

**If you see error about branch name:**
Some Git installations use "master" instead of "main". Check your branch:
```bash
git branch
```

If you're on "master", rename to "main":
```bash
git branch -M main
git push -u origin main
```

**Expected output:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), X.XX MiB | X.XX MiB/s, done.
Total XX (delta X), reused X (delta X)
To https://github.com/dpolonia/202510-CFE.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Step 9: Verify Upload

1. **Visit your GitHub repository:**
   https://github.com/dpolonia/202510-CFE

2. **Check that you see:**
   - ✅ README.md
   - ✅ LICENSE
   - ✅ .gitignore
   - ✅ requirements.txt
   - ✅ scripts/ folder
   - ✅ docs/ folder
   - ✅ metadata/ folder
   - ✅ notebooks/ folder (empty)
   - ❌ data/ folder (should NOT be visible - excluded by .gitignore)

3. **Verify repository size:**
   - Should be < 1 MB (not 124 MB)
   - If it's 124+ MB, you accidentally uploaded data/ folder

---

## Step 10: Configure Repository Settings (Optional)

On GitHub repository page:

1. **Add description:**
   - Click ⚙️ (settings icon) next to "About"
   - Description: "PhD research: Financial distress analysis of Portuguese NHS hospitals (2015-2025)"
   - Topics: `healthcare`, `finance`, `portugal`, `nhs`, `phd-research`, `data-analysis`

2. **Add README preview:**
   - Your README.md should automatically appear on the main page

---

## Future Workflow: Making Updates

When you make changes to your project:

### 1. Check status
```bash
git status
```

### 2. Stage changes
```bash
git add .
# Or stage specific files:
git add scripts/new_script.py
```

### 3. Commit changes
```bash
git commit -m "Descriptive message about what changed"
```

### 4. Push to GitHub
```bash
git push
```

---

## Troubleshooting

### Problem: "fatal: not a git repository"
**Solution:** You're not in the correct folder. Run:
```bash
cd C:\Users\dpolo\Documents\202510-CFE
```

### Problem: "fatal: remote origin already exists"
**Solution:** Remote already configured. Check with:
```bash
git remote -v
```

To change remote URL:
```bash
git remote set-url origin https://github.com/dpolonia/202510-CFE.git
```

### Problem: "failed to push some refs"
**Solution:** Pull changes first:
```bash
git pull origin main --rebase
git push
```

### Problem: "support for password authentication was removed"
**Solution:** You're using your GitHub password instead of a Personal Access Token. Generate a token (see Step 7) and use it as your password.

### Problem: data/ folder appeared on GitHub
**Solution:** Remove from Git tracking:
```bash
git rm -r --cached data/
git commit -m "Remove data folder from Git tracking"
git push
```

### Problem: Large file error (>100 MB)
**Solution:** Check .gitignore includes data/ folder:
```bash
cat .gitignore | grep data
```

Should show: `data/`

If missing, add it:
```bash
echo "data/" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore to exclude data folder"
git push
```

---

## Quick Reference Commands

```bash
# Check status
git status

# Stage all changes
git add .

# Commit with message
git commit -m "Your message here"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Check remote URL
git remote -v
```

---

## Summary

Your repository is now synchronized with GitHub!

**What's on GitHub:**
- All documentation (.md files)
- All scripts (.py files)
- Metadata (data_inventory.json)
- Configuration files (.gitignore, requirements.txt, LICENSE)
- **Total size:** < 1 MB

**What's NOT on GitHub:**
- data/ folder (124 MB) - excluded by .gitignore
- Users can download data by running your extraction scripts

**Next steps:**
1. Continue your PhD research
2. Update scripts and documentation as needed
3. Commit and push changes regularly
4. Keep data/ folder in local directory only

---

**Repository URL:** https://github.com/dpolonia/202510-CFE

**Questions?** Check GitHub's documentation: https://docs.github.com/en/get-started
