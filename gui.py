
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from encryption_layer import TransparentEncryptionLayer

BASE_DIR = Path(__file__).resolve().parent
disk = TransparentEncryptionLayer(BASE_DIR)
DECRYPTED_DIR = BASE_DIR / "decrypted"
DECRYPTED_DIR.mkdir(exist_ok=True)


def save_to_virtual_disk():
    filename = filedialog.askopenfilename(
        title="Choose a file to save securely"
    )
    if not filename:
        return

    source = Path(filename)

    try:
        data = source.read_bytes()
        disk.write_file(source.name, data)

        status.config(text=f"Encrypted on virtual disk: {source.name}")
        messagebox.showinfo(
            "Success",
            f"File encrypted and saved to the virtual disk.\n\n"
            f"Original file: {source.name}\n"
            f"Stored data: virtual_disk"
        )
    except (OSError, ValueError, TypeError) as error:
        messagebox.showerror("Error", str(error))


def read_from_virtual_disk():
    filename = name_entry.get().strip()

    if not filename:
        messagebox.showwarning(
            "Filename required",
            "Enter the original filename, such as sample.txt."
        )
        return

    try:
        data = disk.read_file(filename)
        output = DECRYPTED_DIR / filename

        if output.exists():
            overwrite = messagebox.askyesno(
                "File exists",
                f"{output.name} already exists. Overwrite it?"
            )
            if not overwrite:
                return

        output.write_bytes(data)
        status.config(text=f"Decrypted from virtual disk: {filename}")

        messagebox.showinfo(
            "Success",
            f"File decrypted successfully.\n\nRecovered file:\n{output}"
        )
    except (OSError, ValueError) as error:
        messagebox.showerror("Error", str(error))


root = tk.Tk()
root.title("SecureDisk - Transparent Encryption Simulation")
root.geometry("540x400")
root.resizable(False, False)
root.configure(bg="#101827")

tk.Label(
    root,
    text="SecureDisk",
    font=("Segoe UI", 25, "bold"),
    fg="#60A5FA",
    bg="#101827"
).pack(pady=(22, 5))

tk.Label(
    root,
    text="Transparent Encrypted Virtual Storage",
    font=("Segoe UI", 11),
    fg="white",
    bg="#101827"
).pack(pady=(0, 18))

tk.Button(
    root,
    text="Save File to Virtual Disk (Encrypt)",
    command=save_to_virtual_disk,
    font=("Segoe UI", 11, "bold"),
    bg="#2563EB",
    fg="white",
    width=34,
    pady=7
).pack(pady=7)

tk.Label(
    root,
    text="Enter the original filename to read:",
    font=("Segoe UI", 10),
    fg="white",
    bg="#101827"
).pack(pady=(12, 4))

name_entry = tk.Entry(root, font=("Segoe UI", 11), width=34)
name_entry.pack(pady=4)

tk.Button(
    root,
    text="Read File from Virtual Disk (Decrypt)",
    command=read_from_virtual_disk,
    font=("Segoe UI", 11, "bold"),
    bg="#059669",
    fg="white",
    width=34,
    pady=7
).pack(pady=8)

status = tk.Label(
    root,
    text="Ready",
    font=("Segoe UI", 9),
    fg="#D1D5DB",
    bg="#101827"
)
status.pack(pady=12)

root.mainloop()
