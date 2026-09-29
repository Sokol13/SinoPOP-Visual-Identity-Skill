"""Build tokens.css from tokens.json. Run: python3 tokens/build.py"""
import json, re, pathlib
here = pathlib.Path(__file__).parent
t = json.loads((here / "tokens.json").read_text())
prim = t["color"]["primitive"]
ROLES = ["display", "h1", "h2", "h3", "body", "caption", "label"]
def val(v):
    m = re.fullmatch(r"\{color\.primitive\.([\w-]+)\}", v)
    return f"var(--sp-{m.group(1)})" if m else v
def stack(fams): return ", ".join(f'"{f}"' if " " in f else f for f in fams)
def type_vars(lang, mobile=False):
    s = t["type"][lang]; out = []
    if not mobile:
        out.append(f"  --sp-font: {stack(s['family']['$value'])};")
        out.append(f"  --sp-measure: {s['measure']['$value']};")
    for r in ROLES:
        x = s[r]
        out.append(f"  --sp-type-{r}: {x['mobile' if mobile else 'size']['$value']};")
        if not mobile:
            out += [f"  --sp-type-{r}-lh: {x['line']['$value']};", f"  --sp-type-{r}-wt: {x['weight']['$value']};", f"  --sp-type-{r}-ls: {x['tracking']['$value']};"]
            if "case" in x: out.append(f"  --sp-type-{r}-case: {x['case']['$value']};")
    return out
out = ["/* Generated from tokens.json — do not edit by hand. */", ":root, .sp-root {"]
out += [f"  --sp-{k}: {v['$value']};" for k, v in prim.items()]
for k, v in t["space"].items(): out.append(f"  --sp-space-{k}: {v['$value']};")
out += [f"  --sp-radius: {t['radius']['component']['$value']};", f"  --sp-control-m: {t['size']['control-m']['$value']};", f"  --sp-control-s: {t['size']['control-s']['$value']};", "}"]
for theme, sel in (("dark", ':root, .sp-root, [data-sp-theme="dark"]'), ("light", '[data-sp-theme="light"]')):
    out.append(sel + " {")
    out += [f"  --sp-color-{k}: {val(v['$value'])};" for k, v in t["color"][theme].items() if not k.startswith("$")]
    out.append("}")
out.append("/* Typesetting: Chinese is the default; any element with lang=\"en\" switches to the English set. */")
out.append(':root, [lang|="zh"] {'); out += type_vars("zh"); out.append("}")
out.append('[lang|="en"] {'); out += type_vars("en"); out.append("}")
out.append("@media (max-width: 640px) {")
out.append('  :root, [lang|="zh"] {'); out += ["  " + l for l in type_vars("zh", True)]; out.append("  }")
out.append('  [lang|="en"] {'); out += ["  " + l for l in type_vars("en", True)]; out.append("  }")
out.append("}")
(here / "tokens.css").write_text("\n".join(out) + "\n")
print("wrote tokens.css")
