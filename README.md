# **School Management Module (Odoo 16 Community)**

Modul ini dibuat untuk mengelola data **Guru**, **Siswa**, dan **Kelas**, sekaligus mempermudah pembuatan **tagihan bulanan otomatis** dan **kwitansi pembayaran** di Odoo.

---

## **Fitur Utama**
| No | Fitur | Status |
|----|-------|--------|
| 1 | Kelola data **Guru**, **Siswa**, dan **Kelas** | ✅ |
| 2 | Relasi guru → kelas → siswa | ✅ |
| 3 | Validasi nomor telepon guru harus unik | ✅ |
| 4 | GET API daftar guru (`/api/teachers`) | ✅ |
| 5 | POST API tambah siswa (`/api/students`) | ✅ |
| 6 | Report daftar guru & siswa dalam format PDF | ✅ |
| 7 | Scheduler otomatis untuk membuat invoice bulanan | ✅ |
| 8 | Tombol cetak kwitansi PDF hanya muncul jika status **Paid** | ✅ |

---

## **Struktur Modul**
```
school_management/
│
├── controllers/
│   └── api.py      # Endpoint API GET guru & POST siswa
│
├── models/
│   ├── teacher.py             # Model Guru
│   ├── student.py             # Model Siswa
│   ├── class_room.py               # Model Kelas
│   ├── account_extension.py     # Inherit account.move
│   └── student_invoice_scheduler.py  # Scheduler logic
│
├── reports/
│   ├── teacher_report.xml     # Report daftar guru & siswa
│   └── receipt_report.xml     # Report kwitansi pembayaran
│
├── views/
│   ├── teacher_views.xml
│   ├── student_views.xml
│   ├── menu_actions.xml
│   ├── class_views.xml
│   └── account_move_views.xml
│
├── data/
│   ├── demo_data.xml       # Product default untuk biaya sekolah
│   └── ir_cron.xml            # Scheduler untuk tagihan bulanan
│
├── security/
│   ├── ir.model.access.csv
│   └── security.xml           # Groups dan hak akses
│
├── __manifest__.py
└── README.md
```

---

## **Flow Sistem**

### **1. Relasi Model**
- **Guru** (`school.teacher`) → memiliki banyak **Kelas** (`school.class`).
- **Kelas** (`school.class`) → memiliki banyak **Siswa** (`school.student`).

```
Guru 1 ---< Kelas 1 ---< Siswa
Guru 2 ---< Kelas 2 ---< Siswa
```

---

### **2. Scheduler Invoice Bulanan**
- Setiap awal bulan, cron job otomatis dijalankan.
- Sistem mencari semua **siswa aktif**.
- Untuk setiap siswa:
  - Jika **belum ada invoice** untuk bulan berjalan, sistem membuat invoice baru.
  - Jika sudah ada → **skip**.
- Invoice default status **Draft**.

**Formula Billing Period:**
- Format: `YYYY-MM`
- Contoh: `2025-10` untuk bulan Oktober 2025.

---

### **3. Workflow Kwitansi**
1. Invoice yang sudah **Paid** → tombol **Cetak Kwitansi** muncul otomatis.
2. Klik tombol → PDF kwitansi akan di-generate.
3. Jika status invoice bukan Paid → tombol tidak muncul.

---

## **Setup Awal**

### **1. Install Modul**
- Salin folder `school_management` ke folder custom addons Odoo.
- Jalankan upgrade:
  ```bash
  ./odoo-bin -u school_management -c odoo.conf
  ```
---
**Note : Pastikan setelah di install setting user groups ke manager**
```settings -> users -> cari akses groups dengan nama "School Management -> pilih school manager"```

### **2. Buat Product "Biaya Sekolah Bulanan"**
Scheduler membutuhkan product dengan **nama persis**:  
```
Biaya Sekolah Bulanan
```

Cara membuat:
1. Menu **Sales → Products → Products** → **Create**.
2. Isi:
   - **Name** = `Biaya Sekolah Bulanan`
   - **Product Type** = Service
   - **Sales Price** = 500000 (atau sesuai kebutuhan)
3. Simpan.

> **Note:** Jika product ini tidak ada, scheduler akan error.

---

## **Testing API**

### **1. GET Daftar Guru**
- **URL:**  
  ```
  GET http://localhost:8069/api/teachers
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "count": 2,
    "data": [
      {
        "id": 1,
        "name": "Budi Santoso",
        "phone": "081234567891",
        "email": "budi@example.com",
        "student_count": 10
      }
    ]
  }
  ```

---

### **2. POST Tambah Siswa**
- **URL:**  
  ```
  POST http://localhost:8069/api/students
  ```
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body:**
  ```json
  {
    "name": "Dewi Kartika",
    "dob": "2015-02-20",
    "class_id": 1,
    "partner_id": 3 
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Siswa berhasil ditambahkan",
    "data": {
      "id": 4,
      "name": "Dewi Kartika",
      "dob": "2015-02-20",
      "class_name": "Kelas 1A",
      "partner_name": "Mitchell Admin"
    }
  }
  ```

---

## **Testing Scheduler**

### **1. Jalankan Cron Secara Manual**
Untuk testing, jalankan scheduler dari menu Odoo:
- **Settings → Technical → Scheduled Actions**
- Cari **"Generate Monthly Tuition Invoices"**.
- Klik **Run Manually**.

Jika berhasil, cek menu:
- **Accounting → Customers → Invoices**
- Invoice baru akan muncul untuk setiap siswa aktif.

---

### **2. Error yang Mungkin Terjadi**
| Error | Penyebab | Solusi |
|-------|----------|--------|
| `"Product 'Biaya Sekolah Bulanan' tidak ditemukan"` | Product belum dibuat atau nama salah | Pastikan product ada dan namanya **persis** sama |
| Invoice double dalam 1 bulan | Scheduler dijalankan lebih dari sekali tanpa pengecekan | Cek logika `billing_period` di model |

---

## **Testing Cetak Kwitansi**

1. Buka menu **Accounting → Customers → Invoices**.
2. Bayar invoice hingga status menjadi **Paid**.
3. Tombol **Cetak Kwitansi** akan muncul di form invoice.
4. Klik tombol → PDF kwitansi akan otomatis terdownload.

---

## **Flow Testing Interview**

1. **Setup Awal**
   - Install modul.
   - Buat product `"Biaya Sekolah Bulanan"`.

2. **Testing CRUD**
   - Tambahkan guru, kelas, dan siswa manual.
   - Gunakan API GET dan POST untuk validasi endpoint.

3. **Testing Scheduler**
   - Jalankan cron manual → cek invoice terbentuk.

4. **Testing Payment**
   - Bayar invoice → status menjadi Paid.
   - Pastikan tombol **Cetak Kwitansi** muncul.

5. **Cetak Kwitansi**
   - Klik tombol → PDF download otomatis.

---

## **Penutup**
Modul ini dirancang untuk mendemonstrasikan:
- **Integrasi API**, **scheduler otomatis**, **QWeb report**

