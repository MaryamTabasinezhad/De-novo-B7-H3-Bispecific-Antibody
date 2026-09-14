from pathlib import Path
import shutil
import tomllib
root = Path(__file__).resolve().parent.parent
source = root / 'codex-permissions-setup'
roots = [root]
for project in roots:
    dest = project / '.codex'
    (dest / 'rules').mkdir(parents=True, exist_ok=True)
    for src, target in [(source / 'config.toml', dest / 'config.toml'), (source / 'claude-equivalent.rules', dest / 'rules/claude-equivalent.rules')]:
        if target.exists() and target.read_bytes() != src.read_bytes():
            raise RuntimeError(f'Refusing to overwrite existing settings: {target}')
        shutil.copyfile(src, target)
    print(f'Installed project config and rules: {dest}')
user = Path('/home/ghaedi/.codex/config.toml')
original = user.read_text()
parsed = tomllib.loads(original)
updated = original
for project in roots:
    for name in dict.fromkeys([str(project), str(project.resolve())]):
        level = parsed.get('projects', {}).get(name, {}).get('trust_level')
        if level is None:
            updated += f'\n[projects."{name}"]\ntrust_level = "trusted"\n'
        elif level != 'trusted':
            raise RuntimeError(f'Existing trust setting requires review: {name}')
if updated != original:
    backup = user.with_name('config.toml.before-mab-permissions')
    if not backup.exists():
        shutil.copyfile(user, backup)
    tomllib.loads(updated)
    user.write_text(updated)
    print(f'Added project trust entries; backup: {backup}')
