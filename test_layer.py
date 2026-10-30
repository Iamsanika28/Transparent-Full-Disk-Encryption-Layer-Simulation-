
from encryption_layer import TransparentEncryptionLayer

disk = TransparentEncryptionLayer()

filename = "demo.txt"
original = b"This file is stored through the transparent encryption layer."

# Write: automatically encrypts before storage
disk.write_file(filename, original)

# Read: automatically decrypts after storage
recovered = disk.read_file(filename)

assert recovered == original, "Recovered data does not match!"
print("PASS: recovered data matches the original.")

# Inspect stored bytes without decrypting them
encrypted_path = disk._encrypted_path(filename)
stored = encrypted_path.read_bytes()

assert stored != original, "Data was not encrypted!"
print("PASS: virtual disk contains encrypted data.")
print("Encrypted storage file:", encrypted_path.name)
