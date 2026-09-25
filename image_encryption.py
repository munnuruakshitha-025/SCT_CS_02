import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PixelShield - Image Encryption Tool")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)
        self.root.configure(bg="#0f172a")

        self.original_image = None
        self.processed_image = None
        self.image_path = None

        self.key_var = tk.IntVar(value=50)
        self.status_var = tk.StringVar(value="Ready")

        self.build_ui()

    # ---------------- IMAGE PROCESSING ----------------

    def encrypt_image(self):
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please select an image first.")
            return

        key = self.key_var.get()

        image = self.original_image.convert("RGB")
        pixels = image.load()

        width, height = image.size

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]

                r = (r + key) % 256
                g = (g + key) % 256
                b = (b + key) % 256

                pixels[x, y] = (r, g, b)

        self.processed_image = image
        self.display_image(image, self.output_label)

        self.status_var.set("Image encrypted successfully.")

    def decrypt_image(self):
        if self.processed_image is None:
            messagebox.showwarning(
                "No Encrypted Image",
                "Please encrypt an image first."
            )
            return

        key = self.key_var.get()

        image = self.processed_image.copy()
        pixels = image.load()

        width, height = image.size

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]

                r = (r - key) % 256
                g = (g - key) % 256
                b = (b - key) % 256

                pixels[x, y] = (r, g, b)

        self.processed_image = image
        self.display_image(image, self.output_label)

        self.status_var.set("Image decrypted successfully.")

    # ---------------- FILE OPERATIONS ----------------

    def select_image(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        try:
            image = Image.open(path).convert("RGB")

            self.original_image = image
            self.processed_image = None
            self.image_path = path

            self.display_image(image, self.input_label)

            self.output_label.config(
                image="",
                text="Encrypted / Decrypted image\nwill appear here"
            )

            self.status_var.set("Image loaded successfully.")

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Unable to open image.\n\n{e}"
            )

    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning(
                "No Output",
                "Please encrypt or decrypt an image first."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Save Processed Image",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        try:
            self.processed_image.save(path)
            self.status_var.set("Image saved successfully.")

            messagebox.showinfo(
                "Saved",
                "Processed image saved successfully."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Unable to save image.\n\n{e}"
            )

    # ---------------- DISPLAY ----------------

    def display_image(self, image, label):
        preview = image.copy()

        preview.thumbnail((380, 360))

        photo = ImageTk.PhotoImage(preview)

        label.config(image=photo, text="")
        label.image = photo

    # ---------------- CLEAR ----------------

    def clear_all(self):
        self.original_image = None
        self.processed_image = None
        self.image_path = None

        self.input_label.config(
            image="",
            text="Select an image to begin"
        )

        self.output_label.config(
            image="",
            text="Encrypted / Decrypted image\nwill appear here"
        )

        self.key_var.set(50)
        self.status_var.set("Ready")

    # ---------------- UI ----------------

    def build_ui(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#111827",
            height=100
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="PIXELSHIELD",
            font=("Segoe UI", 25, "bold"),
            fg="#38bdf8",
            bg="#111827"
        ).pack(anchor="w", padx=35, pady=(18, 0))

        tk.Label(
            header,
            text="Image Encryption & Decryption using Pixel Manipulation",
            font=("Segoe UI", 11),
            fg="#cbd5e1",
            bg="#111827"
        ).pack(anchor="w", padx=37)

        # Main area
        main = tk.Frame(
            self.root,
            bg="#0f172a"
        )
        main.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        # Image panels
        panels = tk.Frame(
            main,
            bg="#0f172a"
        )
        panels.pack(
            fill="both",
            expand=True
        )

        # Input panel
        left = tk.Frame(
            panels,
            bg="#1e293b"
        )
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            left,
            text="ORIGINAL IMAGE",
            font=("Segoe UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#1e293b"
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 10)
        )

        self.input_label = tk.Label(
            left,
            text="Select an image to begin",
            font=("Segoe UI", 11),
            fg="#64748b",
            bg="#0b1220"
        )
        self.input_label.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 14)
        )

        # Output panel
        right = tk.Frame(
            panels,
            bg="#1e293b"
        )
        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            right,
            text="PROCESSED IMAGE",
            font=("Segoe UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#1e293b"
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 10)
        )

        self.output_label = tk.Label(
            right,
            text="Encrypted / Decrypted image\nwill appear here",
            font=("Segoe UI", 11),
            fg="#64748b",
            bg="#0b1220"
        )
        self.output_label.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 14)
        )

        # Controls
        controls = tk.Frame(
            main,
            bg="#0f172a"
        )
        controls.pack(
            fill="x",
            pady=(18, 0)
        )

        # Select button
        tk.Button(
            controls,
            text="SELECT IMAGE",
            command=self.select_image,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#0284c7",
            activebackground="#0284c7",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=11,
            cursor="hand2"
        ).pack(
            side="left",
            padx=4
        )

        # Key
        key_frame = tk.Frame(
            controls,
            bg="#1e293b"
        )
        key_frame.pack(
            side="left",
            padx=10
        )

        tk.Label(
            key_frame,
            text="KEY",
            font=("Segoe UI", 10, "bold"),
            fg="#94a3b8",
            bg="#1e293b"
        ).pack(
            side="left",
            padx=(12, 6),
            pady=10
        )

        tk.Spinbox(
            key_frame,
            from_=1,
            to=255,
            textvariable=self.key_var,
            width=5,
            font=("Segoe UI", 12, "bold"),
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            buttonbackground="#334155",
            relief="flat"
        ).pack(
            side="left",
            padx=(0, 12),
            pady=10
        )

        # Encrypt
        tk.Button(
            controls,
            text="ENCRYPT",
            command=self.encrypt_image,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#7c3aed",
            activebackground="#7c3aed",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=11,
            cursor="hand2"
        ).pack(
            side="left",
            padx=4
        )

        # Decrypt
        tk.Button(
            controls,
            text="DECRYPT",
            command=self.decrypt_image,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#059669",
            activebackground="#059669",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=11,
            cursor="hand2"
        ).pack(
            side="left",
            padx=4
        )

        # Save
        tk.Button(
            controls,
            text="SAVE",
            command=self.save_image,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#334155",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=11,
            cursor="hand2"
        ).pack(
            side="left",
            padx=4
        )

        # Clear
        tk.Button(
            controls,
            text="CLEAR",
            command=self.clear_all,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#475569",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=11,
            cursor="hand2"
        ).pack(
            side="left",
            padx=4
        )

        # Footer
        footer = tk.Frame(
            self.root,
            bg="#111827",
            height=45
        )
        footer.pack(
            fill="x",
            side="bottom"
        )
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="●",
            font=("Segoe UI", 10),
            fg="#22c55e",
            bg="#111827"
        ).pack(
            side="left",
            padx=(30, 6),
            pady=13
        )

        tk.Label(
            footer,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            fg="#cbd5e1",
            bg="#111827"
        ).pack(
            side="left",
            pady=13
        )

        tk.Label(
            footer,
            text="SkillCraft Technology • Task 02",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#111827"
        ).pack(
            side="right",
            padx=30
        )


# ---------------- MAIN ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()