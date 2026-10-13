# Sistem Manajemen PLTA Curug - Perum Jasa Tirta II

Aplikasi sistem informasi dan manajemen operasional untuk **PLTA Curug**, **Gardu Induk 70 / 6,3 kV**, **Mini Hydro**, dan **Pompa Elektrik Tarum Timur (PETT)** di bawah naungan **Perum Jasa Tirta II (PJT II)**.

Aplikasi ini telah dimigrasikan dari Python/Flask ke stack modern **React 19 + TypeScript + Vite + Express Node.js**.

## Fitur Utama

1. **Laporan Gangguan Baru**
   - Pencatatan jenis gangguan, jam, tanggal kejadian, dan kronologi operasional.
   - Generator PDF berkas resmi laporan gangguan sesuai tata letak ReportLab.
   - Penyimpanan riwayat kejadian lokal dan unduhan dokumen PDF.

2. **Hystori Gangguan & Berkas Tergenerate**
   - Riwayat pelaporan insiden lengkap dengan rincian kronologi.
   - Arsip dokumen PDF checklist normalisasi dan manuver yang telah selesai dieksekusi.

3. **Form Normalisasi & Checklist Operasional**
   - **Mode Manual:** Input kustom daftar uraian penanganan, jam manuver, dan status.
   - **Mode Otomatis (SOP Standar PJT II):**
     1. Checklist Pengamanan Gangguan / Trip (Gardu Induk 70 / 6,3 kV Curug).
     2. Checklist Pindah Line 70 kV Jatiluhur ke Kosambi (`F-20/DPL/IK.12-01`).
     3. Checklist Pindah Line 70 kV Kosambi ke Jatiluhur (`F-20/DPL/IK.12-02`).
     4. Checklist Operasi PLTA Mini Hydro Curug (`F-20/DPL/IK.10-01`).
   - Pencatatan Tap Changer (TC 1–20), pengesahan tim, dan ekspor instan PDF checklist.

4. **Struktur Laboratorium Energi (Struktural Pegawai)**
   - Diagram hierarki terintegrasi membedakan jalur Sektor Operasional (Kelompok I–IV) dan Sektor Pemeliharaan (Mini Hydro, GI, PETT, SUTT, SUTM, SUTR).

5. **Sejarah Bendung Curug & Dokumentasi Historis**
   - Informasi historis pengelolaan aliran Citarum, Saluran Induk Tarum Barat & Tarum Timur, serta dokumentasi foto Bendung Curug tempo dulu.

6. **Pusat Informasi & Pengetahuan (FAQ)**
   - Pencarian interaktif dan kategorisasi (Profil PJT II, PLTA & Energi, Bendungan & Air).

7. **Asisten AI Operasional**
   - Konsultasi SOP teknis, manuver pindah line, K3 ketenagalistrikan, dan operasional PLTA Curug terhubung ke backend Express (`/api/ask-ai`).

## Cara Menjalankan

```bash
# Instalasi dependensi
npm install

# Menjalankan dev server pada port 3000
npm run dev

# Membangun produksi
npm run build
```