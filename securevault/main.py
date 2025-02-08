import os
from pathlib import Path
from typing import Optional, Self


VAULTS_PATH: Path = Path(os.environ['USERPROFILE']) / '.vaults' if os.name == 'nt' else Path('~').expanduser() / '.vaults'

if not os.path.exists(VAULTS_PATH):
    os.makedirs(VAULTS_PATH)


class Vault:
    def __init__(self: Self) -> None:
        self.vaults: list[str] = [vault_name.stem for vault_name in VAULTS_PATH.iterdir() if vault_name.is_dir()]
        self.active_vault: str = self.vaults[0] if self.vaults else None
        self.vault_path: Path = VAULTS_PATH / self.active_vault if self.active_vault else None

    def create_vault(self: Self, vault_name: str, encoder_file: Path | str) -> None:
        ...

    def open_vault(self: Self, vault_name: str) -> None:
        ...

    def update_vault(self: Self, new_vault_name: str, encoder_file: Optional[Path | str]) -> None:
        ...

    def add_key(self: Self, key_path: str, data: str) -> None:
        ...

    def get_key(self: Self, key_path: str):
        ...

    def search_key(self: Self, key_path: str) -> bool:
        ...

    def del_key(self: Self, key_path: str) -> None:
        ...

    def backup_vault(self: Self) -> None:
        ...

    def restore_vault(self: Self) -> None:
        ...

    def del_vault(self: Self) -> None:
        ...

