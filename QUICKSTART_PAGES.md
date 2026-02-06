# 🚀 Quick Start: Activate Your GitHub Pages Website

## 3 Steps to Go Live

### Step 1: Push to GitHub (if not already done)

```bash
git add .
git commit -m "Add GitHub Pages website"
git push -u origin master
```

### Step 2: Enable GitHub Pages

1. Go to: `https://github.com/[your-username]/flywire-gaba-topology/settings/pages`
2. Under **"Source"**, select:
   - Branch: **master**
   - Folder: **/docs**
3. Click **Save**

### Step 3: Update Your Username

Replace `jknight137` with your actual GitHub username in these files:

**docs/\_config.yml** (line 6-7):

```yaml
url: "https://[YOUR-USERNAME].github.io"
repository: [YOUR-USERNAME]/flywire-gaba-topology
```

**docs/index.md** (multiple locations):

```markdown
[GitHub repository](https://github.com/[YOUR-USERNAME]/flywire-gaba-topology)
```

Then commit and push:

```bash
git add docs/_config.yml docs/index.md
git commit -m "Update GitHub username in config"
git push
```

---

## ✅ Your Site is Live!

**URL:** `https://[YOUR-USERNAME].github.io/flywire-gaba-topology/`

GitHub Pages will automatically rebuild your site when you push changes (takes ~1-2 minutes).

---

## 📝 What You Get

Your new website includes:

- ✅ **Home page** with key findings and abstract
- ✅ **Methods page** with detailed methodology
- ✅ **Results page** with comprehensive findings
- ✅ **Code page** with reproducibility guide
- ✅ **About page** with project context
- ✅ **Responsive design** (works on mobile)
- ✅ **Custom styling** (modern, professional look)
- ✅ **Math equations** (MathJax support)
- ✅ **Navigation menu** (easy site navigation)

---

## 🎨 Customization Options

### Change Site Title/Description

Edit `docs/_config.yml`:

```yaml
title: "Your Custom Title"
description: "Your custom description"
author: "Your Name"
email: your.email@institution.edu
```

### Change Color Scheme

Edit `docs/assets/css/style.scss` and search for:

- `#667eea` (primary purple)
- `#764ba2` (secondary purple)

Replace with your preferred colors.

### Add Your Own Content

- Add new `.md` files to `docs/` folder
- Use the same frontmatter format:
  ```yaml
  ---
  layout: default
  title: Your Page Title
  ---
  ```

---

## 🔍 Preview Locally (Optional)

To test changes before pushing:

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Visit: `http://localhost:4000/flywire-gaba-topology/`

---

## 📚 Full Documentation

See [GITHUB_PAGES_SETUP.md](../GITHUB_PAGES_SETUP.md) for:

- Detailed setup instructions
- Advanced customization options
- Troubleshooting guide
- SEO and analytics setup

---

## 🆘 Troubleshooting

**Site not building?**

- Check the "Actions" tab in GitHub for error messages
- Ensure `docs/_config.yml` has valid YAML syntax

**404 errors?**

- Verify `baseurl` in `_config.yml` matches repo name
- Check that all file names are lowercase

**Styling not working?**

- Clear browser cache
- Wait 2-3 minutes for GitHub to rebuild

---

## 🎉 You're All Set!

Your professional research website is ready to share with:

- Collaborators
- Reviewers
- The broader research community

**Share your URL:**
`https://[YOUR-USERNAME].github.io/flywire-gaba-topology/`
