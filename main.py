
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
import hashlib

BASE_DIR = Path(__file__).resolve().parent
KEY_FILE = BASE_DIR / "keys" / "fernet.key"
STORAGE_DIR = BASE_DIR / "storage"
FILE_STORAGE = STORAGE_DIR / "encrypted_files"

STORAGE_DIR.mkdir(exist_ok=True)
FILE_STORAGE.mkdir(exist_ok=True)


def load_cipher():
    if not KEY_FILE.exists():
        KEY_FILE.parent.mkdir(exist_ok=True)
        KEY_FILE.write_bytes(Fernet.generate_key())

    return Fernet(KEY_FILE.read_bytes())


cipher = load_cipher()


def safe_name(filename):
    name = Path(filename).name
    if not name or name != filename or name in {".", ".."}:
        raise ValueError("Enter a filename only, without folder paths.")
    return hashlib.sha256(name.encode()).hexdigest() + ".enc"


def encrypt_message():
    message = input("Enter your confidential message: ")
    encrypted = cipher.encrypt(message.encode("utf-8"))
    filename = input("Enter a name (e.g. note.txt): ").strip()
    output = STORAGE_DIR / safe_name(filename)
    output.write_bytes(encrypted)
    print("Message encrypted successfully.")


def decrypt_message():
    filename = input("Enter the name used when saving: ").strip()
    path = STORAGE_DIR / safe_name(filename)

    if not path.exists():
        print("Encrypted message not found.")
        return

    try:
        print(cipher.decrypt(path.read_bytes()).decode("utf-8"))
    except (InvalidToken, UnicodeDecodeError):
        print("Decryption failed: invalid key or modified data.")


def encrypt_file():
    filename = input("Enter the sample filename (e.g. sample.txt): ").strip()

    if not filename or Path(filename).name != filename:
        print("Enter only a filename, not a folder path.")
        return

    source = STORAGE_DIR / filename
    if not source.is_file():
        print("File not found inside the storage folder.")
        return

    output = FILE_STORAGE / safe_name(filename)
    if output.exists():
        confirm = input("Encrypted copy exists. Overwrite it? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return

    output.write_bytes(cipher.encrypt(source.read_bytes()))
    print("File encrypted successfully.")
    print("Original file was not changed.")
    print("Encrypted copy:", output)


def decrypt_file():
    filename = input("Enter the original filename used for encryption: ").strip()

    if not filename or Path(filename).name != filename:
        print("Enter only a filename, not a folder path.")
        return

    encrypted_path = FILE_STORAGE / safe_name(filename)
    if not encrypted_path.is_file():
        print("Encrypted file not found.")
        return

    output_dir = BASE_DIR / "decrypted"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / filename

    if output_path.exists():
        confirm = input("Decrypted output exists. Overwrite it? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return

    try:
        output_path.write_bytes(cipher.decrypt(encrypted_path.read_bytes()))
        print("File decrypted successfully.")
        print("Recovered file:", output_path)
    except InvalidToken:
        print("Decryption failed: invalid key or modified data.")


def main():
    while True:
        print("\n=== Disk Encryption Layer Simulation ===")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Encrypt a file from storage")
        print("4. Decrypt a file to decrypted folder")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                encrypt_message()
            elif choice == "2":
                decrypt_message()
            elif choice == "3":
                encrypt_file()
            elif choice == "4":
                decrypt_file()
            elif choice == "5":
                print("Exiting.")
                break
            else:
                print("Invalid choice.")
        except (OSError, ValueError) as error:
            print("Operation failed:", error)


if __name__ == "__main__":
    main()
