import os
from datetime import datetime

class InventoryGudang:
    def __init__(self):
        self.inventory = {}
        self.load_data()
    
    def clear_screen(self):
        """Membersihkan layar terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def load_data(self):
        """Memuat data inventory dari file"""
        try:
            with open('inventory.txt', 'r') as file:
                for line in file:
                    data = line.strip().split('|')
                    if len(data) == 5:
                        kode, nama, jumlah, harga, tanggal = data
                        self.inventory[kode] = {
                            'nama': nama,
                            'jumlah': int(jumlah),
                            'harga': float(harga),
                            'tanggal': tanggal
                        }
        except FileNotFoundError:
            pass
    
    def save_data(self):
        """Menyimpan data inventory ke file"""
        with open('inventory.txt', 'w') as file:
            for kode, item in self.inventory.items():
                file.write(f"{kode}|{item['nama']}|{item['jumlah']}|{item['harga']}|{item['tanggal']}\n")
    
    def tambah_barang(self):
        """Menambah barang baru ke inventory"""
        self.clear_screen()
        print("="*50)
        print("TAMBAH BARANG BARU")
        print("="*50)
        
        kode = input("Masukkan kode barang: ").upper()
        
        if kode in self.inventory:
            print(f"Barang dengan kode {kode} sudah ada!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        nama = input("Masukkan nama barang: ")
        
        try:
            jumlah = int(input("Masukkan jumlah barang: "))
            if jumlah < 0:
                print("Jumlah tidak boleh negatif!")
                input("\nTekan Enter untuk melanjutkan...")
                return
        except ValueError:
            print("Jumlah harus berupa angka!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        try:
            harga = float(input("Masukkan harga barang: "))
            if harga < 0:
                print("Harga tidak boleh negatif!")
                input("\nTekan Enter untuk melanjutkan...")
                return
        except ValueError:
            print("Harga harus berupa angka!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        self.inventory[kode] = {
            'nama': nama,
            'jumlah': jumlah,
            'harga': harga,
            'tanggal': tanggal
        }
        
        self.save_data()
        print(f"\n✓ Barang {nama} berhasil ditambahkan!")
        input("\nTekan Enter untuk melanjutkan...")
    
    def lihat_barang(self):
        """Menampilkan semua barang di inventory"""
        self.clear_screen()
        print("="*50)
        print("DAFTAR INVENTORY GUDANG")
        print("="*50)
        
        if not self.inventory:
            print("\nInventory kosong!")
        else:
            print(f"{'Kode':<10} {'Nama':<20} {'Jumlah':<10} {'Harga':<15} {'Total':<15}")
            print("-"*70)
            
            total_nilai = 0
            for kode, item in self.inventory.items():
                total = item['jumlah'] * item['harga']
                total_nilai += total
                print(f"{kode:<10} {item['nama']:<20} {item['jumlah']:<10} Rp{item['harga']:<13,.2f} Rp{total:<13,.2f}")
            
            print("-"*70)
            print(f"Total Nilai Inventory: Rp{total_nilai:,.2f}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def cari_barang(self):
        """Mencari barang berdasarkan kode atau nama"""
        self.clear_screen()
        print("="*50)
        print("CARI BARANG")
        print("="*50)
        
        keyword = input("Masukkan kode atau nama barang: ").upper()
        
        ditemukan = False
        print("\nHasil Pencarian:")
        print("-"*50)
        
        for kode, item in self.inventory.items():
            if keyword in kode or keyword.lower() in item['nama'].lower():
                ditemukan = True
                print(f"Kode      : {kode}")
                print(f"Nama      : {item['nama']}")
                print(f"Jumlah    : {item['jumlah']}")
                print(f"Harga     : Rp{item['harga']:,.2f}")
                print(f"Total     : Rp{item['jumlah'] * item['harga']:,.2f}")
                print(f"Tanggal   : {item['tanggal']}")
                print("-"*50)
        
        if not ditemukan:
            print("Barang tidak ditemukan!")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def update_barang(self):
        """Mengupdate data barang"""
        self.clear_screen()
        print("="*50)
        print("UPDATE BARANG")
        print("="*50)
        
        kode = input("Masukkan kode barang yang akan diupdate: ").upper()
        
        if kode not in self.inventory:
            print(f"Barang dengan kode {kode} tidak ditemukan!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        item = self.inventory[kode]
        print(f"\nData Barang Saat Ini:")
        print(f"Nama    : {item['nama']}")
        print(f"Jumlah  : {item['jumlah']}")
        print(f"Harga   : Rp{item['harga']:,.2f}")
        
        print("\nPilih data yang akan diupdate:")
        print("1. Nama barang")
        print("2. Jumlah barang")
        print("3. Harga barang")
        print("4. Semua data")
        
        pilihan = input("Masukkan pilihan (1-4): ")
        
        if pilihan == '1':
            nama_baru = input("Masukkan nama baru: ")
            item['nama'] = nama_baru
            print("✓ Nama barang berhasil diupdate!")
            
        elif pilihan == '2':
            try:
                jumlah_baru = int(input("Masukkan jumlah baru: "))
                if jumlah_baru >= 0:
                    item['jumlah'] = jumlah_baru
                    print("✓ Jumlah barang berhasil diupdate!")
                else:
                    print("Jumlah tidak boleh negatif!")
            except ValueError:
                print("Input tidak valid!")
                
        elif pilihan == '3':
            try:
                harga_baru = float(input("Masukkan harga baru: "))
                if harga_baru >= 0:
                    item['harga'] = harga_baru
                    print("✓ Harga barang berhasil diupdate!")
                else:
                    print("Harga tidak boleh negatif!")
            except ValueError:
                print("Input tidak valid!")
                
        elif pilihan == '4':
            nama_baru = input("Masukkan nama baru: ")
            try:
                jumlah_baru = int(input("Masukkan jumlah baru: "))
                harga_baru = float(input("Masukkan harga baru: "))
                
                if jumlah_baru >= 0 and harga_baru >= 0:
                    item['nama'] = nama_baru
                    item['jumlah'] = jumlah_baru
                    item['harga'] = harga_baru
                    print("✓ Semua data berhasil diupdate!")
                else:
                    print("Jumlah dan harga tidak boleh negatif!")
            except ValueError:
                print("Input tidak valid!")
        else:
            print("Pilihan tidak valid!")
        
        item['tanggal'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.save_data()
        input("\nTekan Enter untuk melanjutkan...")
    
    def hapus_barang(self):
        """Menghapus barang dari inventory"""
        self.clear_screen()
        print("="*50)
        print("HAPUS BARANG")
        print("="*50)
        
        kode = input("Masukkan kode barang yang akan dihapus: ").upper()
        
        if kode not in self.inventory:
            print(f"Barang dengan kode {kode} tidak ditemukan!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        item = self.inventory[kode]
        print(f"\nAnda akan menghapus barang:")
        print(f"Nama  : {item['nama']}")
        print(f"Jumlah: {item['jumlah']}")
        
        konfirmasi = input("\nYakin ingin menghapus? (y/n): ").lower()
        
        if konfirmasi == 'y':
            del self.inventory[kode]
            self.save_data()
            print("✓ Barang berhasil dihapus!")
        else:
            print("Penghapusan dibatalkan!")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def laporan_stock_rendah(self, batas=10):
        """Menampilkan barang dengan stock di bawah batas minimum"""
        self.clear_screen()
        print("="*50)
        print("LAPORAN STOCK RENDAH")
        print("="*50)
        
        try:
            batas = int(input(f"Masukkan batas minimum stock (default {batas}): ") or batas)
        except ValueError:
            batas = 10
        
        stock_rendah = False
        for kode, item in self.inventory.items():
            if item['jumlah'] <= batas:
                if not stock_rendah:
                    print(f"\nBarang dengan stock <= {batas}:")
                    print(f"{'Kode':<10} {'Nama':<20} {'Jumlah':<10} {'Status':<15}")
                    print("-"*55)
                    stock_rendah = True
                
                status = "⚠️ Stock Rendah" if item['jumlah'] <= batas else ""
                print(f"{kode:<10} {item['nama']:<20} {item['jumlah']:<10} {status}")
        
        if not stock_rendah:
            print(f"\n✓ Tidak ada barang dengan stock di bawah {batas}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def menu(self):
        """Menu utama program"""
        while True:
            self.clear_screen()
            print("="*50)
            print("     SISTEM INVENTORY GUDANG")
            print("="*50)
            print("1. ➕ Tambah Barang")
            print("2. 📋 Lihat Semua Barang")
            print("3. 🔍 Cari Barang")
            print("4. ✏️ Update Barang")
            print("5. 🗑️ Hapus Barang")
            print("6. ⚠️ Laporan Stock Rendah")
            print("7. 🚪 Keluar")
            print("="*50)
            
            pilihan = input("Masukkan pilihan (1-7): ")
            
            if pilihan == '1':
                self.tambah_barang()
            elif pilihan == '2':
                self.lihat_barang()
            elif pilihan == '3':
                self.cari_barang()
            elif pilihan == '4':
                self.update_barang()
            elif pilihan == '5':
                self.hapus_barang()
            elif pilihan == '6':
                self.laporan_stock_rendah()
            elif pilihan == '7':
                self.clear_screen()
                print("Terima kasih telah menggunakan program ini!")
                break
            else:
                print("Pilihan tidak valid!")
                input("Tekan Enter untuk melanjutkan...")

def main():
    """Fungsi utama untuk menjalankan program"""
    program = InventoryGudang()
    program.menu()

if __name__ == "__main__":
    main()