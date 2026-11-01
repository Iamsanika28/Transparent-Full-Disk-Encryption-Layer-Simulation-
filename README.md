# 🔐 Transparent Full Disk Encryption Layer Simulation

## 📌 Project Overview

The **Transparent Full Disk Encryption Layer Simulation** is a Python-based project that demonstrates how encryption and decryption can protect files from unauthorized access.

The project simulates a disk encryption environment where files are encrypted before being stored and decrypted when authorized access is required.

It uses the **Fernet symmetric encryption mechanism** from the Python Cryptography library to provide confidentiality and integrity protection.

This project is designed for educational purposes to demonstrate the working principles of disk encryption without modifying an actual physical hard drive.

## 🎯 Objectives

- To understand the working principles of disk encryption.
- To protect files using symmetric encryption.
- To simulate secure file storage and retrieval.
- To prevent unauthorized access to encrypted files.
- To demonstrate file encryption and decryption using Python.

## ✨ Features

- **File Encryption:** Converts readable files into encrypted `.enc` files.
- **File Decryption:** Restores encrypted files using the correct encryption key.
- **Key Management:** Uses a Fernet key for encryption and decryption.
- **File Integrity:** Detects unauthorized modifications to encrypted files.
- **Secure Storage Simulation:** Stores encrypted files in a simulated virtual disk environment.
- **Authentication through Key:** Only users possessing the correct key can decrypt protected files.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Cryptography | Encryption and decryption |
| Fernet | Symmetric authenticated encryption |
| Flask | Optional web-based interface |
| HTML/CSS | User interface |
| VS Code | Development environment |

## 📂 Project Structure

```text
Transparent-Disk-Encryption/
│
├── app.py
├── main.py
├── gui.py
├── keys/
│   └── fernet.key
│
├── storage/
├── virtual_disk/
├── encrypted_files/
├── decrypted/
│
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: The folder structure may vary depending on your implementation.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Iamsanika28/Transparent-Full-Disk-Encryption-Layer-Simulation-.git
```

### 2. Navigate to the Project Directory

```bash
cd Transparent-Disk-Encryption
```

### 3. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If needed, install the Cryptography library separately:

```bash
pip install cryptography
```

## ▶️ How to Run

Run the Python application:

```bash
python main.py
```

If using the Flask web interface:

```bash
python app.py
```

Open the browser at:

```text
http://127.0.0.1:5000
```

## 🔒 Working Principle

1. The user selects a file for encryption.
2. The application uses a Fernet encryption key.
3. The selected file is encrypted.
4. The encrypted file is stored with the `.enc` extension.
5. When authorized access is required, the application uses the correct key to decrypt the file.
6. The original file is restored.
7. If the encrypted file has been modified, decryption fails.

## 🔑 Encryption Algorithm

This project uses **Fernet symmetric encryption**.

- The same secret key is used for encryption and decryption.
- Fernet uses AES-128 in CBC mode with PKCS7 padding.
- HMAC-SHA256 provides authentication and integrity verification.
- A modified encrypted file or incorrect key causes decryption to fail.

## 🧪 Expected Results

| Test Case | Expected Result |
|---|---|
| Encrypt a file | Encrypted `.enc` file generated |
| Decrypt with correct key | Original file restored |
| Decrypt with incorrect key | Decryption rejected |
| Modify encrypted file | Integrity verification fails |
| Access encrypted file without key | Original content remains protected |

## ⚠️ Limitations

- This is a simulation, not a real full-disk encryption implementation.
- It does not encrypt an entire physical hard drive or operating system.
- Encryption and decryption are performed at the file level.
- The encryption key must be stored securely and backed up separately.

## 🚀 Future Enhancements

- Implement real-time transparent file encryption.
- Add user authentication and access control.
- Integrate secure key management.
- Support larger files and multiple file formats.
- Explore integration with operating-system-level storage encryption.


## 📜 Disclaimer

This project is developed for educational and academic purposes. It demonstrates encryption concepts through a simulated virtual disk environment and is not intended to replace production-grade full-disk encryption solutions.
