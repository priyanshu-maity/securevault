import os
from pathlib import Path
from typing import Optional, Self
import pickle
from encoding.utils import TextEncoder


VAULTS_PATH: Path = Path(os.environ['USERPROFILE']) / '.vaults' if os.name == 'nt' else Path('~').expanduser() / '.vaults'

if not os.path.exists(VAULTS_PATH):
    VAULTS_PATH.mkdir()


class Vault:
    def __init__(self: Self) -> None:
        self.vaults: list[str] = [vault_name.stem.lower() for vault_name in VAULTS_PATH.iterdir() if vault_name.is_dir()]
        self.active_vault: str = self.vaults[0] if self.vaults else None
        self.vault_path: Path = VAULTS_PATH / self.active_vault if self.active_vault else None

    def create_vault(self: Self, vault_name: str, encoder: Path | str | TextEncoder) -> None:
        if vault_name.lower() in self.vaults:
            raise ValueError(f"Vault '{vault_name}' already exists")

        vault_path = VAULTS_PATH / vault_name.lower()
        vault_path.mkdir()

        if isinstance(encoder, str | Path):
            encoder_path = Path(encoder) if isinstance(encoder, str) else encoder
            if encoder_path.is_file() and encoder_path.suffix == '.enc':
                with open(encoder_path, 'rb') as enc_file:
                    encoder = pickle.load(enc_file)
                with open(vault_path / "encoder.enc", 'wb') as enc_file:
                    pickle.dump(encoder, enc_file, protocol=4)
            else:
                raise FileNotFoundError(f"Encoder file not found at {encoder_path}")
        elif isinstance(encoder, TextEncoder):
            with open(vault_path / "encoder.enc", 'wb') as enc_file:
                pickle.dump(encoder, enc_file, protocol=4)
        else:
            raise ValueError("encoder must be a TextEncoder instance or path to a '.enc' file.")

        (vault_path / "index.idx").touch()
        (vault_path / "data.vault").touch()

        self.vaults.append(vault_name.lower())

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


if __name__ == '__main__':
    from encoding.ciphers.substitution import CaesarCipher, AffineCipher
    from encoding.utils import Pipeline
    encoder = Pipeline([
        (CaesarCipher(3), "caesar"),
        (AffineCipher(2, 5), "affine")
    ])
    # vault = Vault()
    # vault.create_vault("test_vault", encoder)

    print(pickle.dumps(encoder))
