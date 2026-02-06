# Activate GitHub Pages Website
# Run this script in PowerShell to commit and push all website files

Write-Host "🚀 Activating GitHub Pages Website for GABA Topology Study" -ForegroundColor Cyan
Write-Host ""

# Add all website files
Write-Host "📦 Adding files..." -ForegroundColor Yellow
git add docs/
git add QUICKSTART_PAGES.md
git add GITHUB_PAGES_SETUP.md
git add WEBSITE_SUMMARY.md
git add SITE_ARCHITECTURE.md
git add _config.yml
git add README.md

Write-Host "✅ Files staged" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git commit -m "Add GitHub Pages website with comprehensive documentation"

Write-Host "✅ Committed" -ForegroundColor Green
Write-Host ""

# Push to GitHub
Write-Host "☁️  Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin master

Write-Host "✅ Pushed to GitHub" -ForegroundColor Green
Write-Host ""

Write-Host "🎉 Success! Your website files are now on GitHub." -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Go to: https://github.com/[your-username]/flywire-gaba-topology/settings/pages"
Write-Host "2. Under 'Source', select:"
Write-Host "   - Branch: master"
Write-Host "   - Folder: /docs"
Write-Host "3. Click 'Save'"
Write-Host ""
Write-Host "4. Update your username in:"
Write-Host "   - docs/_config.yml (lines 6-7)"
Write-Host "   - docs/index.md (GitHub links)"
Write-Host ""
Write-Host "5. Commit and push the username updates"
Write-Host ""
Write-Host "🌐 Your site will be live at:" -ForegroundColor Cyan
Write-Host "   https://[your-username].github.io/flywire-gaba-topology/"
Write-Host ""
Write-Host "⏱️  Site builds in 1-2 minutes after enabling GitHub Pages" -ForegroundColor Yellow
