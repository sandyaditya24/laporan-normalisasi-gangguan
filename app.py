from flask import Flask, render_template_string, request, send_file, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
import re
import urllib.parse
from datetime import datetime

app = Flask(__name__)

PDF_FOLDER = "static"
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aplikasi Laporan Normalisasi Gangguan - PJT II</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #070f1e;
            --card-bg: rgba(255, 255, 255, 0.95);
            --primary-color: #2563eb;
            --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border-color: rgba(226, 232, 240, 0.8);
        }
        body {
            background: linear-gradient(135deg, rgba(7, 15, 30, 0.85), rgba(15, 23, 42, 0.9)), url('/static/CURUGTEMPODULU.jpg') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: var(--text-main);
            padding-bottom: 3rem;
            transition: background 1s ease-in-out;
        }
        .enterprise-wrapper {
            max-width: 1450px;
            margin: 0 auto;
        }
        .dashboard-header {
            background: var(--card-bg);
            border-radius: 20px;
            backdrop-filter: blur(16px);
            padding: 2rem 2.5rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
            position: relative;
            overflow: hidden;
        }
        .dashboard-header::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 6px; height: 100%;
            background: var(--primary-gradient);
        }
        .menu-sidebar {
            background: var(--card-bg);
            border-radius: 20px;
            backdrop-filter: blur(16px);
            padding: 1.75rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
        }
        .menu-btn {
            width: 100%;
            text-align: left;
            font-weight: 600;
            border-radius: 12px;
            padding: 0.9rem 1.25rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid var(--border-color);
            background-color: #f8fafc;
            color: var(--text-main);
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .menu-btn:hover {
            background-color: #eff6ff;
            color: var(--primary-color);
            border-color: #bfdbfe;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
        }
        .menu-btn.active {
            background: var(--primary-gradient);
            color: white;
            border-color: transparent;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
        }
        /* Style untuk Sub-Menu Laporan Gangguan */
        .submenu-container {
            padding-left: 1.5rem;
            margin-top: 0.5rem;
            margin-bottom: 0.75rem;
            border-left: 2px dashed #cbd5e1;
            display: none;
        }
        .submenu-btn {
            width: 100%;
            text-align: left;
            font-weight: 500;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            transition: all 0.2s;
            border: 1px solid transparent;
            background-color: transparent;
            color: var(--text-muted);
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 4px;
        }
        .submenu-btn:hover {
            background-color: #f1f5f9;
            color: var(--primary-color);
        }
        .submenu-btn.active {
            background-color: #eff6ff;
            color: var(--primary-color);
            font-weight: 600;
            border-color: #bfdbfe;
        }
        .content-card {
            border: none;
            border-radius: 20px;
            backdrop-filter: blur(16px);
            background-color: var(--card-bg);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
            animation: fadeIn 0.4s ease-in-out;
            position: relative;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .card-header-custom {
            border-top-left-radius: 20px !important;
            border-top-right-radius: 20px !important;
            background: linear-gradient(135deg, #0f172a, #1e293b) !important;
            padding: 1.75rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .btn-close-red-container {
            position: absolute;
            top: 1.25rem;
            right: 1.25rem;
            background-color: #dc3545;
            color: white;
            border: none;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            cursor: pointer;
            z-index: 10;
            box-shadow: 0 4px 10px rgba(220, 53, 69, 0.4);
            transition: all 0.2s ease;
        }
        .btn-close-red-container:hover {
            background-color: #b02a37;
            transform: scale(1.08);
        }
        .form-control, .form-select {
            border-radius: 12px;
            padding: 0.75rem 1rem;
            border: 1px solid var(--border-color);
            background-color: #f8fafc;
            font-size: 0.95rem;
            transition: all 0.2s;
        }
        .form-control:focus, .form-select:focus {
            background-color: #ffffff;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
            border-color: var(--primary-color);
        }
        .btn-custom {
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        .table-responsive {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }
        .closable-image-wrapper {
            position: relative;
            display: inline-block;
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        .closable-image-wrapper.transparent-state {
            opacity: 0.35;
        }
        .closable-image-wrapper img {
            max-height: 250px;
            object-fit: cover;
            border-radius: 1rem;
        }
        .btn-close-img {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.6);
            color: white;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            cursor: pointer;
            transition: background 0.2s;
            z-index: 5;
        }
        .btn-close-img:hover {
            background: rgba(220, 53, 69, 0.9);
        }
        .bg-switcher-badge {
            cursor: pointer;
            transition: all 0.2s;
        }
        .bg-switcher-badge:hover {
            background-color: #1d4ed8 !important;
            transform: translateY(-1px);
        }
    </style>
</head>
<body>
    <div class="container mt-4 mb-5 enterprise-wrapper">
        
        <!-- HEADER UTAMA -->
        <div class="row justify-content-center mb-4">
            <div class="col-md-12">
                <div class="dashboard-header">
                    <div class="row align-items-center">
                        <div class="col-lg-8">
                            <h2 class="fw-bold text-dark mb-2 fs-3 tracking-tight">SISTEM MANAJEMEN PLTA CURUG</h2>
                            <h5 class="fw-semibold text-primary mb-2">PERUM JASA TIRTA II</h5>
                            <p class="text-muted mb-0">Platform pelaporan operasional, normalisasi gangguan, dan manajemen teknis gardu induk yang terintegrasi.</p>
                        </div>
                        <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
                            <span class="badge bg-primary px-3 py-2 rounded-pill fs-6 fw-normal shadow-sm">
                                <i class="fa-solid fa-shield-halved me-1"></i> Enterprise v3.2
                            </span>
                            <div class="mt-2">
                                <span class="badge bg-dark bg-switcher-badge px-3 py-2 rounded-pill fs-7 shadow-sm" onclick="gantiBackgroundPJT()" title="Klik untuk mengganti background PJT II">
                                    <i class="fa-solid fa-image me-1"></i> Background PJT II (<span id="bgName">Curug Tempo Dulu</span>)
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- LAYOUT UTAMA: SIDEBAR & KONTEN -->
        <div class="row g-4">
            <!-- SIDEBAR NAVIGASI -->
            <div class="col-lg-3">
                <div class="menu-sidebar sticky-top" style="top: 2rem;">
                    <h6 class="text-uppercase text-muted fw-bold mb-3" style="font-size: 0.75rem; letter-spacing: 0.08em;">Menu Navigasi</h6>
                    <div class="d-grid gap-2 mb-4">
                        
                        <!-- MENU UTAMA: LAPORAN GANGGUAN DENGAN SUB-MENU -->
                        <div>
                            <button type="button" class="btn menu-btn" id="btnMenuLaporanGangguan" onclick="toggleSubMenu('laporan-gangguan-submenu')">
                                <i class="fa-solid fa-triangle-exclamation fa-fw text-warning"></i> Laporan Gangguan <i class="fa-solid fa-chevron-down ms-auto fs-7"></i>
                            </button>
                            <div class="submenu-container" id="laporan-gangguan-submenu">
                                <button type="button" class="btn submenu-btn" id="btnSubBuatLaporan" onclick="pilihMenu('form')">
                                    <i class="fa-solid fa-file-circle-plus fa-fw"></i> Buat Laporan Gangguan
                                </button>
                                <button type="button" class="btn submenu-btn" id="btnSubHistory" onclick="pilihMenu('history')">
                                    <i class="fa-solid fa-clock-rotate-left fa-fw"></i> History Gangguan
                                </button>
                            </div>
                        </div>

                        <!-- MENU LAINNYA -->
                        <button type="button" class="btn menu-btn" id="btnMenuSejarah" onclick="pilihMenu('sejarah')">
                            <i class="fa-solid fa-landmark fa-fw"></i> Sejarah Bendung Curug
                        </button>
                    </div>
                    
                    <div class="p-3 bg-light rounded-4 border border-light">
                        <small class="text-muted d-block fw-semibold mb-1">Status Sistem:</small>
                        <span class="d-flex align-items-center text-success fw-bold small">
                            <span class="spinner-grow spinner-grow-sm me-2 text-success" role="status"></span> Server Aktif & Aman
                        </span>
                    </div>
                </div>
            </div>

            <!-- AREA KONTEN (DEFAULT KOSONG TOTAL) -->
            <div class="col-lg-9">
                
                <!-- 1. ARTIKEL SEJARAH BENDUNG CURUG -->
                <div class="card content-card mb-4" id="container-sejarah" style="display: none;">
                    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup / Kosongkan Halaman">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="card-header-custom text-white text-center">
                        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-landmark me-2"></i> SEJARAH BENDUNG CURUG & PENGEMBANGANNYA</h3>
                        <p class="mb-0 text-white-50 small mt-1">Perum Jasa Tirta II - Perjalanan Infrastruktur Pengairan & Kelistrikan di Jawa Barat</p>
                    </div>
                    <div class="card-body p-4 p-md-5">
                        <div class="row align-items-center mb-4">
                            <div class="col-md-7">
                                <h4 class="fw-bold text-dark">Awal Mula Pembangunan</h4>
                                <p class="text-muted" style="text-align: justify; line-height: 1.7;">
                                    Bendung Curug memiliki peranan yang sangat vital dalam sejarah pengelolaan sumber daya air dan kelistrikan di Indonesia, khususnya di Jawa Barat. Pembangunan kompleks pengairan di kawasan Curug (Kecamatan Klari / Ciampel, Karawang) tidak dapat dilepaskan dari sejarah besar proyek irigasi Jatiluhur (Waduk Ir. H. Djuanda). Bendung Curug berfungsi sebagai pengatur pembagian air utama yang mengalirkan air dari Sungai Citarum ke Saluran Induk Tarum Barat dan Tarum Timur.
                                </p>
                            </div>
                            <div class="col-md-5 text-center">
                                <div id="imageWrapper" class="closable-image-wrapper border shadow-sm rounded-4">
                                    <button type="button" class="btn-close-img" onclick="toggleCloseImage()" title="Tutup / Kosongkan Gambar">
                                        <i class="fa-solid fa-xmark"></i>
                                    </button>
                                    <img src="/static/CURUGTEMPODULU.jpg" alt="Bendung Curug Tempo Dulu" class="img-fluid rounded-4" id="targetImage">
                                </div>
                                <small class="d-block text-muted mt-2 fst-italic" id="imageCaption">Dokumentasi historis kawasan Bendung Curug.</small>
                            </div>
                        </div>

                        <hr class="my-4">

                        <h4 class="fw-bold text-dark mb-3">Transformasi dan Peran Strategis</h4>
                        <p class="text-muted" style="text-align: justify; line-height: 1.7;">
                            Selain berfungsi sebagai pengendali debit air irigasi primer, kawasan ini juga dimanfaatkan untuk potensi energi terbarukan melalui Pembangkit Listrik Tenaga Air (PLTA) Mini Hydro Curug serta fasilitas Gardu Induk (GI) Curug 70/6,3 kV guna menopang suplai energi lokal.
                        </p>

                        <div class="mt-4 text-center">
                            <button type="button" class="btn btn-outline-primary px-4 btn-custom" onclick="pilihMenu('form')">
                                <i class="fa-solid fa-arrow-left me-2"></i> Kembali ke Buat Laporan
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 2. HISTORY GANGGUAN / DAFTAR LAPORAN PDF TERSIMPAN -->
                <div class="card content-card mb-4" id="container-history" style="display: none;">
                    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup / Kosongkan Halaman">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="card-header-custom text-white text-center">
                        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-clock-rotate-left me-2"></i> HISTORY GANGGUAN & LAPORAN TERSIMPAN</h3>
                        <p class="mb-0 text-white-50 small mt-1">Daftar arsip file laporan PDF normalisasi yang telah dibuat sebelumnya</p>
                    </div>
                    <div class="card-body p-4 p-md-5">
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover align-middle bg-white shadow-sm">
                                <thead class="table-dark text-center">
                                    <tr>
                                        <th width="8%">No</th>
                                        <th width="52%">Nama File Laporan PDF</th>
                                        <th width="20%">Waktu Pembuatan</th>
                                        <th width="20%">Aksi</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% if pdf_files %}
                                        {% for file in pdf_files %}
                                        <tr>
                                            <td class="text-center fw-bold">{{ loop.index }}</td>
                                            <td><i class="fa-solid fa-file-pdf text-danger me-2"></i> {{ file.name }}</td>
                                            <td class="text-center text-muted small">{{ file.date }}</td>
                                            <td class="text-center">
                                                <a href="/download/{{ file.name }}" class="btn btn-sm btn-primary px-3 shadow-sm" target="_blank">
                                                    <i class="fa-solid fa-download me-1"></i> Unduh
                                                </a>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    {% else %}
                                        <tr>
                                            <td colspan="4" class="text-center text-muted py-4">Belum ada file laporan PDF yang dibuat. Silakan buat laporan terlebih dahulu.</td>
                                        </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>
                        <div class="mt-4 text-center">
                            <button type="button" class="btn btn-outline-primary px-4 btn-custom" onclick="pilihMenu('form')">
                                <i class="fa-solid fa-file-circle-plus me-2"></i> Buat Laporan Baru
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 3. FORM UTAMA LAPORAN & CHECKLIST -->
                <div class="card content-card" id="container-form-laporan" style="display: none;">
                    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup / Kosongkan Halaman">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="card-header-custom text-white text-center">
                        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-clipboard-list me-2"></i> FORM LAPORAN NORMALISASI & CHECKLIST</h3>
                        <p class="mb-0 text-white-50 small mt-1">Sistem Pencatatan & Pelaporan Operasional Gardu Induk / Unit Terkait</p>
                    </div>
                    <div class="card-body p-4 p-md-5">
                        <form method="POST" action="/generate">
                            <div class="mb-4">
                                <label for="kategori" class="form-label fw-bold text-secondary">Pilih Kategori / Lokasi:</label>
                                <select class="form-select" id="kategori" name="kategori" required>
                                    <option value="" disabled selected>-- Pilih Jenis Normalisasi --</option>
                                    <option value="Gardu Induk Curug">1. Gardu Induk Curug</option>
                                    <option value="Mini Hydro">2. Mini Hydro</option>
                                    <option value="Pompa Elektrik Tarum Timur">3. Pompa Elektrik Tarum Timur</option>
                                </select>
                            </div>

                            <div class="mb-4 p-3 bg-light border rounded-4">
                                <label class="form-label fw-bold text-primary mb-2">Pilih Mode Pencatatan Penanganan:</label>
                                <div class="btn-group w-100 shadow-sm rounded-3" role="group">
                                    <input type="radio" class="btn-check" name="mode_pencatatan" id="modeManual" value="manual" autocomplete="off" checked onclick="switchMode('manual')">
                                    <label class="btn btn-outline-primary btn-custom" for="modeManual"><i class="fa-solid fa-pen-to-square me-1"></i> Mode Manual</label>

                                    <input type="radio" class="btn-check" name="mode_pencatatan" id="modeOtomatis" value="otomatis" autocomplete="off" onclick="switchMode('otomatis')">
                                    <label class="btn btn-outline-success btn-custom" for="modeOtomatis"><i class="fa-solid fa-list-check me-1"></i> Mode Otomatis</label>
                                </div>
                            </div>

                            <div class="mb-4" id="wrapper-jenis-manual">
                                <label for="jenis_gangguan_manual" class="form-label fw-bold text-secondary">Jenis Gangguan</label>
                                <input type="text" class="form-control" id="jenis_gangguan_manual" name="jenis_gangguan_manual" placeholder="Contoh: Gangguan Trafo / Trip PMT">
                            </div>

                            <div class="mb-4" id="wrapper-jenis-otomatis" style="display: none;">
                                <label for="jenis_gangguan_otomatis" class="form-label fw-bold text-secondary">Jenis Gangguan/Pengoperasian</label>
                                <select class="form-select" id="jenis_gangguan_otomatis" name="jenis_gangguan_otomatis" onchange="switchOtomatisSub(this.value)">
                                    <option value="" disabled selected>-- Pilih Jenis Checklist Otomatis --</option>
                                    <option value="CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)">1. CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)</option>
                                    <option value="CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV JATILUHUR KE PENGHANTAR 70 KV KOSAMBI">2. CHECK LIST PINDAH LINE (JATILUHUR -> KOSAMBI)</option>
                                    <option value="CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV KOSAMBI KE PENGHANTAR 70 KV JATILUHUR">3. CHECK LIST PINDAH LINE (KOSAMBI -> JATILUHUR)</option>
                                    <option value="CHECK LIST OPERASI PLTA MINI HYDRO CURUG">4. CHECK LIST OPERASI PLTA MINI HYDRO CURUG</option>
                                </select>
                            </div>

                            <div class="mb-4">
                                <label for="waktu" class="form-label fw-bold text-secondary">Tanggal & Jam Kejadian</label>
                                <input type="datetime-local" class="form-control" id="waktu" name="waktu" required oninput="updatePreview(this.value)">
                                <div id="preview-waktu" class="form-text text-success fw-bold mt-1"></div>
                            </div>
                            
                            <hr class="my-4">

                            <!-- KONTAINER MODE MANUAL -->
                            <div id="section-manual">
                                <label class="form-label fw-bold mb-2 text-primary">Daftar Penanganan Gangguan, Jam & Status (Manual):</label>
                                <div id="penanganan-container">
                                    <div class="row g-2 mb-2 penanganan-row">
                                        <div class="col-md-1">
                                            <input type="text" class="form-control text-center nomor-urut bg-white" value="1" readonly>
                                        </div>
                                        <div class="col-md-5">
                                            <input type="text" class="form-control" name="penanganan[]" placeholder="Jenis Penanganan">
                                        </div>
                                        <div class="col-md-2">
                                            <input type="text" class="form-control text-center" name="jam_item[]" placeholder="Jam (Cth: 10:00)">
                                        </div>
                                        <div class="col-md-3">
                                            <input type="text" class="form-control text-center" name="status_item[]" placeholder="Status Manual">
                                        </div>
                                        <div class="col-md-1">
                                            <button type="button" class="btn btn-danger w-100 btn-custom" onclick="hapusBaris(this)"><i class="fa-solid fa-trash"></i></button>
                                        </div>
                                    </div>
                                </div>
                                <button type="button" class="btn btn-outline-secondary btn-sm mb-4 px-3 btn-custom" onclick="tambahBaris()"><i class="fa-solid fa-plus me-1"></i> Tambah Baris</button>
                            </div>

                            <!-- KONTAINER MODE OTOMATIS -->
                            <div id="section-otomatis" style="display: none;" class="mb-4">
                                
                                <div id="sub-section-gi-curug" style="display: none;">
                                    <div class="alert alert-warning border-0 shadow-sm rounded-4">
                                        <b>CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)</b><br>
                                        <small>Centang item yang dikerjakan, lalu sesuaikan Keadaan/Posisi serta Pukul (Jam).</small>
                                    </div>

                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">A. RUANG PANEL 6,3 KV</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="45%">Uraian</th>
                                                    <th width="25%">Keadaan / Posisi</th>
                                                    <th width="20%">Pukul (Jam)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a1" value="on" checked></td>
                                                    <td class="text-center">1</td>
                                                    <td>PMT / CB Panel Trafo 500 KVA / Trafo I</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_a1" value="Dikelurkan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_a1" placeholder="Cth: 08:00"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a2" value="on" checked></td>
                                                    <td class="text-center">2</td>
                                                    <td>PMT / CB Panel Trafo 500 KVA / Trafo II</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_a2" value="Dikelurkan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_a2" placeholder="Cth: 08:00"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a3" value="on" checked></td>
                                                    <td class="text-center">3</td>
                                                    <td>PMT / CB Panel Keluaran 6 MB2</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_a3" value="Dikelurkan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_a3" placeholder="Cth: 08:00"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3 mt-3">B. RUANG PANEL 20 KV BUILDING</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="45%">Uraian</th>
                                                    <th width="25%">Keadaan / Posisi</th>
                                                    <th width="20%">Pukul (Jam)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% set items_b = [
                                                    ("PMT / CB Masukan dari Trafo I", "Dikelurkan"),
                                                    ("PMT / CB Trafo I 20 / 70 KV 10 MVA", "Dikelurkan"),
                                                    ("PMT / CB Trafo II 70 / 6,3 KV 5 MVA", "Dikelurkan"),
                                                    ("PMT / CB Trafo III 70 / 6,3 KV 5 MVA", "Dikelurkan"),
                                                    ("Riset Semua Gangguan", "Clear"),
                                                    ("Koordinasi dengan Kontrol Building", "Siap Dimasukan"),
                                                    ("PMT / CB Jatiluhur / Kosambi", "Dimasukan"),
                                                    ("PMT / CB Trafo I 20 / 70 KV 10 MVA", "Dimasukan"),
                                                    ("PMT / CB Masukan dari Trafo I", "Dimasukan"),
                                                    ("PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC", "Dimasukan"),
                                                    ("PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC", "Dimasukan"),
                                                    ("Riset Semua Gangguan", "Clear")
                                                ] %}
                                                {% for desc, default_pos in items_b %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b{{ loop.index }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>{{ desc }}</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_b{{ loop.index }}" value="{{ default_pos }}"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_b{{ loop.index }}"></td>
                                                </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    </div>

                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3 mt-3">C. RUANG PANEL 6 KV</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="45%">Uraian</th>
                                                    <th width="25%">Keadaan / Posisi</th>
                                                    <th width="20%">Pukul (Jam)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% set items_c = [
                                                    ("Riset Semua Gangguan", "Clear"),
                                                    ("PMT / CB Panel Masukan dari Trafo II", "Dimasukan"),
                                                    ("PMT / CB Panel Masukan dari Trafo III", "Dimasukan"),
                                                    ("PMT / CB Panel Trafo 500 KVA / Trafo I", "Dimasukan"),
                                                    ("PMT / CB Panel Trafo 500 KVA / Trafo II", "Dimasukan"),
                                                    ("PMT / CB Panel Keluaran 6 MB2", "Dimasukan"),
                                                    ("Riset Semua Gangguan", "Clear")
                                                ] %}
                                                {% for desc, default_pos in items_c %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_c{{ loop.index }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>{{ desc }}</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_c{{ loop.index }}" value="{{ default_pos }}"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_c{{ loop.index }}"></td>
                                                </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    </div>

                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3 mt-3">D. CB PANEL DISTRIBUSI 380 V AC TARUM BARAT</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="45%">Uraian</th>
                                                    <th width="25%">Keadaan / Posisi</th>
                                                    <th width="20%">Pukul (Jam)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_d1" value="on" checked></td>
                                                    <td class="text-center">1</td>
                                                    <td>CB Panel Distribusi 380 V AC Tarum Barat</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_d1" value="Dimasukan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_d1"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>

                                <div id="sub-section-pindah-line" style="display: none;">
                                    <div class="alert alert-info border-0 shadow-sm rounded-4">
                                        <b>CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV JATILUHUR KE KOSAMBI</b>
                                    </div>
                                    {% set panels_jk = [
                                        ('pa', 'A. RUANG PANEL 6 KV', [
                                            ('pa1', 'PMT/CB panel Trafo 500 KVA / Trafo I', 'Dikelurkan', ''),
                                            ('pa2', 'PMT/CB panel Trafo 500 KVA / Trafo II', 'Dikelurkan', ''),
                                            ('pa3', 'PMT/CB panel keluaran 6 MB2', 'Dikelurkan', ''),
                                            ('pa4', 'PMT/CB panel masukan dari Trafo II', 'Dikelurkan', ''),
                                            ('pa5', 'PMT/CB panel masukan dari Trafo III', 'Dikelurkan', '')
                                        ]),
                                        ('pb', 'B. RUANG PANEL 20 KV BUILDING', [
                                            ('pb1', 'PMT/CB Masukan dari trafo I', 'Dikelurkan', ''),
                                            ('pb2', 'PMT/CB Trafo I 20 / 70 KV 10 MVA', 'Dikelurkan', ''),
                                            ('pb3', 'PMT/CB Trafo II 70 / 6,3 KV 5 MVA', 'Dikelurkan', ''),
                                            ('pb4', 'PMT/CB Trafo III 70 / 6,3 KV 5 MVA', 'Dikelurkan', '')
                                        ]),
                                        ('pc', 'C. PMT JATILUHUR BAY', [
                                            ('pc1', 'PMT / CB 70 KV Jatiluhur Bay', 'Dikelurkan', ''),
                                            ('pc2', 'PMS / DS Line 70 KV Jatiluhur Bay', 'Tdk. dikeluarkan', 'Untuk monitoring'),
                                            ('pc3', 'PMS / DS Arde Line 70 KV Jatiluhur Bay', 'Keluar', '-'),
                                            ('pc4', 'PMS / DS Rel 70 KV Jatiluhur Bay', 'Dikelurkan', '-'),
                                            ('pc5', 'PMS / DS Arde Rel 70 KV Jatiluhur Bay', 'Keluar', '-')
                                        ]),
                                        ('pd', 'D. PMT KOSAMBI BAY', [
                                            ('pd1', 'PMS / DS Arde Line 70 KV Kosambi Bay', 'Keluar', '-'),
                                            ('pd2', 'PMS / DS Line 70 KV Kosambi Bay', 'Masuk', '-'),
                                            ('pd3', 'PMS / DS Arde Rel 70 KV Kosambi Bay', 'Keluar', '-'),
                                            ('pd4', 'PMS / DS Rel 70 KV Kosambi Bay', 'Dimasukan', '-'),
                                            ('pd5', 'PMT / CB 70 KV Kosambi Bay', 'Dimasukan', '-')
                                        ]),
                                        ('pe', 'E. RUANG PANEL 20 KV BUILDING', [
                                            ('pe1', 'PMT / CB Trafo I 20 / 70 KV 10 MVA', 'Dimasukan', ''),
                                            ('pe2', 'PMT / CB Masukan dari Trafo I', 'Dimasukan', ''),
                                            ('pe3_custom', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC', 'Dimasukan', 'Posisi TC harus sama'),
                                            ('pe4_custom', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC', 'Dimasukan', 'Posisi TC harus sama')
                                        ]),
                                        ('pf', 'F. RUANG PANEL 6 KV', [
                                            ('pf1', 'PMT / CB panel masukan dari Trafo II', 'Dimasukan', ''),
                                            ('pf2', 'PMT / CB panel masukan dari Trafo III', 'Dimasukan', ''),
                                            ('pf3', 'PMT / CB panel Trafo 500 KVA / Trafo I', 'Dimasukan', ''),
                                            ('pf4', 'PMT / CB panel Trafo 500 KVA / Trafo II', 'Dimasukan', ''),
                                            ('pf5', 'PMT / CB panel keluaran 6 MB2', 'Dimasukan', '')
                                        ])
                                    ] %}
                                    {% for p_key, p_title, p_items in panels_jk %}
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3 mt-3">{{ p_title }}</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th><th width="5%">No</th><th width="35%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="15%">Pukul (Jam)</th><th width="15%">Keterangan</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% for item_id, item_desc, item_default, item_ket in p_items %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_{{ item_id }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>{{ item_desc }}
                                                        {% if 'Posisi TC' in item_desc %}<br><input type="text" class="form-control form-control-sm mt-1" name="tc_val_{{ item_id }}" placeholder="Nilai TC...">{% endif %}
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_{{ item_id }}" value="{{ item_default }}"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_{{ item_id }}" placeholder="Jam"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_{{ item_id }}" value="{{ item_ket }}"></td>
                                                </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    </div>
                                    {% endfor %}
                                </div>

                                <div id="sub-section-pindah-line-kj" style="display: none;">
                                    <div class="alert alert-success border-0 shadow-sm rounded-4">
                                        <b>CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI KOSAMBI KE JATILUHUR</b>
                                    </div>
                                    {% set panels_kj = [
                                        ('qa', 'A. RUANG PANEL 6 KV', [
                                            ('qa1', 'PMT/CB panel Trafo 500 KVA / Trafo I', 'Dikelurkan', ''),
                                            ('qa2', 'PMT/CB panel Trafo 500 KVA / Trafo II', 'Dikelurkan', ''),
                                            ('qa3', 'PMT/CB panel keluaran 6 MB2', 'Dikelurkan', ''),
                                            ('qa4', 'PMT/CB panel masukan dari Trafo II', 'Dikelurkan', ''),
                                            ('qa5', 'PMT/CB panel masukan dari Trafo III', 'Dikelurkan', '')
                                        ]),
                                        ('qb', 'B. RUANG PANEL 20 KV BUILDING', [
                                            ('qb1', 'PMT/CB Masukan dari trafo I', 'Dikelurkan', ''),
                                            ('qb2', 'PMT/CB Trafo I 20 / 70 KV 10 MVA', 'Dikelurkan', ''),
                                            ('qb3', 'PMT/CB Trafo II 70 / 6,3 KV 5 MVA', 'Dikelurkan', ''),
                                            ('qb4', 'PMT/CB Trafo III 70 / 6,3 KV 5 MVA', 'Dikelurkan', '')
                                        ]),
                                        ('qc', 'C. PMT KOSAMBI BAY', [
                                            ('qc1', 'PMT / CB 70 KV Kosambi Bay', 'Dikelurkan', ''),
                                            ('qc2', 'PMS / DS Line 70 KV Kosambi Bay', 'Tdk. dikeluarkan', 'Monitoring'),
                                            ('qc3', 'PMS / DS Arde Line 70 KV Kosambi Bay', 'Keluar', '-'),
                                            ('qc4', 'PMS / DS Rel 70 KV Kosambi Bay', 'Dikelurkan', '-'),
                                            ('qc5', 'PMS / DS Arde Rel 70 KV Kosambi Bay', 'Keluar', '-')
                                        ]),
                                        ('qd', 'D. PMT JATILUHUR BAY', [
                                            ('qd1', 'PMS / DS Arde Line 70 KV Jatiluhur Bay', 'Keluar', '-'),
                                            ('qd2', 'PMS / DS Line 70 KV Jatiluhur Bay', 'Masuk', '-'),
                                            ('qd3', 'PMS / DS Arde Rel 70 KV Jatiluhur Bay', 'Keluar', '-'),
                                            ('qd4', 'PMS / DS Rel 70 KV Jatiluhur Bay', 'Dimasukan', '-'),
                                            ('qd5', 'PMT / CB 70 KV Jatiluhur Bay', 'Dimasukan', '-')
                                        ]),
                                        ('qe', 'E. RUANG PANEL 20 KV BUILDING', [
                                            ('qe1', 'PMT / CB Trafo I 20 / 70 KV 10 MVA', 'Dimasukan', ''),
                                            ('qe2', 'PMT / CB Masukan dari Trafo I', 'Dimasukan', ''),
                                            ('qe3_custom', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC', 'Dimasukan', 'Sama'),
                                            ('qe4_custom', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC', 'Dimasukan', 'Sama')
                                        ]),
                                        ('qf', 'F. RUANG PANEL 6 KV', [
                                            ('qf1', 'PMT / CB panel masukan dari Trafo II', 'Dimasukan', ''),
                                            ('qf2', 'PMT / CB panel masukan dari Trafo III', 'Dimasukan', ''),
                                            ('qf3', 'PMT / CB panel Trafo 500 KVA / Trafo I', 'Dimasukan', ''),
                                            ('qf4', 'PMT / CB panel Trafo 500 KVA / Trafo II', 'Dimasukan', ''),
                                            ('qf5', 'PMT / CB panel keluaran 6 MB2', 'Dimasukan', '')
                                        ])
                                    ] %}
                                    {% for p_key, p_title, p_items in panels_kj %}
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3 mt-3">{{ p_title }}</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th><th width="5%">No</th><th width="35%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="15%">Pukul (Jam)</th><th width="15%">Keterangan</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% for item_id, item_desc, item_default, item_ket in p_items %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_{{ item_id }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>{{ item_desc }}
                                                        {% if 'Posisi TC' in item_desc %}<br><input type="text" class="form-control form-control-sm mt-1" name="tc_val_{{ item_id }}" placeholder="Nilai TC...">{% endif %}
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_{{ item_id }}" value="{{ item_default }}"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_{{ item_id }}" placeholder="Jam"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_{{ item_id }}" value="{{ item_ket }}"></td>
                                                </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    </div>
                                    {% endfor %}
                                </div>

                                <div id="sub-section-plta-curug" style="display: none;">
                                    <div class="alert alert-primary border-0 shadow-sm rounded-4 mb-3">
                                        <b>CHECK LIST OPERASI PLTA MINI HYDRO CURUG</b>
                                    </div>
                                    <div class="row g-3 mb-3 bg-white p-3 border rounded-4 shadow-sm">
                                        <div class="col-md-6">
                                            <label for="plta_unit_no" class="form-label fw-bold text-secondary">UNIT No.:</label>
                                            <input type="text" class="form-control" id="plta_unit_no" name="plta_unit_no" placeholder="Contoh: Unit 1">
                                        </div>
                                        <div class="col-md-6">
                                            <label for="plta_jam_kerja" class="form-label fw-bold text-secondary">Jam Kerja Unit (TM):</label>
                                            <input type="text" class="form-control" id="plta_jam_kerja" name="plta_jam_kerja" placeholder="Contoh: 1250 Jam">
                                        </div>
                                    </div>
                                    {% set plta_sections = [
                                        ('plta_a', 'A. RUANG PANEL CONTROL ROOM', [
                                            ('plta_a1', 'Pada jendela alarm tidak ada indikasi gangguan', '-', 'TMA Udik 26-36', False),
                                            ('plta_a2', 'Tinggi Muka Air', 'Udik: ..., Hilir: ...', '-', True),
                                            ('plta_a3', 'Kriteria berhenti stabil', 'Menyala', '-', False),
                                            ('plta_a4', 'Posisi Pintu Pembuangan Tutup', 'Menyala', '-', False),
                                            ('plta_a5', 'Indikasi DS Phase Cubicle', 'Masuk', '-', True),
                                            ('plta_a6', 'Indikasi Earthing Switch', 'Keluar', '-', True),
                                            ('plta_a7', 'Indikasi CB 20 KV', 'Keluar', 'TPL Menyala', True),
                                            ('plta_a8', 'Indikasi Earthing Switch', 'Keluar', '-', True),
                                            ('plta_a9', 'Indikasi Unit Siap Jalan', 'Menyala', '-', False)
                                        ]),
                                        ('plta_b', 'B. CARA PENGOPERASIAAN', [
                                            ('plta_b1', 'Sistim Pengatur Unit', 'Lokal', '-', False),
                                            ('plta_b2', 'Sistim Komando Unit', 'Unit: ...', '-', True),
                                            ('plta_b3', 'Sinkronisasi', '-', '-', False),
                                            ('plta_b4', 'Duga Muka Air / Kontrol water level', 'ON / OFF', '-', False),
                                            ('plta_b5_1', 'Tombol Putaran Tanpa Beban', 'Berkedip', 'Tunggu', False),
                                            ('plta_b5_2', 'Tombol Eksitasi', 'Berkedip', 'Tunggu', False),
                                            ('plta_b5_3', 'Tombol Generator', 'Berkedip', 'Tunggu', False),
                                            ('plta_b5_4', 'Tombol Putaran Tanpa Beban (AUTO)', 'Berkedip', '-', False),
                                            ('plta_b6_1', 'Periksa TPL (CB 20 KV)', 'Berkedip', 'ON', True),
                                            ('plta_b6_2', 'Pengaturan beban / frekuensi', '-', '-', False),
                                            ('plta_b6_3', 'Pengaturan tegangan eksitasi', '-', '-', False),
                                            ('plta_b6_4', 'Putar Switch CB / TPL CB', 'LGB001JD', 'ON', True),
                                            ('plta_b6_5', 'Tekan tombol TPL CB paralel', 'Pukul: ...', '-', True)
                                        ]),
                                        ('plta_c', 'C. PENGATURAN BEBAN', [
                                            ('plta_c1', 'Tekan Tombol Pengatur Beban', '... MW', 'Bertahap', True)
                                        ]),
                                        ('plta_d', 'D. PENCATATAN RUTIN', [
                                            ('plta_d1', 'Pencatatan rutin harian', '-', '-', False)
                                        ])
                                    ] %}
                                    {% for p_key, p_title, p_items in plta_sections %}
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3 mt-3">{{ p_title }}</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="20%">Posisi / Isian</th><th width="12%">Status</th><th width="13%">Ket</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% for item_id, item_desc, item_default, item_ket, is_custom in p_items %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_{{ item_id }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>{{ item_desc }}
                                                        {% if is_custom %}<div class="mt-1"><input type="text" class="form-control form-control-sm" name="custom_input_{{ item_id }}" placeholder="Detail..."></div>{% endif %}
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_{{ item_id }}" value="{{ item_default }}"></td>
                                                    <td>
                                                        <select class="form-select form-select-sm text-center fw-bold" name="paraf_{{ item_id }}">
                                                            <option value="✔" selected class="text-success">✔ (OK)</option>
                                                            <option value="✖" class="text-danger">✖ (Tidak)</option>
                                                        </select>
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_{{ item_id }}" value="{{ item_ket }}"></td>
                                                </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>

                            <hr class="my-4">
                            
                            <!-- INFORMASI PEMBUAT LAPORAN -->
                            <div class="card p-4 mb-4 bg-light border-0 shadow-sm rounded-4">
                                <h6 class="fw-bold text-primary mb-3"><i class="fa-solid fa-user-shield me-2"></i> Informasi Pembuat Laporan</h6>
                                <div class="row g-3">
                                    <div class="col-md-4">
                                        <label for="nama_group" class="form-label fw-bold text-secondary">Group / Tim:</label>
                                        <input type="text" class="form-control bg-white" id="nama_group" name="nama_group" placeholder="Contoh: Group 1" required>
                                    </div>
                                    <div class="col-md-8">
                                        <label for="nama_petugas" class="form-label fw-bold text-secondary">Nama Petugas / Yang Melaksanakan:</label>
                                        <input type="text" class="form-control bg-white" id="nama_petugas" name="nama_petugas" placeholder="Contoh: Budi, Andi, Joko" required>
                                    </div>
                                </div>
                            </div>

                            <button type="submit" class="btn btn-primary w-100 py-3 shadow-sm fs-5 btn-custom">
                                <i class="fa-solid fa-file-pdf me-2"></i> Buat Laporan PDF Sekarang
                            </button>
                        </form>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        const backgroundListPJT = [
            {
                url: '/static/CURUGTEMPODULU.jpg',
                name: 'Bendung Curug Tempo Dulu'
            },
            {
                url: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1920&q=80',
                name: 'Waduk Ir. H. Djuanda (Jatiluhur)'
            },
            {
                url: 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1920&q=80',
                name: 'Kawasan Aliran Sungai & Hijau PJT II'
            },
            {
                url: 'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=1920&q=80',
                name: 'Infrastruktur Air & PLTA'
            }
        ];
        let currentBgIndex = 0;

        function gantiBackgroundPJT() {
            currentBgIndex = (currentBgIndex + 1) % backgroundListPJT.length;
            const selectedBg = backgroundListPJT[currentBgIndex];
            document.body.style.backgroundImage = `linear-gradient(135deg, rgba(7, 15, 30, 0.85), rgba(15, 23, 42, 0.9)), url('${selectedBg.url}')`;
            document.getElementById('bgName').innerText = selectedBg.name;
        }

        setInterval(gantiBackgroundPJT, 8000);

        function toggleSubMenu(submenuId) {
            const submenu = document.getElementById(submenuId);
            if (submenu.style.display === 'block') {
                submenu.style.display = 'none';
            } else {
                submenu.style.display = 'block';
            }
        }

        function pilihMenu(menu) {
            const formContainer = document.getElementById('container-form-laporan');
            const sejarahContainer = document.getElementById('container-sejarah');
            const historyContainer = document.getElementById('container-history');
            
            const btnLaporanGroup = document.getElementById('btnMenuLaporanGangguan');
            const btnSubBuat = document.getElementById('btnSubBuatLaporan');
            const btnSubHist = document.getElementById('btnSubHistory');
            const btnSejarah = document.getElementById('btnMenuSejarah');

            // Sembunyikan semua kontainer
            formContainer.style.display = 'none';
            sejarahContainer.style.display = 'none';
            historyContainer.style.display = 'none';

            // Reset active state tombol
            btnLaporanGroup.classList.remove('active');
            btnSubBuat.classList.remove('active');
            btnSubHist.classList.remove('active');
            btnSejarah.classList.remove('active');

            if (menu === 'form') {
                formContainer.style.display = 'block';
                btnLaporanGroup.classList.add('active');
                btnSubBuat.classList.add('active');
                document.getElementById('laporan-gangguan-submenu').style.display = 'block';
            } else if (menu === 'history') {
                historyContainer.style.display = 'block';
                btnLaporanGroup.classList.add('active');
                btnSubHist.classList.add('active');
                document.getElementById('laporan-gangguan-submenu').style.display = 'block';
            } else if (menu === 'sejarah') {
                sejarahContainer.style.display = 'block';
                btnSejarah.classList.add('active');
            }
        }

        function kosongkanKanan() {
            const formContainer = document.getElementById('container-form-laporan');
            const sejarahContainer = document.getElementById('container-sejarah');
            const historyContainer = document.getElementById('container-history');
            
            const btnLaporanGroup = document.getElementById('btnMenuLaporanGangguan');
            const btnSubBuat = document.getElementById('btnSubBuatLaporan');
            const btnSubHist = document.getElementById('btnSubHistory');
            const btnSejarah = document.getElementById('btnMenuSejarah');

            formContainer.style.display = 'none';
            sejarahContainer.style.display = 'none';
            historyContainer.style.display = 'none';

            btnLaporanGroup.classList.remove('active');
            btnSubBuat.classList.remove('active');
            btnSubHist.classList.remove('active');
            btnSejarah.classList.remove('active');
        }

        function switchMode(mode) {
            const secManual = document.getElementById('section-manual');
            const secOtomatis = document.getElementById('section-otomatis');
            const wrapManual = document.getElementById('wrapper-jenis-manual');
            const wrapOtomatis = document.getElementById('wrapper-jenis-otomatis');
            const inputManual = document.getElementById('jenis_gangguan_manual');
            const selectOtomatis = document.getElementById('jenis_gangguan_otomatis');
            const manualInputs = secManual.querySelectorAll('input');
            
            if (mode === 'manual') {
                secManual.style.display = 'block';
                secOtomatis.style.display = 'none';
                wrapManual.style.display = 'block';
                wrapOtomatis.style.display = 'none';
                
                inputManual.setAttribute('required', 'required');
                selectOtomatis.removeAttribute('required');

                manualInputs.forEach(input => {
                    if(!input.classList.contains('nomor-urut')) input.setAttribute('required', 'required');
                });
            } else {
                secManual.style.display = 'none';
                secOtomatis.style.display = 'block';
                wrapManual.style.display = 'none';
                wrapOtomatis.style.display = 'block';

                inputManual.removeAttribute('required');
                selectOtomatis.setAttribute('required', 'required');

                manualInputs.forEach(input => {
                    input.removeAttribute('required');
                });
            }
        }

        function switchOtomatisSub(val) {
            const subGiCurug = document.getElementById('sub-section-gi-curug');
            const subPindahLine = document.getElementById('sub-section-pindah-line');
            const subPindahLineKj = document.getElementById('sub-section-pindah-line-kj');
            const subPltaCurug = document.getElementById('sub-section-plta-curug');
            
            subGiCurug.style.display = 'none';
            subPindahLine.style.display = 'none';
            subPindahLineKj.style.display = 'none';
            subPltaCurug.style.display = 'none';

            if (val.includes("GARDU INDUK 70 / 6,3 KV CURUG")) {
                subGiCurug.style.display = 'block';
            } else if (val.includes("JATILUHUR KE PENGHANTAR 70 KV KOSAMBI")) {
                subPindahLine.style.display = 'block';
            } else if (val.includes("KOSAMBI KE PENGHANTAR 70 KV JATILUHUR")) {
                subPindahLineKj.style.display = 'block';
            } else if (val.includes("PLTA MINI HYDRO CURUG")) {
                subPltaCurug.style.display = 'block';
            }
        }

        function updatePreview(val) {
            if (!val) {
                document.getElementById('preview-waktu').innerText = '';
                return;
            }
            const dt = new Date(val);
            if (isNaN(dt)) return;

            const hariList = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
            const bulanList = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];

            const namaHari = hariList[dt.getDay()];
            const tanggal = dt.getDate();
            const namaBulan = bulanList[dt.getMonth()];
            const tahun = dt.getFullYear();
            
            const jam = String(dt.getHours()).padStart(2, '0');
            const menit = String(dt.getMinutes()).padStart(2, '0');

            const hasil = 'Format Tampil: ' + namaHari + ', ' + tanggal + ' ' + namaBulan + ' ' + tahun + ' Pukul ' + jam + ':' + menit + ' WIB';
            document.getElementById('preview-waktu').innerText = hasil;
        }

        function tambahBaris() {
            const container = document.getElementById('penanganan-container');
            const rows = container.getElementsByClassName('penanganan-row');
            const newNum = rows.length + 1;

            const newRow = document.createElement('div');
            newRow.className = 'row g-2 mb-2 penanganan-row';
            newRow.innerHTML = '<div class="col-md-1"><input type="text" class="form-control text-center nomor-urut bg-white" value="' + newNum + '" readonly></div>' +
                               '<div class="col-md-5"><input type="text" class="form-control" name="penanganan[]" placeholder="Jenis Penanganan" required></div>' +
                               '<div class="col-md-2"><input type="text" class="form-control text-center" name="jam_item[]" placeholder="Jam (Cth: 10:00)" required></div>' +
                               '<div class="col-md-3"><input type="text" class="form-control text-center" name="status_item[]" placeholder="Status Manual" required></div>' +
                               '<div class="col-md-1"><button type="button" class="btn btn-danger w-100 btn-custom" onclick="hapusBaris(this)"><i class="fa-solid fa-trash"></i></button></div>';
            container.appendChild(newRow);
        }

        function hapusBaris(btn) {
            const container = document.getElementById('penanganan-container');
            const rows = container.getElementsByClassName('penanganan-row');
            if (rows.length > 1) {
                btn.closest('.penanganan-row').remove();
                updateNomor();
            } else {
                alert("Minimal harus ada 1 baris penanganan!");
            }
        }

        function updateNomor() {
            const rows = document.getElementsByClassName('penanganan-row');
            for (let i = 0; i < rows.length; i++) {
                rows[i].getElementsByClassName('nomor-urut')[0].value = i + 1;
            }
        }

        let isImageClosed = false;
        function toggleCloseImage() {
            const img = document.getElementById('targetImage');
            const wrapper = document.getElementById('imageWrapper');
            const caption = document.getElementById('imageCaption');
            const closeBtn = wrapper.querySelector('.btn-close-img');

            isImageClosed = !isImageClosed;
            if (isImageClosed) {
                img.style.display = 'none';
                wrapper.classList.add('transparent-state');
                caption.style.display = 'none';
                closeBtn.innerHTML = '<i class="fa-solid fa-arrow-rotate-left"></i>';
                closeBtn.title = "Tampilkan Kembali Gambar";
            } else {
                img.style.display = 'block';
                wrapper.classList.remove('transparent-state');
                caption.style.display = 'block';
                closeBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
                closeBtn.title = "Tutup / Kosongkan Gambar";
            }
        }

        window.onload = function() {
            switchMode('manual');
            kosongkanKanan();
        }
    </script>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pratinjau Laporan</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, rgba(7, 15, 30, 0.85), rgba(15, 23, 42, 0.9)), url('/static/CURUGTEMPODULU.jpg') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card {
            border: none;
            border-radius: 20px;
            backdrop-filter: blur(16px);
            background-color: rgba(255, 255, 255, 0.95);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .card-header {
            border-top-left-radius: 20px !important;
            border-top-right-radius: 20px !important;
            background: linear-gradient(135deg, #198754, #157347) !important;
            padding: 1.75rem;
        }
        .btn {
            border-radius: 12px;
            padding: 0.75rem 1rem;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow-lg text-center">
                    <div class="card-header text-white">
                        <h4 class="mb-0 fw-bold"><i class="fa-solid fa-circle-check me-2"></i> Laporan Berhasil Dibuat!</h4>
                    </div>
                    <div class="card-body p-4 p-md-5">
                        <p class="text-muted mb-4">File PDF laporan gangguan Anda telah selesai disusun dan siap untuk diunduh atau dibagikan ke WhatsApp.</p>
                        <a href="/download/{{ filename }}" class="btn btn-primary w-100 mb-3 shadow-sm" target="_blank">
                            <i class="fa-solid fa-download me-2"></i> Unduh File PDF
                        </a>
                        <a href="https://api.whatsapp.com/send?text={{ wa_message }}" class="btn btn-success w-100 mb-3 shadow-sm" target="_blank">
                            <i class="fa-brands fa-whatsapp me-2"></i> Kirim ke Grup WhatsApp
                        </a>
                        <a href="/" class="btn btn-outline-secondary w-100">
                            <i class="fa-solid fa-arrow-left me-2"></i> Kembali ke Dashboard
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def get_pdf_files_list():
    files = []
    if os.path.exists(PDF_FOLDER):
        for f in os.listdir(PDF_FOLDER):
            if f.endswith(".pdf"):
                full_path = os.path.join(PDF_FOLDER, f)
                mod_time = os.path.getmtime(full_path)
                date_str = datetime.fromtimestamp(mod_time).strftime('%d-%m-%Y %H:%M')
                files.append({"name": f, "timestamp": mod_time, "date": date_str})
        files.sort(key=lambda x: x["timestamp"], reverse=True)
    return files

@app.route("/")
def index():
    pdf_files = get_pdf_files_list()
    return render_template_string(HTML_TEMPLATE, pdf_files=pdf_files)

@app.route("/generate", methods=["POST"])
def generate():
    kategori = request.form["kategori"]
    mode = request.form.get("mode_pencatatan", "manual")
    
    if mode == "manual":
        jenis_gangguan = request.form.get("jenis_gangguan_manual", "-")
    else:
        jenis_gangguan = request.form.get("jenis_gangguan_otomatis", "-")

    waktu_raw = request.form["waktu"]
    nama_group = request.form.get("nama_group", "-")
    nama_petugas = request.form.get("nama_petugas", "-")
    
    try:
        dt = datetime.strptime(waktu_raw, "%Y-%m-%dT%H:%M")
        hari_list = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
        bulan_list = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"}
        
        nama_hari = hari_list.get(dt.weekday(), "")
        nama_bulan = bulan_list.get(dt.month, "")
        waktu = f"{nama_hari}, {dt.day} {nama_bulan} {dt.year} Pukul {dt.strftime('%H:%M')} WIB"
        default_jam = dt.strftime('%H:%M')
        
        file_date_str = dt.strftime('%d-%m-%Y_%H%M')
    except:
        waktu = waktu_raw
        default_jam = "00:00"
        file_date_str = datetime.now().strftime('%d-%m-%Y_%H%M')

    clean_jenis = re.sub(r'[^a-zA-Z0-9]', '_', jenis_gangguan)
    clean_jenis = re.sub(r'_+', '_', clean_jenis).strip('_')
    if len(clean_jenis) > 30:
        clean_jenis = clean_jenis[:30]
    
    filename = f"laporan_{clean_jenis}_{file_date_str}.pdf"

    styles = getSampleStyleSheet()
    cell_style = ParagraphStyle(
        "CellStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=10
    )
    cell_center = ParagraphStyle(
        "CellCenter",
        parent=cell_style,
        alignment=1
    )
    sec_style = ParagraphStyle(
        "SecStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        fontName="Helvetica-Bold"
    )

    is_plta_curug = "PLTA MINI HYDRO CURUG" in jenis_gangguan

    if is_plta_curug:
        table_data = [[
            Paragraph("<b>No</b>", cell_center),
            Paragraph("<b>URAIAN</b>", cell_style),
            Paragraph("<b>POSISI / ISIAN</b>", cell_center),
            Paragraph("<b>STATUS</b>", cell_center),
            Paragraph("<b>KETERANGAN</b>", cell_center)
        ]]
    else:
        table_data = [[
            Paragraph("<b>No</b>", cell_center),
            Paragraph("<b>Uraian / Jenis Penanganan</b>", cell_style),
            Paragraph("<b>Pukul</b>", cell_center),
            Paragraph("<b>Keadaan / Posisi</b>", cell_center),
            Paragraph("<b>Keterangan</b>", cell_center)
        ]]

    wa_details = []

    if mode == "manual":
        penanganan_list = request.form.getlist("penanganan[]")
        jam_list = request.form.getlist("jam_item[]")
        status_list = request.form.getlist("status_item[]")
        
        for i, (penang, jam_item, stat) in enumerate(zip(penanganan_list, jam_list, status_list), start=1):
            table_data.append([
                Paragraph(str(i), cell_center),
                Paragraph(penang, cell_style),
                Paragraph(jam_item, cell_center),
                Paragraph(stat, cell_center),
                Paragraph("-", cell_center)
            ])
            wa_details.append(f"{i}. [{jam_item}] {penang} - {stat}")
    else:
        if is_plta_curug:
            plta_sections = [
                ('plta_a', 'A. RUANG PANEL CONTROL ROOM', [
                    ('plta_a1', 'Pada jendela alarm tidak ada indikasi gangguan', '-', 'TMA Udik 26-36 mohon diperhatikan apabila Beban sudah turun dan air Udik kecil, maka Mini Hydro Stop', False),
                    ('plta_a2', 'Tinggi Muka Air', 'Udik: ..., Hilir: ...', '-', True),
                    ('plta_a3', 'Kriteria berhenti stabil', 'Menyala', '-', False),
                    ('plta_a4', 'Posisi Pintu Pembuangan Tutup', 'Menyala', '-', False),
                    ('plta_a5', 'Indikasi DS Phase Cubicle', 'Masuk', '-', True),
                    ('plta_a6', 'Indikasi Earthing Switch', 'Keluar', '-', True),
                    ('plta_a7', 'Indikasi CB 20 KV', 'Keluar', 'TPL Menyala', True),
                    ('plta_a8', 'Indikasi Earthing Switch', 'Keluar', '-', True),
                    ('plta_a9', 'Indikasi Unit Siap Jalan', 'Menyala', '-', False)
                ]),
                ('plta_b', 'B. CARA PENGOPERASIAAN', [
                    ('plta_b1', 'Sistim Pengatur Unit', 'Lokal', '-', False),
                    ('plta_b2', 'Sistim Komando Unit', 'Unit: ...', '-', True),
                    ('plta_b3', 'Sinkronisasi', '-', '-', False),
                    ('plta_b4', 'Duga Muka Air / Kontrol water level', 'ON / OFF', '-', False),
                    ('plta_b5_1', 'Tombol Putaran Tanpa Beban', 'Berkedip', 'Tunggu', False),
                    ('plta_b5_2', 'Tombol Eksitasi', 'Berkedip', 'Tunggu', False),
                    ('plta_b5_3', 'Tombol Generator', 'Berkedip', 'Tunggu', False),
                    ('plta_b5_4', 'Tombol Putaran Tanpa Beban (AUTO)', 'Berkedip', '-', False),
                    ('plta_b6_1', 'Periksa TPL (CB 20 KV)', 'Berkedip', 'ON', True),
                    ('plta_b6_2', 'Pengaturan beban / frekuensi', '-', '-', False),
                    ('plta_b6_3', 'Pengaturan tegangan eksitasi', '-', '-', False),
                    ('plta_b6_4', 'Putar Switch CB / TPL CB', 'LGB001JD', 'ON', True),
                    ('plta_b6_5', 'Tekan tombol TPL CB paralel', 'Pukul: ...', '-', True)
                ]),
                ('plta_c', 'C. PENGATURAN BEBAN', [
                    ('plta_c1', 'Tekan Tombol Pengatur Beban', '... MW', 'Bertahap', True)
                ]),
                ('plta_d', 'D. PENCATATAN RUTIN', [
                    ('plta_d1', 'Pencatatan rutin harian', '-', '-', False)
                ])
            ]

            global_idx = 1
            for p_key, p_title, p_items in plta_sections:
                table_data.append([Paragraph(p_title, sec_style), "", "", "", ""])
                for item_id, desc, item_default, item_ket, is_custom in p_items:
                    chk_val = request.form.get(f"chk_{item_id}")
                    if chk_val == "on":
                        pos = request.form.get(f"pos_{item_id}", item_default)
                        if is_custom:
                            custom_val = request.form.get(f"custom_input_{item_id}", "").strip()
                            if custom_val:
                                desc = f"{desc} [{custom_val}]"
                        
                        paraf = request.form.get(f"paraf_{item_id}", "✔")
                        ket = request.form.get(f"ket_{item_id}", item_ket)

                        table_data.append([
                            Paragraph(str(global_idx), cell_center),
                            Paragraph(desc, cell_style),
                            Paragraph(pos, cell_center),
                            Paragraph(paraf, cell_center),
                            Paragraph(ket, cell_center)
                        ])
                        wa_details.append(f"{global_idx}. {desc} - Pos: {pos} - Status: {paraf}")
                        global_idx += 1
        elif "KOSAMBI KE PENGHANTAR 70 KV JATILUHUR" in jenis_gangguan:
            sections = [
                ("A. RUANG PANEL 6 KV", [
                    ('qa1', 'PMT/CB panel Trafo 500 KVA / Trafo I'),
                    ('qa2', 'PMT/CB panel Trafo 500 KVA / Trafo II'),
                    ('qa3', 'PMT/CB panel keluaran 6 MB2'),
                    ('qa4', 'PMT/CB panel masukan dari Trafo II'),
                    ('qa5', 'PMT/CB panel masukan dari Trafo III')
                ]),
                ("B. RUANG PANEL 20 KV BUILDING", [
                    ('qb1', 'PMT/CB Masukan dari trafo I'),
                    ('qb2', 'PMT/CB Trafo I 20 / 70 KV 10 MVA'),
                    ('qb3', 'PMT/CB Trafo II 70 / 6,3 KV 5 MVA'),
                    ('qb4', 'PMT/CB Trafo III 70 / 6,3 KV 5 MVA')
                ]),
                ("C. PMT KOSAMBI BAY", [
                    ('qc1', 'PMT / CB 70 KV Kosambi Bay'),
                    ('qc2', 'PMS / DS Line 70 KV Kosambi Bay'),
                    ('qc3', 'PMS / DS Arde Line 70 KV Kosambi Bay'),
                    ('qc4', 'PMS / DS Rel 70 KV Kosambi Bay'),
                    ('qc5', 'PMS / DS Arde Rel 70 KV Kosambi Bay')
                ]),
                ("D. PMT JATILUHUR BAY", [
                    ('qd1', 'PMS / DS Arde Line 70 KV Jatiluhur Bay'),
                    ('qd2', 'PMS / DS Line 70 KV Jatiluhur Bay'),
                    ('qd3', 'PMS / DS Arde Rel 70 KV Jatiluhur Bay'),
                    ('qd4', 'PMS / DS Rel 70 KV Jatiluhur Bay'),
                    ('qd5', 'PMT / CB 70 KV Jatiluhur Bay')
                ]),
                ("E. RUANG PANEL 20 KV BUILDING", [
                    ('qe1', 'PMT / CB Trafo I 20 / 70 KV 10 MVA'),
                    ('qe2', 'PMT / CB Masukan dari Trafo I'),
                    ('qe3_custom', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC'),
                    ('qe4_custom', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC')
                ]),
                ("F. RUANG PANEL 6 KV", [
                    ('qf1', 'PMT / CB panel masukan dari Trafo II'),
                    ('qf2', 'PMT / CB panel masukan dari Trafo III'),
                    ('qf3', 'PMT / CB panel Trafo 500 KVA / Trafo I'),
                    ('qf4', 'PMT / CB panel Trafo 500 KVA / Trafo II'),
                    ('qf5', 'PMT / CB panel keluaran 6 MB2')
                ])
            ]
        elif "JATILUHUR KE PENGHANTAR 70 KV KOSAMBI" in jenis_gangguan:
            sections = [
                ("A. RUANG PANEL 6 KV", [
                    ('pa1', 'PMT/CB panel Trafo 500 KVA / Trafo I'),
                    ('pa2', 'PMT/CB panel Trafo 500 KVA / Trafo II'),
                    ('pa3', 'PMT/CB panel keluaran 6 MB2'),
                    ('pa4', 'PMT/CB panel masukan dari Trafo II'),
                    ('pa5', 'PMT/CB panel masukan dari Trafo III')
                ]),
                ("B. RUANG PANEL 20 KV BUILDING", [
                    ('pb1', 'PMT/CB Masukan dari trafo I'),
                    ('pb2', 'PMT/CB Trafo I 20 / 70 KV 10 MVA'),
                    ('pb3', 'PMT/CB Trafo II 70 / 6,3 KV 5 MVA'),
                    ('pb4', 'PMT/CB Trafo III 70 / 6,3 KV 5 MVA')
                ]),
                ("C. PMT JATILUHUR BAY", [
                    ('pc1', 'PMT / CB 70 KV Jatiluhur Bay'),
                    ('pc2', 'PMS / DS Line 70 KV Jatiluhur Bay'),
                    ('pc3', 'PMS / DS Arde Line 70 KV Jatiluhur Bay'),
                    ('pc4', 'PMS / DS Rel 70 KV Jatiluhur Bay'),
                    ('pc5', 'PMS / DS Arde Rel 70 KV Jatiluhur Bay')
                ]),
                ("D. PMT KOSAMBI BAY", [
                    ('pd1', 'PMS / DS Arde Line 70 KV Kosambi Bay'),
                    ('pd2', 'PMS / DS Line 70 KV Kosambi Bay'),
                    ('pd3', 'PMS / DS Arde Rel 70 KV Kosambi Bay'),
                    ('pd4', 'PMS / DS Rel 70 KV Kosambi Bay'),
                    ('pd5', 'PMT / CB 70 KV Kosambi Bay')
                ]),
                ("E. RUANG PANEL 20 KV BUILDING", [
                    ('pe1', 'PMT / CB Trafo I 20 / 70 KV 10 MVA'),
                    ('pe2', 'PMT / CB Masukan dari Trafo I'),
                    ('pe3_custom', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC'),
                    ('pe4_custom', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC')
                ]),
                ("F. RUANG PANEL 6 KV", [
                    ('pf1', 'PMT / CB panel masukan dari Trafo II'),
                    ('pf2', 'PMT / CB panel masukan dari Trafo III'),
                    ('pf3', 'PMT / CB panel Trafo 500 KVA / Trafo I'),
                    ('pf4', 'PMT / CB panel Trafo 500 KVA / Trafo II'),
                    ('pf5', 'PMT / CB panel keluaran 6 MB2')
                ])
            ]
        else:
            sections = [
                ("A. RUANG PANEL 6,3 KV", [
                    ('chk_a1', 'PMT / CB Panel Trafo 500 KVA / Trafo I'),
                    ('chk_a2', 'PMT / CB Panel Trafo 500 KVA / Trafo II'),
                    ('chk_a3', 'PMT / CB Panel Keluaran 6 MB2')
                ]),
                ("B. RUANG PANEL 20 KV BUILDING", [
                    ('chk_b1', 'PMT / CB Masukan dari Trafo I'),
                    ('chk_b2', 'PMT / CB Trafo I 20 / 70 KV 10 MVA'),
                    ('chk_b3', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA'),
                    ('chk_b4', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA'),
                    ('chk_b5', 'Riset Semua Gangguan'),
                    ('chk_b6', 'Koordinasi dengan Kontrol Building'),
                    ('chk_b7', 'PMT / CB Jatiluhur / Kosambi'),
                    ('chk_b8', 'PMT / CB Trafo I 20 / 70 KV 10 MVA'),
                    ('chk_b9', 'PMT / CB Masukan dari Trafo I'),
                    ('chk_b10', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC'),
                    ('chk_b11', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC'),
                    ('chk_b12', 'Riset Semua Gangguan')
                ]),
                ("C. RUANG PANEL 6 KV", [
                    ('chk_c1', 'Riset Semua Gangguan'),
                    ('chk_c2', 'PMT / CB Panel Masukan dari Trafo II'),
                    ('chk_c3', 'PMT / CB Panel Masukan dari Trafo III'),
                    ('chk_c4', 'PMT / CB Panel Trafo 500 KVA / Trafo I'),
                    ('chk_c5', 'PMT / CB Panel Trafo 500 KVA / Trafo II'),
                    ('chk_c6', 'PMT / CB Panel Keluaran 6 MB2'),
                    ('chk_c7', 'Riset Semua Gangguan')
                ]),
                ("D. CB PANEL DISTRIBUSI 380 V AC TARUM BARAT", [
                    ('chk_d1', 'CB Panel Distribusi 380 V AC Tarum Barat')
                ])
            ]

        if not is_plta_curug:
            global_idx = 1
            for sec_title, items in sections:
                table_data.append([Paragraph(sec_title, sec_style), "", "", "", ""])
                for item_id, desc in items:
                    chk_val = request.form.get(f"chk_{item_id}") or request.form.get(item_id)
                    if chk_val == "on" or "PINDAH LINE" in jenis_gangguan:
                        pukul = request.form.get(f"jam_{item_id}") or default_jam
                        keadaan = request.form.get(f"pos_{item_id}") or "-"
                        ket = request.form.get(f"ket_{item_id}") or "-"
                        
                        final_desc = desc
                        if "Posisi TC" in desc:
                            custom_tc = request.form.get(f"tc_val_{item_id}")
                            if custom_tc:
                                final_desc += f" {custom_tc}"

                        table_data.append([
                            Paragraph(str(global_idx), cell_center),
                            Paragraph(final_desc, cell_style),
                            Paragraph(pukul, cell_center),
                            Paragraph(keadaan, cell_center),
                            Paragraph(ket, cell_center)
                        ])
                        wa_details.append(f"{global_idx}. [{pukul}] {final_desc} - {keadaan}")
                        global_idx += 1

        if len(table_data) == 1:
            table_data.append([
                Paragraph("1", cell_center),
                Paragraph("Pemeriksaan Checklist Otomatis", cell_style),
                Paragraph(default_jam, cell_center),
                Paragraph("Normal", cell_center),
                Paragraph("-", cell_center)
            ])
            wa_details.append(f"1. [{default_jam}] Pemeriksaan Checklist Otomatis - Normal")

    filepath = os.path.join(PDF_FOLDER, filename)

    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        alignment=1,
        fontSize=13,
        spaceAfter=10
    )

    if is_plta_curug:
        plta_unit = request.form.get("plta_unit_no", "-")
        plta_tm = request.form.get("plta_jam_kerja", "-")
        story.append(Paragraph("<b>CHECK LIST OPERASI PLTA MINI HYDRO CURUG</b>", title_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"<b>UNIT No.:</b> {plta_unit} &nbsp;&nbsp;&nbsp;&nbsp; <b>Jam Kerja Unit (TM):</b> {plta_tm}", styles["Normal"]))
    else:
        story.append(Paragraph("<b>LAPORAN NORMALISASI GANGGUAN / MANUVER</b>", title_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"<b>Kategori / Lokasi:</b> {kategori}", styles["Normal"]))
        story.append(Spacer(1, 2))
        story.append(Paragraph(f"<b>Jenis Kegiatan:</b> {jenis_gangguan}", styles["Normal"]))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"<b>Waktu Kejadian:</b> {waktu}", styles["Normal"]))
    story.append(Spacer(1, 8))

    if is_plta_curug:
        t = Table(table_data, colWidths=[25, 227, 95, 60, 147])
    else:
        t = Table(table_data, colWidths=[25, 237, 85, 125, 80])

    table_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]

    for idx, row in enumerate(table_data):
        if isinstance(row[0], Paragraph) and any(row[0].text.startswith(x) for x in ["A.", "B.", "C.", "D.", "E.", "F."]):
            table_styles.append(('SPAN', (0, idx), (-1, idx)))
            table_styles.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#e2e8f0')))
            table_styles.append(('TOPPADDING', (0, idx), (-1, idx), 4))
            table_styles.append(('BOTTOMPADDING', (0, idx), (-1, idx), 4))

    t.setStyle(TableStyle(table_styles))

    story.append(t)
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Pembuat Laporan:</b> {nama_group} ({nama_petugas})", styles["Normal"]))

    doc.build(story)

    joined_details = "\n".join(wa_details)
    raw_message = f"📢 *LAPORAN OPERASIONAL / CHECKLIST* 📢\n\n📌 Kategori: {kategori}\n⚠ Kegiatan: {jenis_gangguan}\n📅 Waktu: {waktu}\n\n⚙️ *Detail Pelaksanaan:*\n{joined_details}\n\n✍️ *Pembuat Laporan:* {nama_group} ({nama_petugas})\n\n_(Laporan otomatis tercatat)_"
    wa_message = urllib.parse.quote(raw_message)

    return render_template_string(RESULT_TEMPLATE, filename=filename, wa_message=wa_message)

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(PDF_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
