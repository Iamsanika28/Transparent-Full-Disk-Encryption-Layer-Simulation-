
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
import hashlib


class TransparentEncryptionLayer:
    """Simulate encrypted storage with automatic encryption and decryption."""

    def __init__(self, project_folder=None):
        self.base_dir = (
            Path(project_folder).resolve()
            if project_folder
            else Path(__file__).resolve().parent
        )

        self.key_file = self.base_dir / "keys" / "fernet.key"
        self.disk_dir = self.base_dir / "virtual_disk"

        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        self.disk_dir.mkdir(parents=True, exist_ok=True)

        if not self.key_file.exists():
            self.key_file.write_bytes(Fernet.generate_key())

        self.cipher = Fernet(self.key_file.read_bytes())

    def _encrypted_path(self, filename):
        """Map a simple filename to a safe encrypted storage name."""
        if (
            not filename
            or Path(filename).name != filename
            or filename in {".", ".."}
            or "/" in filename
            or "\\" in filename
        ):
            raise ValueError("Use a filename only, without folder paths.")

        file_id = hashlib.sha256(filename.encode("utf-8")).hexdigest()
        return self.disk_dir / f"{file_id}.enc"

    def write_file(self, filename, data):
        """Encrypt data automatically before writing it to simulated disk."""
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes.")

        encrypted_path = self._encrypted_path(filename)
        encrypted_path.write_bytes(self.cipher.encrypt(data))

        print(f"[ENCRYPTION LAYER] Stored encrypted: {filename}")

    def read_file(self, filename):
        """Decrypt data automatically after reading it from simulated disk."""
        encrypted_path = self._encrypted_path(filename)

        if not encrypted_path.exists():
            raise FileNotFoundError(f"No stored file named: {filename}")

        encrypted_data = encrypted_path.read_bytes()
        plaintext = self.cipher.decrypt(encrypted_data)

        print(f"[ENCRYPTION LAYER] Returned decrypted data: {filename}")
        return plaintext

    def list_files(self):
        """List logical filenames are not stored in the encrypted disk."""
        return [
            file.name
            for file in self.disk_dir.iterdir()
            if file.is_file() and file.suffix == ".enc"
        ]
