from pathlib import Path

from deskset.core.standard import DesksetError

# 检查 vault_path 是不是 Obsidian 仓库
def check_vault(vault_path: str) -> None:
    if not (Path(vault_path) / '.obsidian').is_dir():
        raise DesksetError(message=f'{vault_path} 不是 Obsidian 仓库')
