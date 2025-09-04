@echo off
title Cleaning up unwanted files

echo Cleaning up unwanted files from the project...
echo ==========================================

echo Removing .bolt directory...
rmdir /s /q .bolt 2>nul

echo Removing any log files...
del *.log 2>nul
del *.log.* 2>nul

echo Cleaning node_modules cache...
rmdir /s /q node_modules\.vite 2>nul
rmdir /s /q node_modules\.vite-temp 2>nul

echo Removing temporary files...
del *.tmp 2>nul
del *.temp 2>nul
del *~ 2>nul

echo Cleanup completed!
echo.
echo Note: The following files and directories are important and have NOT been removed:
echo - dist/ (built files)
echo - node_modules/ (dependencies)
echo - src/ (source code)
echo - .env and .env.production (environment files)
echo - package.json and package-lock.json (dependency files)
echo - vite.config.ts (build configuration)
echo - index.html (entry point)
echo - README.md and other documentation files

pause