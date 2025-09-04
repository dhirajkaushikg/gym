# Cleanup script for removing unwanted files
Write-Host "Cleaning up unwanted files from the project..." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Remove .bolt directory if it exists
if (Test-Path ".bolt") {
    Remove-Item -Recurse -Force ".bolt"
    Write-Host "Removed .bolt directory" -ForegroundColor Yellow
}

# Remove any log files
Get-ChildItem -Path "." -Filter "*.log" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "." -Filter "*.log.*" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "Removed log files" -ForegroundColor Yellow

# Clean node_modules cache
if (Test-Path "node_modules\.vite") {
    Remove-Item -Recurse -Force "node_modules\.vite"
    Write-Host "Removed node_modules\.vite directory" -ForegroundColor Yellow
}

if (Test-Path "node_modules\.vite-temp") {
    Remove-Item -Recurse -Force "node_modules\.vite-temp"
    Write-Host "Removed node_modules\.vite-temp directory" -ForegroundColor Yellow
}

# Remove temporary files
Get-ChildItem -Path "." -Filter "*.tmp" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "." -Filter "*.temp" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "." -Filter "*~" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "Removed temporary files" -ForegroundColor Yellow

Write-Host "Cleanup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Note: The following files and directories are important and have NOT been removed:" -ForegroundColor Cyan
Write-Host "- dist/ (built files)" -ForegroundColor Cyan
Write-Host "- node_modules/ (dependencies)" -ForegroundColor Cyan
Write-Host "- src/ (source code)" -ForegroundColor Cyan
Write-Host "- .env and .env.production (environment files)" -ForegroundColor Cyan
Write-Host "- package.json and package-lock.json (dependency files)" -ForegroundColor Cyan
Write-Host "- vite.config.ts (build configuration)" -ForegroundColor Cyan
Write-Host "- index.html (entry point)" -ForegroundColor Cyan
Write-Host "- README.md and other documentation files" -ForegroundColor Cyan