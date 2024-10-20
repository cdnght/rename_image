import os
import zipfile
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

class PNGExtractorApp:
    def init(self, root):
        self.root = root
        self.root.title("PNG Extractor")
        self.root.geometry("400x400")
        self.root.config(bg="white")

        # Tombol untuk memilih direktori file ZIP
        self.select_button = tk.Button(self.root, text="Pilih Direktori File ZIP", command=self.select_directory)
        self.select_button.pack(pady=20)

        # Kolom untuk menampilkan direktori file ZIP (awalnya disembunyikan)
        self.directory_label = tk.Label(self.root, text="Direktori File ZIP:")
        self.directory_text = tk.Text(self.root, height=10, width=40)
        self.directory_text.pack_forget()  # Menyembunyikan kolom

        # Tombol untuk mengekstrak file
        self.extract_button = tk.Button(self.root, text="Ekstrak dan Rename PNG", command=self.extract_png)
        self.extract_button.pack(pady=20)

        # Tombol Close
        self.close_button = tk.Button(self.root, text="Tutup", command=self.root.quit)
        self.close_button.pack(pady=20)

        self.zip_files = []
        self.time_dict = {}

    def select_directory(self):
        directory = filedialog.askdirectory(title="Pilih Direktori File ZIP")
        if directory:
            self.zip_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.zip')]
            if self.zip_files:
                self.directory_text.pack()  # Menampilkan kolom jika ada file ZIP
                self.directory_text.delete(1.0, tk.END)
                for file in self.zip_files:
                    self.directory_text.insert(tk.END, file + "\n")
                messagebox.showinfo("Info", f"{len(self.zip_files)} file ZIP terdeteksi.")
            else:
                messagebox.showwarning("Peringatan", "Tidak ada file ZIP ditemukan di direktori yang dipilih.")

    def extract_png(self):
        if not self.zip_files:
            messagebox.showwarning("Peringatan", "Silakan pilih direktori file ZIP terlebih dahulu.")
            return
        
        output_dir = os.path.join(os.getcwd(), "extracted_pngs")
        os.makedirs(output_dir, exist_ok=True)

        for zip_file in self.zip_files:
            mod_time = os.path.getmtime(zip_file)
            time_key = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')

            if time_key not in self.time_dict:
                self.time_dict[time_key] = 1  # Inisialisasi hitungan
            else:
                self.time_dict[time_key] += 1
            
            section_number = self.time_dict[time_key]
            if section_number > 10:
                continue  # Hanya proses sampai 10 file

            with zipfile.ZipFile(zip_file, 'r') as z:
                png_files = [f for f in z.namelist() if f.endswith('.png')]
                for i, file in enumerate(png_files):
                    if i < 10:  # Hanya ambil 10 file PNG
                        new_name = f"section{section_number}image{i+1}.png"
                        z.extract(file, output_dir)
                        os.rename(os.path.join(output_dir, file), os.path.join(output_dir, new_name))

        messagebox.showinfo("Info", "Proses ekstraksi dan rename selesai.")

if name == "main":
    root = tk.Tk()
    app = PNGExtractorApp(root)
    root.mainloop()
