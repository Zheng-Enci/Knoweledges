import re
import shutil
from pathlib import Path

SUSPICIOUS_PATTERNS = [
    r"FromBase64String\(''{1}''\)",
    r"Emit\s*\('Set-Alias -Name \"\{0\}\" -Value \"\{1\}\"",
    r"Set-Alias -Name \"\{0\}\" -Value \"\{1\}\""
]

PROFILE_REL_PATHS = [
    Path("Documents") / "PowerShell" / "Microsoft.PowerShell_profile.ps1",
    Path("Documents") / "PowerShell" / "Microsoft.VSCode_profile.ps1",
    Path("Documents") / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1",
    Path("Documents") / "WindowsPowerShell" / "profile.ps1"
]

def clean_profile_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not any(re.search(pattern, text, re.IGNORECASE) for pattern in SUSPICIOUS_PATTERNS):
        return False

    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)

    lines = text.splitlines()
    keep = []
    skip_block = False
    for line in lines:
        if any(pattern.split("(")[0] in line for pattern in ["Emit ", "FromBase64String", "Set-Alias -Name \"{0}\""]):
            skip_block = True
        if not skip_block:
            keep.append(line)
        if skip_block and line.strip().endswith(")"):
            skip_block = False

    sanitized = "\n".join(keep).strip() + "\n"
    path.write_text(sanitized, encoding="utf-8")
    return True

def main():
    home = Path.home()
    modified = []

    for rel in PROFILE_REL_PATHS:
        profile_path = home / rel
        if profile_path.exists():
            try:
                if clean_profile_file(profile_path):
                    modified.append(str(profile_path))
            except Exception as exc:
                print(f"[!] 处理 {profile_path} 失败: {exc}")

    if not modified:
        print("未在任何 profile 中发现可疑片段，未做改动。")
    else:
        print("已清理以下 profile，并生成 .bak 备份：")
        for path in modified:
            print(f" - {path}")
        print("请关闭所有终端窗口后重新打开再试。")

if __name__ == "__main__":
    main()