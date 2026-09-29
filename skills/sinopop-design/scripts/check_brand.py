#!/usr/bin/env python3
"""sinoPOP brand check — run on anything you made before handing it over.

Usage:  python3 check_brand.py <file-or-folder> [...]

Checks HTML / CSS / SVG / JS / JSX / TSX / Vue / Markdown files for:
  - colours that are not in design-system/tokens/tokens.json (hex and rgb())
  - retired colours (#141926 ink blue, #1B1E24 old grey)
  - forbidden wording ("ALL ACCESS")
Exit code 1 if anything is wrong, so agents can loop until it passes.
The WeChat framework B placeholder accent #1863C3 is reported as a reminder, not an error.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKENS = HERE.parent / "design-system" / "tokens" / "tokens.json"
EXTS = {".html", ".htm", ".css", ".svg", ".js", ".jsx", ".ts", ".tsx", ".vue", ".md"}
RETIRED = {"#141926": "retired ink blue — use surface #181A1F", "#1B1E24": "retired grey — use surface #181A1F"}
BORROWED = "#1863C3"  # WeChat framework B placeholder: replace with the poster colour
RULE_DOCS = {"SKILL.md", "AGENTS.md", "CHANGELOG.md", "README.md", "INSTALL.md", "CLAUDE.md"}  # rule books mention retired values on purpose
SHELL = {"#EDEDED"}   # grey page around the WeChat preview only; never inside #sp-article

palette = {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}", TOKENS.read_text(encoding="utf-8"))}
hex_re = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b")
rgb_re = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")


def norm(h):
    h = h.upper()
    return "#" + "".join(c * 2 for c in h[1:]) if len(h) == 4 else h


def check(path):
    problems, notes = [], []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for n, line in enumerate(text.splitlines(), 1):
        if "base64," in line:  # skip embedded images / fonts
            line = re.sub(r"base64,[A-Za-z0-9+/=]+", "", line)
        found = [norm(m) for m in hex_re.findall(line)]
        found += ["#%02X%02X%02X" % tuple(int(v) for v in m) for m in rgb_re.findall(line)]
        for h in found:
            if h in RETIRED:
                problems.append(f"{path}:{n}  {h}  {RETIRED[h]}")
            elif h == BORROWED:
                notes.append(f"{path}:{n}  {h}  WeChat B placeholder — replace with the poster colour before publishing")
            elif h in SHELL:
                continue
            elif h not in palette:
                problems.append(f"{path}:{n}  {h}  not a sinoPOP token colour")
        if re.search(r"all\s*access", line, re.I):
            problems.append(f"{path}:{n}  'ALL ACCESS' wording is not allowed")
    return problems, notes


def main(args):
    if not args:
        print(__doc__)
        return 2
    files = []
    for a in args:
        p = Path(a)
        files += [f for f in p.rglob("*") if f.suffix.lower() in EXTS and f.name not in RULE_DOCS] if p.is_dir() else [p]
    problems, notes = [], []
    for f in files:
        p, n = check(f)
        problems += p
        notes += n
    for line in notes:
        print("NOTE ", line)
    for line in problems:
        print("ERROR", line)
    print(f"\nChecked {len(files)} file(s): {len(problems)} error(s), {len(notes)} note(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
