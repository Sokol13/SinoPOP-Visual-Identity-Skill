#!/usr/bin/env bash
# Rebuild the generated files in dist/ after changing anything in skills/sinopop-design.
#   dist/sinopop-design-skill.zip  -> upload in the Claude app (Settings → Skills)
#   dist/chatgpt-knowledge/        -> drag into a ChatGPT Project as project files
set -euo pipefail
cd "$(dirname "$0")/.."
S=skills/sinopop-design
rm -rf dist && mkdir -p dist/chatgpt-knowledge

(cd skills && zip -qr -X ../dist/sinopop-design-skill.zip sinopop-design -x '*/__pycache__/*' '*.pyc')

K=dist/chatgpt-knowledge
cp "$S/SKILL.md"                                   "$K/SKILL.md"
cp "$S/design-system/AGENTS.md"                    "$K/AGENTS.md"
cp "$S/design-system/tokens/tokens.json"           "$K/tokens.json"
cp "$S/design-system/tokens/tokens.css"            "$K/tokens.css"
cp "$S/design-system/web/sinopop-widgets.css"      "$K/sinopop-widgets.css"
cp "$S/design-system/wechat/article-template.html" "$K/article-template.html"
cp "$S/design-system/wechat/article-artist.html"   "$K/article-artist.html"
cp "$S/design-system/assets/sinopop-logo-white.svg" "$K/sinopop-logo-white.svg"
cp "$S/design-system/assets/sinopop-logo-black.svg" "$K/sinopop-logo-black.svg"
# the two PDFs live in docs/ — upload them from there too (not copied to keep the repo small)
cp chatgpt/PROJECT-INSTRUCTIONS.md "$K/PROJECT-INSTRUCTIONS.md"

echo "dist rebuilt:"; ls -la dist dist/chatgpt-knowledge
