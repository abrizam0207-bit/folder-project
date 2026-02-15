import os
import json
from datetime import datetime
from tabulate import tabulate

class InventoryGudang:
    def __init__(self):
        self.inventory = {}
        self.transaksi = []
        self.load_data()
    
    def clear_screen(self):
        """Membersihkan layar terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def load_data(self):
        """Memuat data inventory dan transaksi dari file"""
        # Load inventory
        try:
            with open('inventory_data.json', 'r') as file:
                data = json.load(file)
                self.inventory = data.get('inventory', {})
                self.transaksi = data.get('transaksi', [])
        except FileNotFoundError:
            self.inventory = {}
            self.transaksi = []
    
    def save_data(self):
        """Menyimpan data inventory dan transaksi ke file"""
        data = {
            'inventory': self.inventory,
            'transaksi': self.transaksi
        }
        with open('inventory_data.json', 'w') as file:
            json.dump(data, file, indent=4)
    
    def format_rupiah(self, nilai):
        """Format angka ke format rupiah"""
        return f"Rp {nilai:,.0f}".replace(',', '.')
    
    # ============= FUNGSI MANAJEMEN BARANG =============
    
    def tambah_barang(self):
        """Menambah barang baru ke inventory"""
        self.clear_screen()
        print("="*60)
        print("             TAMBAH BARANG BARU")
        print("="*60)
        
        kode = input("Masukkan kode barang: ").upper()
        
        if kode in self.inventory:
            print(f"\n❌ Barang dengan kode {kode} sudah ada!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        nama = input("Masukkan nama barang: ")
        kategori = input("Masukkan kategori barang: ")
        satuan = input("Masukkan satuan barang (pcs/box/liter/dll): ")
        
        try:
            harga_beli = float(input("Masukkan harga beli: "))
            harga_jual = float(input("Masukkan harga jual: "))
            stock_minimum = int(input("Masukkan batas stock minimum: "))
            
            if harga_beli < 0 or harga_jual < 0 or stock_minimum < 0:
                print("\n❌ Nilai tidak boleh negatif!")
                input("\nTekan Enter untuk melanjutkan...")
                return
        except ValueError:
            print("\n❌ Input harus berupa angka!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        lokasi = input("Masukkan lokasi penyimpanan (rak/gudang): ")
        supplier = input("Masukkan nama supplier: ")
        tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        self.inventory[kode] = {
            'nama': nama,
            'kategori': kategori,
            'satuan': satuan,
            'stock': 0,
            'harga_beli': harga_beli,
            'harga_jual': harga_jual,
            'stock_minimum': stock_minimum,
            'lokasi': lokasi,
            'supplier': supplier,
            'tanggal_daftar': tanggal,
            'terakhir_update': tanggal
        }
        
        self.save_data()
        print(f"\n✅ Barang {nama} berhasil didaftarkan!")
        input("\nTekan Enter untuk melanjutkan...")
    
    # ============= FUNGSI PEMASUKKAN BARANG =============
    
    def pemasukkan_barang(self):
        """Mencatat pemasukkan/penambahan stock barang"""
        self.clear_screen()
        print("="*60)
        print("             PEMASUKKAN BARANG")
        print("="*60)
        
        kode = input("Masukkan kode barang: ").upper()
        
        if kode not in self.inventory:
            print(f"\n❌ Barang dengan kode {kode} tidak ditemukan!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        barang = self.inventory[kode]
        print(f"\n📦 Data Barang:")
        print(f"Nama Barang   : {barang['nama']}")
        print(f"Stock Saat Ini: {barang['stock']} {barang['satuan']}")
        print(f"Harga Beli    : {self.format_rupiah(barang['harga_beli'])}")
        print(f"Lokasi        : {barang['lokasi']}")
        
        try:
            jumlah = int(input(f"\nMasukkan jumlah {barang['satuan']} yang masuk: "))
            if jumlah <= 0:
                print("\n❌ Jumlah harus lebih dari 0!")
                input("\nTekan Enter untuk melanjutkan...")
                return
            
            harga_beli_baru = input(f"Masukkan harga beli baru (Enter jika tetap {self.format_rupiah(barang['harga_beli'])}): ")
            if harga_beli_baru.strip():
                harga_beli_baru = float(harga_beli_baru)
                if harga_beli_baru > 0:
                    barang['harga_beli'] = harga_beli_baru
            
            nomor_batch = input("Masukkan nomor batch (opsional): ")
            tanggal_expired = input("Masukkan tanggal expired (DD-MM-YYYY, opsional): ")
            
        except ValueError:
            print("\n❌ Input tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        # Update stock
        stock_lama = barang['stock']
        barang['stock'] += jumlah
        barang['terakhir_update'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Catat transaksi
        transaksi = {
            'id': f"IN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'jenis': 'PEMASUKKAN',
            'kode_barang': kode,
            'nama_barang': barang['nama'],
            'jumlah': jumlah,
            'satuan': barang['satuan'],
            'stock_sebelum': stock_lama,
            'stock_sesudah': barang['stock'],
            'harga_beli': barang['harga_beli'],
            'nomor_batch': nomor_batch if nomor_batch else '-',
            'tanggal_expired': tanggal_expired if tanggal_expired else '-',
            'keterangan': 'Pembelian stok',
            'waktu': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'user': 'admin'
        }
        
        self.transaksi.append(transaksi)
        self.save_data()
        
        print(f"\n✅ Berhasil menambahkan {jumlah} {barang['satuan']} {barang['nama']}")
        print(f"   Stock sekarang: {barang['stock']} {barang['satuan']}")
        input("\nTekan Enter untuk melanjutkan...")
    
    # ============= FUNGSI PENGELUARAN BARANG =============
    
    def pengeluaran_barang(self):
        """Mencatat pengeluaran/pengurangan stock barang"""
        self.clear_screen()
        print("="*60)
        print("             PENGELUARAN BARANG")
        print("="*60)
        
        kode = input("Masukkan kode barang: ").upper()
        
        if kode not in self.inventory:
            print(f"\n❌ Barang dengan kode {kode} tidak ditemukan!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        barang = self.inventory[kode]
        print(f"\n📦 Data Barang:")
        print(f"Nama Barang   : {barang['nama']}")
        print(f"Stock Tersedia: {barang['stock']} {barang['satuan']}")
        print(f"Harga Jual    : {self.format_rupiah(barang['harga_jual'])}")
        
        if barang['stock'] <= 0:
            print("\n⚠️ Stock barang kosong!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        try:
            jumlah = int(input(f"\nMasukkan jumlah {barang['satuan']} yang keluar: "))
            if jumlah <= 0:
                print("\n❌ Jumlah harus lebih dari 0!")
                input("\nTekan Enter untuk melanjutkan...")
                return
            
            if jumlah > barang['stock']:
                print(f"\n❌ Stock tidak mencukupi! Tersedia: {barang['stock']} {barang['satuan']}")
                input("\nTekan Enter untuk melanjutkan...")
                return
            
            tujuan = input("Masukkan tujuan pengeluaran: ")
            penerima = input("Masukkan nama penerima: ")
            no_po = input("Masukkan nomor PO (opsional): ")
            
        except ValueError:
            print("\n❌ Input tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        # Update stock
        stock_lama = barang['stock']
        barang['stock'] -= jumlah
        barang['terakhir_update'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Hitung total
        total_harga = jumlah * barang['harga_jual']
        
        # Catat transaksi
        transaksi = {
            'id': f"OUT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'jenis': 'PENGELUARAN',
            'kode_barang': kode,
            'nama_barang': barang['nama'],
            'jumlah': jumlah,
            'satuan': barang['satuan'],
            'stock_sebelum': stock_lama,
            'stock_sesudah': barang['stock'],
            'harga_jual': barang['harga_jual'],
            'total_harga': total_harga,
            'tujuan': tujuan,
            'penerima': penerima,
            'no_po': no_po if no_po else '-',
            'waktu': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'user': 'admin'
        }
        
        self.transaksi.append(transaksi)
        self.save_data()
        
        print(f"\n✅ Berhasil mengeluarkan {jumlah} {barang['satuan']} {barang['nama']}")
        print(f"   Stock sekarang: {barang['stock']} {barang['satuan']}")
        print(f"   Total nilai: {self.format_rupiah(total_harga)}")
        
        # Cek stock minimum
        if barang['stock'] <= barang['stock_minimum']:
            print(f"\n⚠️ PERINGATAN: Stock sudah mencapai batas minimum!")
            print(f"   Stock: {barang['stock']} {barang['satuan']}")
            print(f"   Batas minimum: {barang['stock_minimum']} {barang['satuan']}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    # ============= FUNGSI LIHAT DATA =============
    
    def lihat_semua_barang(self):
        """Menampilkan semua data barang"""
        self.clear_screen()
        print("="*100)
        print("                      DAFTAR INVENTORY GUDANG")
        print("="*100)
        
        if not self.inventory:
            print("\n📭 Inventory kosong!")
        else:
            table_data = []
            for kode, item in self.inventory.items():
                total_nilai_beli = item['stock'] * item['harga_beli']
                total_nilai_jual = item['stock'] * item['harga_jual']
                
                # Status stock
                if item['stock'] <= 0:
                    status = "❌ HABIS"
                elif item['stock'] <= item['stock_minimum']:
                    status = "⚠️ RENDAH"
                else:
                    status = "✅ AMAN"
                
                table_data.append([
                    kode,
                    item['nama'][:20],
                    item['kategori'][:15],
                    f"{item['stock']} {item['satuan']}",
                    self.format_rupiah(item['harga_beli']),
                    self.format_rupiah(item['harga_jual']),
                    self.format_rupiah(total_nilai_beli),
                    status
                ])
            
            print(tabulate(table_data, 
                         headers=['Kode', 'Nama', 'Kategori', 'Stock', 'Harga Beli', 
                                 'Harga Jual', 'Total Nilai', 'Status'],
                         tablefmt='grid'))
            
            # Hitung total nilai inventory
            total_nilai_inventory = sum(item['stock'] * item['harga_beli'] for item in self.inventory.values())
            total_stock_item = sum(1 for item in self.inventory.values() if item['stock'] > 0)
            total_habis = sum(1 for item in self.inventory.values() if item['stock'] <= 0)
            
            print("\n" + "="*100)
            print(f"📊 RINGKASAN:")
            print(f"   Total Item Terdaftar : {len(self.inventory)}")
            print(f"   Item dengan Stock    : {total_stock_item}")
            print(f"   Item Stock Habis     : {total_habis}")
            print(f"   Total Nilai Inventory: {self.format_rupiah(total_nilai_inventory)}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def lihat_riwayat_transaksi(self):
        """Menampilkan riwayat pemasukkan dan pengeluaran"""
        self.clear_screen()
        print("="*100)
        print("                     RIWAYAT TRANSAKSI")
        print("="*100)
        
        if not self.transaksi:
            print("\n📭 Belum ada transaksi!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        # Filter transaksi berdasarkan jenis
        print("\nPilih filter transaksi:")
        print("1. Semua Transaksi")
        print("2. Pemasukkan Barang")
        print("3. Pengeluaran Barang")
        print("4. Transaksi Hari Ini")
        
        pilihan = input("\nMasukkan pilihan (1-4): ")
        
        filtered_transaksi = []
        if pilihan == '1':
            filtered_transaksi = self.transaksi
        elif pilihan == '2':
            filtered_transaksi = [t for t in self.transaksi if t['jenis'] == 'PEMASUKKAN']
        elif pilihan == '3':
            filtered_transaksi = [t for t in self.transaksi if t['jenis'] == 'PENGELUARAN']
        elif pilihan == '4':
            hari_ini = datetime.now().strftime("%d-%m-%Y")
            filtered_transaksi = [t for t in self.transaksi if hari_ini in t['waktu']]
        else:
            filtered_transaksi = self.transaksi
        
        # Ambil 20 transaksi terbaru
        filtered_transaksi = filtered_transaksi[-20:]
        filtered_transaksi.reverse()
        
        table_data = []
        for t in filtered_transaksi:
            if t['jenis'] == 'PEMASUKKAN':
                warna = '🟢'
                jumlah = f"+{t['jumlah']} {t['satuan']}"
                detail = f"Batch: {t.get('nomor_batch', '-')}"
            else:
                warna = '🔴'
                jumlah = f"-{t['jumlah']} {t['satuan']}"
                detail = f"Tujuan: {t.get('tujuan', '-')}"
            
            table_data.append([
                t['id'][-8:],
                t['waktu'][:10],
                t['nama_barang'][:20],
                warna + ' ' + t['jenis'][:12],
                jumlah,
                detail[:20],
                self.format_rupiah(t.get('total_harga', t.get('harga_beli', 0) * t['jumlah']))
            ])
        
        print(tabulate(table_data, 
                     headers=['ID', 'Tanggal', 'Nama', 'Jenis', 'Jumlah', 'Keterangan', 'Nilai'],
                     tablefmt='grid'))
        
        # Hitung total transaksi
        total_pemasukkan = sum(t['jumlah'] * t.get('harga_beli', 0) 
                              for t in self.transaksi if t['jenis'] == 'PEMASUKKAN')
        total_pengeluaran = sum(t.get('total_harga', 0) 
                               for t in self.transaksi if t['jenis'] == 'PENGELUARAN')
        
        print("\n" + "="*100)
        print(f"📊 TOTAL TRANSAKSI:")
        print(f"   Total Pemasukkan : {self.format_rupiah(total_pemasukkan)}")
        print(f"   Total Pengeluaran: {self.format_rupiah(total_pengeluaran)}")
        print(f"   Selisih          : {self.format_rupiah(total_pengeluaran - total_pemasukkan)}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def cek_stock_minimum(self):
        """Menampilkan barang dengan stock di bawah minimum"""
        self.clear_screen()
        print("="*70)
        print("               LAPORAN STOCK MINIMUM")
        print("="*70)
        
        stock_rendah = {}
        for kode, item in self.inventory.items():
            if item['stock'] <= item['stock_minimum']:
                stock_rendah[kode] = item
        
        if not stock_rendah:
            print("\n✅ Semua barang memiliki stock di atas batas minimum!")
        else:
            print(f"\n⚠️ Terdapat {len(stock_rendah)} barang dengan stock di bawah minimum:")
            print("-"*70)
            
            table_data = []
            for kode, item in stock_rendah.items():
                kekurangan = item['stock_minimum'] - item['stock']
                table_data.append([
                    kode,
                    item['nama'],
                    f"{item['stock']} {item['satuan']}",
                    f"{item['stock_minimum']} {item['satuan']}",
                    f"{kekurangan} {item['satuan']}",
                    item['supplier'],
                    '⚠️ SEGERA ORDER'
                ])
            
            print(tabulate(table_data, 
                         headers=['Kode', 'Nama', 'Stock', 'Minimum', 'Kekurangan', 'Supplier', 'Status'],
                         tablefmt='grid'))
            
            # Rekomendasi pembelian
            print("\n📋 REKOMENDASI PEMBELIAN:")
            for kode, item in stock_rendah.items():
                kekurangan = item['stock_minimum'] - item['stock']
                estimasi_biaya = kekurangan * item['harga_beli']
                print(f"   - {item['nama']}: Order {kekurangan} {item['satuan']} "
                      f"(Estimasi: {self.format_rupiah(estimasi_biaya)})")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    # ============= FUNGSI UPDATE DAN DELETE =============
    
    def update_barang(self):
        """Mengupdate data barang"""
        self.clear_screen()
        print("="*60)
        print("             UPDATE DATA BARANG")
        print("="*60)
        
        kode = input("Masukkan kode barang: ").upper()
        
        if kode not in self.inventory:
            print(f"\n❌ Barang dengan kode {kode} tidak ditemukan!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        barang = self.inventory[kode]
        print(f"\n📦 Data Barang Saat Ini:")
        print(f"Nama        : {barang['nama']}")
        print(f"Kategori    : {barang['kategori']}")
        print(f"Stock       : {barang['stock']} {barang['satuan']}")
        print(f"Harga Beli  : {self.format_rupiah(barang['harga_beli'])}")
        print(f"Harga Jual  : {self.format_rupiah(barang['harga_jual'])}")
        print(f"Stock Min   : {barang['stock_minimum']} {barang['satuan']}")
        print(f"Lokasi      : {barang['lokasi']}")
        print(f"Supplier    : {barang['supplier']}")
        
        print("\n✏️ Update Data (kosongkan jika tidak ingin mengubah):")
        
        nama_baru = input(f"Nama baru [{barang['nama']}]: ")
        if nama_baru.strip():
            barang['nama'] = nama_baru
        
        kategori_baru = input(f"Kategori baru [{barang['kategori']}]: ")
        if kategori_baru.strip():
            barang['kategori'] = kategori_baru
        
        try:
            harga_beli_baru = input(f"Harga beli baru [{barang['harga_beli']}]: ")
            if harga_beli_baru.strip():
                barang['harga_beli'] = float(harga_beli_baru)
            
            harga_jual_baru = input(f"Harga jual baru [{barang['harga_jual']}]: ")
            if harga_jual_baru.strip():
                barang['harga_jual'] = float(harga_jual_baru)
            
            stock_min_baru = input(f"Stock minimum baru [{barang['stock_minimum']}]: ")
            if stock_min_baru.strip():
                barang['stock_minimum'] = int(stock_min_baru)
        except ValueError:
            print("\n❌ Input angka tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        lokasi_baru = input(f"Lokasi baru [{barang['lokasi']}]: ")
        if lokasi_baru.strip():
            barang['lokasi'] = lokasi_baru
        
        supplier_baru = input(f"Supplier baru [{barang['supplier']}]: ")
        if supplier_baru.strip():
            barang['supplier'] = supplier_baru
        
        barang['terakhir_update'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.save_data()
        
        print(f"\n✅ Data barang {barang['nama']} berhasil diupdate!")
        input("\nTekan Enter untuk melanjutkan...")
    
    def hapus_barang(self):
        """Menghapus barang dari inventory"""
        self.clear_screen()
        print("="*60)
        print("             HAPUS BARANG")
        print("="*60)
        
        kode = input("Masukkan kode barang: ").upper()
        
        if kode not in self.inventory:
            print(f"\n❌ Barang dengan kode {kode} tidak ditemukan!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        barang = self.inventory[kode]
        print(f"\n⚠️ Anda akan menghapus barang:")
        print(f"Nama    : {barang['nama']}")
        print(f"Stock   : {barang['stock']} {barang['satuan']}")
        print(f"Supplier: {barang['supplier']}")
        
        if barang['stock'] > 0:
            print(f"\n❌ PERHATIAN: Barang masih memiliki stock {barang['stock']} {barang['satuan']}!")
            print("   Hapus stock terlebih dahulu atau lakukan pengeluaran barang.")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        konfirmasi = input(f"\nYakin ingin menghapus {barang['nama']}? (y/n): ").lower()
        
        if konfirmasi == 'y':
            del self.inventory[kode]
            self.save_data()
            print(f"\n✅ Barang {barang['nama']} berhasil dihapus!")
        else:
            print("\n❌ Penghapusan dibatalkan!")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    # ============= FUNGSI LAPORAN =============
    
    def laporan_harian(self):
        """Menampilkan laporan transaksi harian"""
        self.clear_screen()
        print("="*70)
        print("               LAPORAN HARIAN")
        print("="*70)
        
        tanggal = input("Masukkan tanggal (DD-MM-YYYY) atau Enter untuk hari ini: ")
        if not tanggal:
            tanggal = datetime.now().strftime("%d-%m-%Y")
        
        transaksi_harian = [t for t in self.transaksi if tanggal in t['waktu']]
        
        if not transaksi_harian:
            print(f"\n📭 Tidak ada transaksi pada tanggal {tanggal}")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        print(f"\n📊 LAPORAN TANGGAL: {tanggal}")
        print("-"*70)
        
        # Pisahkan pemasukkan dan pengeluaran
        pemasukkan = [t for t in transaksi_harian if t['jenis'] == 'PEMASUKKAN']
        pengeluaran = [t for t in transaksi_harian if t['jenis'] == 'PENGELUARAN']
        
        print(f"\n🟢 PEMASUKKAN BARANG ({len(pemasukkan)} transaksi):")
        if pemasukkan:
            table_pemasukkan = []
            for t in pemasukkan:
                table_pemasukkan.append([
                    t['nama_barang'],
                    f"{t['jumlah']} {t['satuan']}",
                    self.format_rupiah(t['harga_beli']),
                    self.format_rupiah(t['jumlah'] * t['harga_beli'])
                ])
            print(tabulate(table_pemasukkan, 
                         headers=['Nama', 'Jumlah', 'Harga', 'Total'],
                         tablefmt='simple'))
        
        print(f"\n🔴 PENGELUARAN BARANG ({len(pengeluaran)} transaksi):")
        if pengeluaran:
            table_pengeluaran = []
            for t in pengeluaran:
                table_pengeluaran.append([
                    t['nama_barang'],
                    f"{t['jumlah']} {t['satuan']}",
                    t['tujuan'],
                    self.format_rupiah(t['total_harga'])
                ])
            print(tabulate(table_pengeluaran, 
                         headers=['Nama', 'Jumlah', 'Tujuan', 'Total'],
                         tablefmt='simple'))
        
        # Ringkasan
        total_pemasukkan = sum(t['jumlah'] * t['harga_beli'] for t in pemasukkan)
        total_pengeluaran = sum(t['total_harga'] for t in pengeluaran)
        
        print("\n" + "="*70)
        print(f"RINGKASAN KEUANGAN:")
        print(f"  Total Pemasukkan : {self.format_rupiah(total_pemasukkan)}")
        print(f"  Total Pengeluaran: {self.format_rupiah(total_pengeluaran)}")
        print(f"  Selisih          : {self.format_rupiah(total_pengeluaran - total_pemasukkan)}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    # ============= MENU UTAMA =============
    
    def menu(self):
        """Menu utama program"""
        while True:
            self.clear_screen()
            print("="*60)
            print("         SISTEM INVENTORY GUDANG")
            print("         Manajemen Barang & Transaksi")
            print("="*60)
            print(f"📦 Total Barang: {len(self.inventory)}")
            print(f"📊 Total Transaksi: {len(self.transaksi)}")
            print("="*60)
            print("\n🔷 MENU UTAMA:")
            print("   1. 📦 Manajemen Barang")
            print("   2. ⬆️  Pemasukkan Barang (Barang Masuk)")
            print("   3. ⬇️  Pengeluaran Barang (Barang Keluar)")
            print("   4. 📋 Lihat Data")
            print("   5. 📊 Laporan & Statistik")
            print("   6. 🚪 Keluar")
            print("="*60)
            
            pilihan = input("Masukkan pilihan (1-6): ")
            
            if pilihan == '1':
                self.menu_manajemen_barang()
            elif pilihan == '2':
                self.pemasukkan_barang()
            elif pilihan == '3':
                self.pengeluaran_barang()
            elif pilihan == '4':
                self.menu_lihat_data()
            elif pilihan == '5':
                self.menu_laporan()
            elif pilihan == '6':
                self.clear_screen()
                print("="*60)
                print("         TERIMA KASIH")
                print("         Program Inventory Gudang")
                print("="*60)
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk melanjutkan...")
    
    def menu_manajemen_barang(self):
        """Sub menu manajemen barang"""
        while True:
            self.clear_screen()
            print("="*60)
            print("         MANAJEMEN BARANG")
            print("="*60)
            print("   1. ➕ Tambah Barang Baru")
            print("   2. ✏️  Update Data Barang")
            print("   3. 🗑️  Hapus Barang")
            print("   4. 🔍 Cari Barang")
            print("   5. ↩️  Kembali ke Menu Utama")
            print("="*60)
            
            pilihan = input("Masukkan pilihan (1-5): ")
            
            if pilihan == '1':
                self.tambah_barang()
            elif pilihan == '2':
                self.update_barang()
            elif pilihan == '3':
                self.hapus_barang()
            elif pilihan == '4':
                self.cari_barang()
            elif pilihan == '5':
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk melanjutkan...")
    
    def menu_lihat_data(self):
        """Sub menu lihat data"""
        while True:
            self.clear_screen()
            print("="*60)
            print("         LIHAT DATA")
            print("="*60)
            print("   1. 📋 Lihat Semua Barang")
            print("   2. 📜 Riwayat Transaksi")
            print("   3. ⚠️  Cek Stock Minimum")
            print("   4. ↩️  Kembali ke Menu Utama")
            print("="*60)
            
            pilihan = input("Masukkan pilihan (1-4): ")
            
            if pilihan == '1':
                self.lihat_semua_barang()
            elif pilihan == '2':
                self.lihat_riwayat_transaksi()
            elif pilihan == '3':
                self.cek_stock_minimum()
            elif pilihan == '4':
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk melanjutkan...")
    
    def menu_laporan(self):
        """Sub menu laporan"""
        while True:
            self.clear_screen()
            print("="*60)
            print("         LAPORAN & STATISTIK")
            print("="*60)
            print("   1. 📅 Laporan Harian")
            print("   2. 📊 Laporan Stock Minimum")
            print("   3. 📈 Statistik Inventory")
            print("   4. ↩️  Kembali ke Menu Utama")
            print("="*60)
            
            pilihan = input("Masukkan pilihan (1-4): ")
            
            if pilihan == '1':
                self.laporan_harian()
            elif pilihan == '2':
                self.cek_stock_minimum()
            elif pilihan == '3':
                self.statistik_inventory()
            elif pilihan == '4':
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk melanjutkan...")
    
    def cari_barang(self):
        """Mencari barang berdasarkan berbagai kriteria"""
        self.clear_screen()
        print("="*60)
        print("         CARI BARANG")
        print("="*60)
        
        print("\nCari berdasarkan:")
        print("1. Kode Barang")
        print("2. Nama Barang")
        print("3. Kategori")
        print("4. Supplier")
        
        pilihan = input("\nMasukkan pilihan (1-4): ")
        keyword = input("Masukkan kata kunci: ").lower()
        
        hasil = []
        for kode, item in self.inventory.items():
            if pilihan == '1' and keyword in kode.lower():
                hasil.append((kode, item))
            elif pilihan == '2' and keyword in item['nama'].lower():
                hasil.append((kode, item))
            elif pilihan == '3' and keyword in item['kategori'].lower():
                hasil.append((kode, item))
            elif pilihan == '4' and keyword in item['supplier'].lower():
                hasil.append((kode, item))
        
        self.clear_screen()
        print("="*60)
        print(f"         HASIL PENCARIAN: {len(hasil)} Barang")
        print("="*60)
        
        if hasil:
            table_data = []
            for kode, item in hasil:
                status = "✅" if item['stock'] > item['stock_minimum'] else "⚠️"
                table_data.append([
                    kode,
                    item['nama'][:20],
                    item['kategori'],
                    f"{item['stock']} {item['satuan']}",
                    self.format_rupiah(item['harga_jual']),
                    status
                ])
            
            print(tabulate(table_data, 
                         headers=['Kode', 'Nama', 'Kategori', 'Stock', 'Harga Jual', 'Status'],
                         tablefmt='grid'))
        else:
            print("\n❌ Barang tidak ditemukan!")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def statistik_inventory(self):
        """Menampilkan statistik inventory"""
        self.clear_screen()
        print("="*60)
        print("         STATISTIK INVENTORY")
        print("="*60)
        
        if not self.inventory:
            print("\n📭 Inventory kosong!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        # Statistik dasar
        total_barang = len(self.inventory)
        total_stock = sum(item['stock'] for item in self.inventory.values())
        total_nilai_beli = sum(item['stock'] * item['harga_beli'] for item in self.inventory.values())
        total_nilai_jual = sum(item['stock'] * item['harga_jual'] for item in self.inventory.values())
        
        # Barang dengan stock terbanyak
        stock_terbanyak = max(self.inventory.items(), key=lambda x: x[1]['stock'])
        stock_tersedikit = min(self.inventory.items(), key=lambda x: x[1]['stock'])
        
        # Barang termahal
        termahal = max(self.inventory.items(), key=lambda x: x[1]['harga_jual'])
        termurah = min(self.inventory.items(), key=lambda x: x[1]['harga_jual'])
        
        print(f"\n📊 INFORMASI UMUM:")
        print(f"   Total Jenis Barang    : {total_barang}")
        print(f"   Total Stock Fisik     : {total_stock} unit")
        print(f"   Total Nilai (Beli)    : {self.format_rupiah(total_nilai_beli)}")
        print(f"   Total Nilai (Jual)    : {self.format_rupiah(total_nilai_jual)}")
        print(f"   Potensi Keuntungan    : {self.format_rupiah(total_nilai_jual - total_nilai_beli)}")
        
        print(f"\n🏆 BARANG TERBANYAK:")
        print(f"   {stock_terbanyak[1]['nama']} - {stock_terbanyak[1]['stock']} {stock_terbanyak[1]['satuan']}")
        
        print(f"\n📉 BARANG TERSEDIKIT:")
        print(f"   {stock_tersedikit[1]['nama']} - {stock_tersedikit[1]['stock']} {stock_tersedikit[1]['satuan']}")
        
        print(f"\n💰 BARANG TERMAHAL:")
        print(f"   {termahal[1]['nama']} - {self.format_rupiah(termahal[1]['harga_jual'])}")
        
        print(f"\n💵 BARANG TERMURAH:")
        print(f"   {termurah[1]['nama']} - {self.format_rupiah(termurah[1]['harga_jual'])}")
        
        # Statistik per kategori
        print(f"\n📋 STATISTIK PER KATEGORI:")
        kategori_dict = {}
        for item in self.inventory.values():
            if item['kategori'] not in kategori_dict:
                kategori_dict[item['kategori']] = {
                    'jumlah_item': 0,
                    'total_stock': 0,
                    'total_nilai': 0
                }
            kategori_dict[item['kategori']]['jumlah_item'] += 1
            kategori_dict[item['kategori']]['total_stock'] += item['stock']
            kategori_dict[item['kategori']]['total_nilai'] += item['stock'] * item['harga_beli']
        
        table_data = []
        for kategori, data in kategori_dict.items():
            table_data.append([
                kategori,
                data['jumlah_item'],
                f"{data['total_stock']} unit",
                self.format_rupiah(data['total_nilai'])
            ])
        
        print(tabulate(table_data, 
                     headers=['Kategori', 'Jumlah Item', 'Total Stock', 'Total Nilai'],
                     tablefmt='simple'))
        
        input("\nTekan Enter untuk melanjutkan...")

def main():
    """Fungsi utama untuk menjalankan program"""
    # Install tabulate jika belum ada
    try:
        import tabulate
    except ImportError:
        print("Menginstall library tabulate...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'tabulate'])
        print("Library berhasil diinstall!")
    
    program = InventoryGudang()
    program.menu()

if __name__ == "__main__":
    main()