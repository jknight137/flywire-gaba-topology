#!/bin/bash
# Activate GitHub Pages Website
# Run this script to commit and push all website files

echo "🚀 Activating GitHub Pages Website for GABA Topology Study"
echo ""

# Add all website files
echo "📦 Adding files..."
git add docs/
git add QUICKSTART_PAGES.md
git add GITHUB_PAGES_SETUP.md
git add WEBSITE_SUMMARY.md
git add SITE_ARCHITECTURE.md
git add _config.yml
git add README.md

echo "✅ Files staged"
echo ""

# Commit
echo "💾 Committing changes..."
git commit -m "Add GitHub Pages website with comprehensive documentation"

echo "✅ Committed"
echo ""

# Push to GitHub
echo "☁️  Pushing to GitHub..."
git push -u origin master

echo "✅ Pushed to GitHub"
echo ""

echo "🎉 Success! Your website files are now on GitHub."
echo ""
echo "📋 Next Steps:"
echo "1. Go to: https://github.com/[your-username]/flywire-gaba-topology/settings/pages"
echo "2. Under 'Source', select:"
echo "   - Branch: master"
echo "   - Folder: /docs"
echo "3. Click 'Save'"
echo ""
echo "4. Update your username in:"
echo "   - docs/_config.yml (lines 6-7)"
echo "   - docs/index.md (GitHub links)"
echo ""
echo "5. Commit and push the username updates"
echo ""
echo "🌐 Your site will be live at:"
echo "   https://[your-username].github.io/flywire-gaba-topology/"
echo ""
echo "⏱️  Site builds in 1-2 minutes after enabling GitHub Pages"
