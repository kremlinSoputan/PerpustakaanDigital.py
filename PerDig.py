import json
import os

# membersihkan layar
def clear_screen():
    os.system("CLS")

# menampilkan menu utama
def menu():
    clear_screen()
    print("   SELAMAT DATANG DI PROGRAM PERPUSTAKAAN DIGITAL  ")
    print("=====================================================")
    print("\nPilih Daftar Menu Untuk Mengakses Program :\n")
    print("[1] Tambah Buku")
    print("[2] Hapus Buku")
    print("[3] Cari Buku") 
    print("[4] Pinjam Buku") 
    print("[5] Kembalikan Buku") 
    print("[6] Tampilkan Buku yang Sedang Dipinjam") 
    print("[7] Simpan Data Buku") 
    print("[8] Keluar") 

    kode = int(input("\nPilih Menu 1-8 : "))
    pilihmenu(kode)

# memilih menu berdasarkan input pengguna
def pilihmenu(p):
    if p == 1:
        tambah_buku()
    elif p == 2:
        hapus_buku()
    elif p == 3:
        cari_buku()
    elif p == 4:
        pinjam_buku()
    elif p == 5:
        kembalikan_buku()
    elif p == 6:
        tampilkan_buku_dipinjam()
    elif p == 7:
        simpan_data_buku()
    elif p == 8:
        print("\n[Anda telah keluar dari program]")
    else:
        print("\n[kode yang anda masukkan tidak valid!]")

# membaca data buku dari file JSON
def baca_data_buku():
    try:
        with open("perdig.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Mengembalikan list kosong jika file tidak ada
    except json.JSONDecodeError:
        return []  # Mengembalikan list kosong jika file rusak

# menulis data buku ke file JSON
def tulis_data_buku(buku_data):
    with open("perdig.json", "w") as file:
        json.dump(buku_data, file, indent=4)

# menambahkan buku
def tambah_buku():
    clear_screen()
    print("\n      - Tambah Buku -")
    print("\nMasukkan data buku baru")
    judul = input("Judul Buku: ")
    penulis = input("Penulis Buku: ")
    tahun = input("Tahun Terbit: ")
    kategori = input("Kategori: ")

    buku_data = baca_data_buku()  # Membaca data buku yang sudah ada
    buku_data.append({
        "judul": judul,
        "penulis": penulis,
        "tahun": tahun,
        "kategori": kategori,
        "dipinjam": "tidak"
    })
    
    tulis_data_buku(buku_data)  # Menyimpan data buku yang baru
    print("\n[Data Buku Berhasil Ditambahkan]")

    lagi = input("\nIngin menambahkan buku lagi? (Ya/Tidak): ").lower()
    if lagi == "ya":
        tambah_buku()
    else:
        input("\nTekan [ENTER] untuk kembali ke menu.")
        menu()

# menghapus buku
def hapus_buku():
    clear_screen()
    print("\n          - Hapus Buku -")
    judul = input("Masukkan judul buku yang ingin dihapus: ")

    buku_data = baca_data_buku()
    buku_data = [buku for buku in buku_data if buku["judul"].lower() != judul.lower()]

    tulis_data_buku(buku_data)
    print("\n[Data Buku Telah Terhapus]")

    lagi = input("\nIngin menghapus buku lagi? (Ya/Tidak): ").lower()
    if lagi == "ya":
        hapus_buku()
    else:
        input("\nTekan [ENTER] untuk kembali ke menu.")
        menu()

# mencari buku
def cari_buku():
    clear_screen()
    print("\n       - Cari Buku -")
    judul = input("Masukkan judul buku yang ingin dicari: ")

    buku_data = baca_data_buku()
    hasil_cari = [buku for buku in buku_data if judul.lower() in buku["judul"].lower()]

    if hasil_cari:
        for buku in hasil_cari:
            print(f"Judul: {buku['judul']}, Penulis: {buku['penulis']}, Tahun: {buku['tahun']}, Kategori: {buku['kategori']}")
    else:
        print("\nBuku tidak ditemukan.")

    input("\nTekan [ENTER] untuk kembali ke menu.")
    menu()

# menampilkan buku yang sedang dipinjam
def tampilkan_buku_dipinjam():
    clear_screen()
    print("\n       - Buku yang Sedang Dipinjam -")
    buku_data = baca_data_buku()
    buku_dipinjam = [buku for buku in buku_data if buku["dipinjam"] == "ya"]

    if buku_dipinjam:
        for buku in buku_dipinjam:
            print(f"Judul: {buku['judul']}, penulis: {buku['penulis']}, tahun: {buku['tahun']} Kategori: {buku['kategori']}")
    else:
        print("\nTidak ada buku yang sedang dipinjam.")

    input("\nTekan [ENTER] untuk kembali ke menu.")
    menu()

# pinjam buku
def pinjam_buku():
    clear_screen()
    print("\n       - Pinjam Buku -")
    judul = input("Masukkan judul buku yang ingin dipinjam: ")

    buku_data = baca_data_buku()
    buku_dipinjam = False

    for buku in buku_data:
        if buku["judul"].lower() == judul.lower():
            if buku["dipinjam"] == "ya":
                print(f"\nBuku '{judul}' sudah dipinjam.")
                buku_dipinjam = True
                break
            buku["dipinjam"] = "ya"  
            buku_dipinjam = True
            break

    if buku_dipinjam:
        tulis_data_buku(buku_data)
        print(f"\nBuku '{judul}' berhasil dipinjam")
    else:
        print("\nBuku tidak ditemukan atau sudah dipinjam.")

    input("\nTekan [ENTER] untuk kembali ke menu.")
    menu()

# kembalikan buku
def kembalikan_buku():
    clear_screen()
    print("\n       - Kembalikan Buku -")
    judul = input("Masukkan judul buku yang ingin dikembalikan: ")

    buku_data = baca_data_buku()
    buku_dikembalikan = False

    for buku in buku_data:
        if buku["judul"].lower() == judul.lower() and buku["dipinjam"] == "ya":
            buku["dipinjam"] = "tidak"
            buku_dikembalikan = True
            break

    if buku_dikembalikan:
        tulis_data_buku(buku_data)
        print(f"\nBuku '{judul}' telah berhasil dikembalikan.")
    else:
        print("\nBuku tidak ditemukan atau belum dipinjam.")

    input("\nTekan [ENTER] untuk kembali ke menu.")
    menu()

# menyimpan data buku
def simpan_data_buku():
    print("\n[Data Buku Sudah Tersimpan secara otomatis saat perubahan].")
    input("\nTekan [ENTER] untuk kembali ke menu.")
    menu()

# jalankan program
menu()
