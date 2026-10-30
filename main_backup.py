
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

# Project folders
BASE_DIR = Path(__file__).resolve().parent
KEY_DIR = BASE_DIR / "keys"
STORAGE_DIR = BASE_DIR / "storage"
KEY_FILE = KEY_DIR / "fernet.key"

# Create required folders
KEY_DIR.mkdir(exist_ok=True)
STORAGE_DIR.mkdir(exist_ok=True)


def load_or_create_key():
    if KEY_FILE.exists():
        return Fernet(KEY_FILE.read_bytes())

    key = Fernet.generate_key()
    with KEY_FILE.open("xb") as file:
        file.write(key)

    return Fernet(key)


cipher = load_or_create_key()


def get_storage_path(filename):
    # Accept filenames only, not folder paths
    if (
        not filename
        or filename in {".", ".."}
        or Path(filename).name != filename
        or "/" in filename
        or "\\" in filename
    ):
        raise ValueError("Enter a valid filename without folder paths.")

    # Use a safe generated name for encrypted storage
    import hashlib
    file_id = hashlib.sha256(filename.encode("utf-8")).hexdigest()
    return STORAGE_DIR / f"{file_id}.enc"


def encrypt_file(filename, message):
    path = get_storage_path(filename)

    # Convert text into bytes, then encrypt
    plaintext = message.encode("utf-8")
    encrypted_data = cipher.encrypt(plaintext)

    # Store encrypted data, not the original message
    path.write_bytes(encrypted_data)

    print("\nFile encrypted and saved successfully!")
    print("Encrypted storage file:", path.name)


def decrypt_file(filename):
    path = get_storage_path(filename)

    if not path.exists():
        print("File not found. Save it first.")
        return

    try:
        encrypted_data = path.read_bytes()
        plaintext = cipher.decrypt(encrypted_data)

        print("\nDecrypted message:")
        print(plaintext.decode("utf-8"))

    except (InvalidToken, UnicodeDecodeError):
        print("Decryption failed: invalid key or modified data.")


def main():
    while True:
        print("\n=== Transparent Disk Encryption Simulation ===")
        print("1. Save and encrypt a message")
        print("2. Read and decrypt a message")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            filename = input("Enter filename (e.g. secret.txt): ").strip()
            message = input("Enter your confidential message: ")

            try:
                encrypt_file(filename, message)
            except (ValueError, OSError) as error:
                print("Could not save file:", error)

        elif choice == "2":
            filename = input("Enter filename to read: ").strip()

            try:
                decrypt_file(filename)
            except (ValueError, OSError) as error:
                print("Could not read file:", error)

        elif choice == "3":
            print("Exiting the simulation.")
            break

        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
