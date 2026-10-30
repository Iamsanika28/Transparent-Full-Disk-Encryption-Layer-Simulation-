

from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

base = Path(__file__).resolve().parent
key_file = base / "keys" / "fernet.key"
disk_dir = base / "virtual_disk"
test_file = base / "tamper-test.bak"

if not key_file.exists():
    print("Encryption key not found.")
elif not disk_dir.exists():
    print("Virtual disk folder not found.")
else:
    encrypted_files = list(disk_dir.glob("*.enc"))

    if not encrypted_files:
        print("No encrypted .enc file found in virtual_disk.")
    else:
        cipher = Fernet(key_file.read_bytes())
        modified_data = bytearray(encrypted_files[0].read_bytes())
        modified_data[-1] ^= 1

        try:
            test_file.write_bytes(modified_data)
            cipher.decrypt(test_file.read_bytes())
            print("Unexpected: modified data was accepted.")
        except InvalidToken:
            print("PASS: modified encrypted data was rejected.")
        finally:
            test_file.unlink(missing_ok=True)

