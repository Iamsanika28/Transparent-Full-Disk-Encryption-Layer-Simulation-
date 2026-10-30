
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

BASE_DIR = Path(__file__).resolve().parent
KEY_FILE = BASE_DIR / "keys" / "fernet.key"
ENCRYPTED_DIR = BASE_DIR / "storage" / "encrypted_files"
DECRYPTED_DIR = BASE_DIR / "decrypted"

ENCRYPTED_DIR.mkdir(parents=True, exist_ok=True)
DECRYPTED_DIR.mkdir(parents=True, exist_ok=True)

def get_cipher():
    if not KEY_FILE.exists():
        KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        KEY_FILE.write_bytes(Fernet.generate_key())
    return Fernet(KEY_FILE.read_bytes())

def encrypt_file():
    filename = filedialog.askopenfilename(
        title="Choose a file to encrypt",
        initialdir=str(BASE_DIR / "storage")
    )
    if not filename:
        return

    source = Path(filename)
    try:
        encrypted = get_cipher().encrypt(source.read_bytes())
        output = ENCRYPTED_DIR / (source.name + ".enc")
        output.write_bytes(encrypted)
        messagebox.showinfo(
            "Success",
            f"File encrypted successfully!\n\nSaved to:\n{output}"
        )
        status.config(text=f"Encrypted: {source.name}")
    except OSError as error:
        messagebox.showerror("Error", str(error))

def decrypt_file():
    filename = filedialog.askopenfilename(
        title="Choose an encrypted .enc file",
        initialdir=str(ENCRYPTED_DIR),
        filetypes=[("Encrypted files", "*.enc")]
    )
    if not filename:
        return

    source = Path(filename)
    try:
        plaintext = get_cipher().decrypt(source.read_bytes())
        output_name = source.name[:-4]
        output = DECRYPTED_DIR / output_name

        if output.exists():
            overwrite = messagebox.askyesno(
                "File exists",
                f"{output.name} already exists. Overwrite it?"
            )
            if not overwrite:
                return

        output.write_bytes(plaintext)
        messagebox.showinfo(
            "Success",
            f"File decrypted successfully!\n\nRecovered to:\n{output}"
        )
        status.config(text=f"Decrypted: {output.name}")
    except InvalidToken:
        messagebox.showerror(
            "Decryption failed",
            "The key is incorrect or the encrypted file was modified."
        )
    except OSError as error:
        messagebox.showerror("Error", str(error))

root = tk.Tk()
root.title("SecureDisk - Encryption Simulation")
root.geometry("520x360")
root.resizable(False, False)
root.configure(bg="#101827")

title = tk.Label(
    root,
    text="SecureDisk",
    font=("Segoe UI", 25, "bold"),
    fg="#60A5FA",
    bg="#101827"
)
title.pack(pady=(25, 5))

subtitle = tk.Label(
    root,
    text="File Encryption & Decryption Simulation",
    font=("Segoe UI", 11),
    fg="white",
    bg="#101827"
)
subtitle.pack(pady=(0, 25))

encrypt_button = tk.Button(
    root,
    text="Encrypt a File",
    command=encrypt_file,
    font=("Segoe UI", 12, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    width=25,
    pady=8
)
encrypt_button.pack(pady=8)

decrypt_button = tk.Button(
    root,
    text="Decrypt a File",
    command=decrypt_file,
    font=("Segoe UI", 12, "bold"),
    bg="#059669",
    fg="white",
    activebackground="#047857",
    width=25,
    pady=8
)
decrypt_button.pack(pady=8)

status = tk.Label(
    root,
    text="Ready",
    font=("Segoe UI", 10),
    fg="#D1D5DB",
    bg="#101827"
)
status.pack(pady=18)

root.mainloop()
