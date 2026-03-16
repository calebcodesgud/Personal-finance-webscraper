#!/bin/zsh
sleep 0.25
SCRIPT=$(mktemp --suffix=.js)
echo "workspace.activeWindow.minimized = true" > "$SCRIPT"
ID=$(qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript "$SCRIPT" 2>/dev/null)
echo "Script ID: $ID"
qdbus6 org.kde.KWin "/Scripting/Script${ID}" run
qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript "$SCRIPT"
rm -f "$SCRIPT"
# Home Value Scraper - Linux/Ubuntu Launcher
# This shell script runs the combined scraper on Ubuntu/Linux
sleep 10
konsole -e '~/MEGA/scraper/run_scrapers_now.sh' '&&' exit
