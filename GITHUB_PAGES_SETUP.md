# Setting Up GitHub Pages for Your Project

This guide will help you activate the GitHub Pages website for your project.

## Quick Setup (Recommended)

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/jknight137/flywire-gaba-topology`
2. Click on **Settings** (gear icon at the top)
3. In the left sidebar, click **Pages**
4. Under **Source**, select:
   - **Branch:** `master` (or `main`)
   - **Folder:** `/docs`
5. Click **Save**

### Step 2: Wait for Deployment

GitHub will automatically build and deploy your site. This takes 1-2 minutes.

You'll see a message: "Your site is live at `https://jknight137.github.io/flywire-gaba-topology/`"

### Step 3: Update URLs

Replace `jknight137` in the following files with your actual GitHub username:

**In `docs/_config.yml`:**

```yaml
url: "https://jknight137.github.io"
repository: jknight137/flywire-gaba-topology
```

**In `docs/index.md`:** Update all GitHub links to your repository

**In `README.md`:** Update the website URL

### Step 4: Commit and Push

```bash
git add .
git commit -m "Configure GitHub Pages URLs"
git push
```

Your site will be live at: `https://jknight137.github.io/flywire-gaba-topology/`

---

## Local Development (Optional)

To preview the site locally before pushing:

### Prerequisites

Install Ruby and Bundler:

- **Windows:** Download from [rubyinstaller.org](https://rubyinstaller.org/)
- **Mac:** `brew install ruby`
- **Linux:** `sudo apt-get install ruby-full build-essential zlib1g-dev`

### Run Locally

```bash
cd docs

# Install dependencies (first time only)
bundle install

# Start the Jekyll server
bundle exec jekyll serve

# Or with live reload:
bundle exec jekyll serve --livereload
```

Visit: `http://localhost:4000/flywire-gaba-topology/`

The site will automatically rebuild when you make changes.

---

## Customization Guide

### Update Site Metadata

Edit `docs/_config.yml`:

```yaml
title: "GABA Topology Study"
description: "Your custom description"
author: "Your Name"
email: your.email@institution.edu
```

### Change Colors/Styling

Edit `docs/assets/css/style.scss` to customize:

- Color scheme (search for `#667eea` and `#764ba2`)
- Typography
- Layout spacing
- Component styles

### Add New Pages

1. Create a new `.md` file in `docs/`
2. Add YAML frontmatter:
   ```yaml
   ---
   layout: default
   title: Your Page Title
   ---
   ```
3. Add content using Markdown
4. Link to it from other pages

### Modify Navigation

Edit `docs/_layouts/default.html` to change the navigation menu:

```html
<nav class="main-nav">
  <a href="{{ site.baseurl }}/" class="btn">Home</a>
  <a href="{{ site.baseurl }}/your-new-page" class="btn">New Page</a>
</nav>
```

---

## Advanced Features

### Custom Domain (Optional)

To use a custom domain like `gaba-topology.yourlab.edu`:

1. In GitHub Settings → Pages, enter your custom domain
2. Add a `CNAME` file to `docs/` with your domain name
3. Configure DNS with your domain provider:
   - Add CNAME record pointing to `jknight137.github.io`

### Analytics (Optional)

Add Google Analytics by editing `docs/_config.yml`:

```yaml
google_analytics: UA-XXXXXXXXX-X
```

### Custom 404 Page

Create `docs/404.md`:

```yaml
---
layout: default
title: Page Not Found
permalink: /404.html
---
# 404 - Page Not Found

The page you're looking for doesn't exist.

[Return to Home](index.md)
```

---

## Troubleshooting

### Site Not Building

1. Check the **Actions** tab in your GitHub repository for build errors
2. Ensure `docs/_config.yml` has valid YAML syntax
3. Verify all required files exist (index.md, \_config.yml)

### 404 Errors for Pages

- Ensure `baseurl` in `_config.yml` matches your repository name
- Links should use `{{ site.baseurl }}/page` format
- File names are case-sensitive

### Styling Not Applying

1. Clear browser cache
2. Check `docs/assets/css/style.scss` has the `---` frontmatter at the top
3. Verify the `@import` statement is correct

### Local Jekyll Errors

```bash
# Update dependencies
bundle update

# Clean and rebuild
bundle exec jekyll clean
bundle exec jekyll build
```

---

## GitHub Pages Features Used

✅ **Jekyll** — Static site generator  
✅ **Cayman Theme** — Clean, professional theme  
✅ **Custom CSS** — Enhanced styling with modern design  
✅ **MathJax** — LaTeX equation rendering  
✅ **Responsive Design** — Mobile-friendly layout  
✅ **SEO Optimization** — Meta tags and sitemap  
✅ **Syntax Highlighting** — Code block styling

---

## File Structure

```
docs/
├── _config.yml              # Jekyll configuration
├── _layouts/
│   └── default.html         # Custom layout with navigation
├── assets/
│   └── css/
│       └── style.scss       # Custom styling
├── index.md                 # Home page
├── methods.md               # Methods documentation
├── results.md               # Results page
├── code.md                  # Code & reproducibility guide
├── Gemfile                  # Ruby dependencies
└── README.md                # Docs folder readme
```

---

## Best Practices

### Content Guidelines

- **Use descriptive headings** — Helps with navigation and SEO
- **Include alt text for images** — Accessibility
- **Link to external resources** — FlyWire dataset, papers, etc.
- **Keep paragraphs concise** — Easier to read online
- **Use tables for data** — Better than long lists

### Performance

- **Optimize images** — Use compressed PNG/JPEG files
- **Minimize custom JavaScript** — Keeps site fast
- **Use CDN resources** — MathJax, fonts from CDNs

### SEO

- **Set descriptive titles** — Each page should have unique title
- **Write meta descriptions** — In page frontmatter
- **Use semantic HTML** — Proper heading hierarchy
- **Include keywords naturally** — GABA, connectome, FlyWire

---

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Cayman Theme](https://github.com/pages-themes/cayman)
- [Markdown Guide](https://www.markdownguide.org/)
- [MathJax Documentation](https://www.mathjax.org/)

---

## Support

If you encounter issues:

1. Check GitHub Pages build status in Actions tab
2. Review Jekyll error messages
3. Search GitHub Pages documentation
4. Open an issue in the repository

---

**Your GitHub Pages site is ready to go!** 🎉

After enabling it in Settings, your professional research website will be live in minutes.
