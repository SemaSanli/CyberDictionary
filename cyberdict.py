import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Veritabanı bağlantısı ve tablo oluşturma
conn = sqlite3.connect('sozluk.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sozluk (
                kelime TEXT PRIMARY KEY,
                anlam TEXT NOT NULL)''')
conn.commit()

# Sözlük yapısı
sozluk = {}

# Veritabanından kelimeleri yükleme fonksiyonu
def kelimeleri_yukle():
    c.execute("SELECT * FROM sozluk")
    rows = c.fetchall()
    for row in rows:
        sozluk[row[0]] = row[1]
    guncelle_liste()

# Kelime arama fonksiyonu
def kelime_arama():
    kelime = kelime_giris.get().strip().lower()
    if kelime in sozluk:
        sonuc_var.set(f"{kelime}: {sozluk[kelime]}")
    else:
        sonuc_var.set(f"'{kelime}' kelimesi sözlükte bulunamadı.")
    guncelle_liste()

# Listeyi güncelleme fonksiyonu
def guncelle_liste():
    for row in tree.get_children():
        tree.delete(row)
    for kelime, anlam in sozluk.items():
        tree.insert('', 'end', values=(kelime, anlam))

# Yeni kelime ekleme fonksiyonu
def kelime_ekle():
    yeni_kelime = yeni_kelime_giris.get().strip().lower()
    yeni_anlam = yeni_anlam_giris.get().strip()
    if yeni_kelime and yeni_anlam:
        if yeni_kelime in sozluk:
            messagebox.showerror("Hata", "Bu kelime zaten sözlükte mevcut!")
        else:
            sozluk[yeni_kelime] = yeni_anlam
            c.execute("INSERT INTO sozluk (kelime, anlam) VALUES (?, ?)", (yeni_kelime, yeni_anlam))
            conn.commit()
            messagebox.showinfo("Başarılı", "Kelime başarıyla eklendi!")
            guncelle_liste()
    else:
        messagebox.showerror("Hata", "Kelime ve anlamı boş olamaz!")

# Kelime silme fonksiyonu
def kelime_sil():
    secili_kelime = tree.selection()
    if secili_kelime:
        kelime = tree.item(secili_kelime)['values'][0]
        del sozluk[kelime]
        c.execute("DELETE FROM sozluk WHERE kelime = ?", (kelime,))
        conn.commit()
        messagebox.showinfo("Başarılı", "Kelime başarıyla silindi!")
        guncelle_liste()
    else:
        messagebox.showerror("Hata", "Silmek için bir kelime seçmelisiniz!")

# Ana pencere
pencere = tk.Tk()
pencere.title("CyberDict")
pencere.state('zoomed')  # Pencereyi tam ekran yapma
pencere.configure(bg="#230035")

# Stil oluşturma
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#6E7B8B", foreground="white")
style.configure("Treeview", font=('Arial', 11), rowheight=25, background="#ecf0f1", foreground="#2c3e50", fieldbackground="#ecf0f1")
style.configure("TLabel", background="#2c3e50", foreground="white", font=('Arial', 11))
style.configure("TButton", font=('Arial', 11), background="#1abc9c", foreground="white", relief="flat")
style.map('TButton', background=[('active', '#16a085')], foreground=[('active', 'white')])

# Başlık ve açıklama
tk.Label(pencere, text="CyberDict", font=('Arial', 24, 'bold'), bg="#230035", fg="white").grid(row=0, column=0, columnspan=3, pady=(20, 10))
tk.Label(pencere, text="Bu program ile siber güvenlikte kullanılan komutların anlamlarını arayabilir, yeni kelimeler ekleyebilir ve silerek kendi sözlüğünüzü oluşturabilirsiniz.", font=('Arial', 14), bg="#230035", fg="white").grid(row=1, column=0, columnspan=3, pady=(0, 20))

# Kelime girişi
tk.Label(pencere, text="Kelime:", font=('Arial', 14), bg="#230035", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky='e')
kelime_giris = tk.Entry(pencere, font=('Arial', 14))
kelime_giris.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Sonuç etiketi
sonuc_var = tk.StringVar()
tk.Label(pencere, textvariable=sonuc_var, font=('Arial', 14), bg="#230035", fg="white").grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Arama butonu
tk.Button(pencere, text="Ara", command=kelime_arama, font=('Arial', 12), bg="#6E7B8B", fg="white", relief="flat").grid(row=2, column=2, padx=10, pady=10)


# Ekle ve Sil butonları
ekle_buton = tk.Button(pencere, text="Ekle", command=kelime_ekle, font=('Arial', 12), bg="#6E7B8B", fg="white", relief="flat")
ekle_buton.grid(row=5, column=2, padx=10, pady=10, sticky='e')
sil_buton = tk.Button(pencere, text="Sil", command=kelime_sil, font=('Arial', 12), bg="#6E7B8B", fg="white", relief="flat")
sil_buton.grid(row=6, column=2, padx=10, pady=10, sticky='e')

# Treeview ile kelime ve anlamlarını gösteren tablo
tree_frame = tk.Frame(pencere)
tree_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree = ttk.Treeview(tree_frame, columns=('Kelime', 'Anlam'), show='headings', yscrollcommand=tree_scroll.set)
tree.heading('Kelime', text='Kelime')
tree.heading('Anlam', text='Anlam')
tree.column('Kelime', width=150)
tree.column('Anlam', width=400)
tree.pack(expand=True, fill='both')
tree_scroll.config(command=tree.yview)

# Pencere boyutlarını ayarlama
pencere.grid_rowconfigure(4, weight=1)
pencere.grid_columnconfigure(1, weight=1)

# Yeni kelime ekleme alanları
tk.Label(pencere, text="Yeni Kelime:", font=('Arial', 14), bg="#230035", fg="white").grid(row=5, column=0, padx=10, pady=10, sticky='e')
yeni_kelime_giris = tk.Entry(pencere, font=('Arial', 14))
yeni_kelime_giris.grid(row=5, column=1, padx=10, pady=10, sticky='w')

tk.Label(pencere, text="Anlam:", font=('Arial', 14), bg="#230035", fg="white").grid(row=6, column=0, padx=10, pady=10, sticky='e')
yeni_anlam_giris = tk.Entry(pencere, font=('Arial', 14))
yeni_anlam_giris.grid(row=6, column=1, padx=10, pady=10, sticky='w')

# Pencereyi çalıştır
kelimeleri_yukle()  # Başlangıçta veritabanından kelimeleri yükle
pencere.mainloop()

# Program kapandığında veritabanı bağlantısını kapatma
conn.close()