"""Checks SKILL.md front matter against the Agent Skills rules that claude.ai
uploads enforce: allowed keys only, kebab-case name matching the folder,
description present, under 1024 characters, no angle brackets."""
import re, sys, pathlib
skill = pathlib.Path(sys.argv[1])
text = (skill / "SKILL.md").read_text()
m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
assert m, "SKILL.md must start with front matter"
fm = m.group(1)
keys = re.findall(r"^([a-z_-]+):", fm, re.M)
allowed = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
bad = set(keys) - allowed
assert not bad, f"keys not allowed on claude.ai: {bad}"
name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64, name
assert name == skill.name, f"folder {skill.name} must match name {name}"
desc = re.search(r"^description:\s*(.+)$", fm, re.M).group(1).strip()
assert len(desc) <= 1024, f"description is {len(desc)} chars"
assert "<" not in desc and ">" not in desc, "no angle brackets in description"
others = [p for p in skill.rglob("SKILL.md") if p != skill / "SKILL.md"]
assert not others, f"only one SKILL.md allowed: {others}"
lines = text.count("\n")
assert lines < 500, f"SKILL.md is {lines} lines"
print(f"ok: {name}, description {len(desc)} chars, SKILL.md {lines} lines")
