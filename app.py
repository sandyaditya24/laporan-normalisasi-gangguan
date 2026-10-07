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

# In-memory database sederhana untuk menyimpan riwayat laporan baru & checklist
HISTORY_LAPORAN_DB = []

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
            transition: opacity 0.3s ease;
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
            z-index: 5;
        }
        .bg-switcher-badge {
            cursor: pointer;
            transition: all 0.2s;
        }
        .bg-switcher-badge:hover {
            background-color: #1d4ed8 !important;
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
                                <span class="badge bg-dark bg-switcher-badge px-3 py-2 rounded-pill fs-7 shadow-sm" onclick="gantiBackgroundPJT()">
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
                        
                        <div>
                            <button type="button" class="btn menu-btn" id="btnMenuLaporanGangguan" onclick="toggleSubMenu('laporan-gangguan-submenu')">
                                <i class="fa-solid fa-triangle-exclamation fa-fw text-warning"></i> Laporan Gangguan <i class="fa-solid fa-chevron-down ms-auto fs-7"></i>
                            </button>
                            <div class="submenu-container" id="laporan-gangguan-submenu">
                                <button type="button" class="btn submenu-btn" id="btnSubBuatLaporanBaru" onclick="pilihMenu('buat-laporan-baru')">
                                    <i class="fa-solid fa-file-circle-plus fa-fw"></i> Buat Laporan Baru
                                </button>
                                <button type="button" class="btn submenu-btn" id="btnSubHistoryGangguan" onclick="pilihMenu('history-gangguan')">
                                    <i class="fa-solid fa-clock-rotate-left fa-fw"></i> Hystori Gangguan
                                </button>
                            </div>
                        </div>

                        <button type="button" class="btn menu-btn" id="btnMenuForm" onclick="pilihMenu('form')">
                            <i class="fa-solid fa-clipboard-list fa-fw"></i> Form Normalisasi & Checklist
                        </button>

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

            <!-- AREA KONTEN -->
            <div class="col-lg-9">
                
                <!-- 1. BUAT LAPORAN BARU -->
                <div class="card content-card mb-4" id="container-buat-laporan-baru" style="display: none;">
                    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="card-header-custom text-white text-center">
                        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-file-circle-plus me-2"></i> BUAT LAPORAN GANGGUAN BARU</h3>
                        <p class="mb-0 text-white-50 small mt-1">Formulir pencatatan kronologi dan detail gangguan operasional</p>
                    </div>
                    <div class="card-body p-4 p-md-5">
                        <form method="POST" action="/generate-laporan-baru">
                            <div class="mb-4">
                                <label for="baru_jenis_gangguan" class="form-label fw-bold text-secondary">Jenis Gangguan:</label>
                                <input type="text" class="form-control" id="baru_jenis_gangguan" name="baru_jenis_gangguan" placeholder="Contoh: Gangguan Trafo Utama / Trip PMT 70 kV" required>
                            </div>

                            <div class="row g-3 mb-4">
                                <div class="col-md-4">
                                    <label for="baru_waktu" class="form-label fw-bold text-secondary">Waktu Gangguan (Jam):</label>
                                    <input type="time" class="form-control" id="baru_waktu" name="baru_waktu" required>
                                </div>
                                <div class="col-md-8">
                                    <label for="baru_tanggal_lengkap" class="form-label fw-bold text-secondary">Tanggal, Bulan, dan Tahun Gangguan:</label>
                                    <input type="date" class="form-control" id="baru_tanggal_lengkap" name="baru_tanggal_lengkap" required>
                                </div>
                            </div>

                            <div class="mb-4">
                                <label for="baru_kronologi" class="form-label fw-bold text-secondary">Kronologi Gangguan:</label>
                                <textarea class="form-control" id="baru_kronologi" name="baru_kronologi" rows="5" placeholder="Jelaskan kronologi kejadian secara detail..." required></textarea>
                            </div>

                            <button type="submit" class="btn btn-primary w-100 py-3 shadow-sm fs-5 btn-custom">
                                <i class="fa-solid fa-paper-plane me-2"></i> Simpan & Catat Laporan Gangguan
                            </button>
                        </form>
                    </div>
                </div>

                <!-- 2. HYSTORY GANGGUAN -->
                <div class="card content-card mb-4" id="container-history-gangguan" style="display: none;">
                    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="card-header-custom text-white text-center">
                        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-clock-rotate-left me-2"></i> HYSTORY GANGGUAN</h3>
                        <p class="mb-0 text-white-50 small mt-1">Daftar riwayat laporan gangguan baru dan checklist normalisasi yang tersimpan</p>
                    </div>
                    <div class="card-body p-4 p-md-5">
                        <h5 class="fw-bold text-dark mb-3"><i class="fa-solid fa-list-check me-2 text-primary"></i> Riwayat Laporan Gangguan Baru</h5>
                        <div class="table-responsive mb-5">
                            <table class="table table-bordered table-hover align-middle bg-white shadow-sm">
                                <thead class="table-dark text-center">
                                    <tr>
                                        <th width="5%">No</th>
                                        <th width="20%">Jenis Gangguan</th>
                                        <th width="15%">Waktu & Tanggal</th>
                                        <th width="45%">Kronologi</th>
                                        <th width="15%">Aksi</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% if history_laporan_baru %}
                                        {% for item in history_laporan_baru %}
                                        <tr>
                                            <td class="text-center fw-bold">{{ loop.index }}</td>
                                            <td class="fw-semibold text-danger">{{ item.jenis }}</td>
                                            <td class="text-center small">{{ item.tanggal }}<br>{{ item.waktu }}</td>
                                            <td class="small">{{ item.kronologi }}</td>
                                            <td class="text-center">
                                                <a href="/download/{{ item.pdf_name }}" class="btn btn-sm btn-primary px-3 shadow-sm" target="_blank">
                                                    <i class="fa-solid fa-download me-1"></i> PDF
                                                </a>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    {% else %}
                                        <tr>
                                            <td colspan="5" class="text-center text-muted py-3">Belum ada riwayat Laporan Gangguan Baru.</td>
                                        </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>

                        <h5 class="fw-bold text-dark mb-3"><i class="fa-solid fa-file-pdf me-2 text-danger"></i> Riwayat Checklist & Laporan PDF Tergenerate</h5>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover align-middle bg-white shadow-sm">
                                <thead class="table-dark text-center">
                                    <tr>
                                        <th width="8%">No</th>
                                        <th width="52%">Nama File Arsip PDF</th>
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
                                            <td colspan="4" class="text-center text-muted py-3">Belum ada file PDF checklist tersimpan.</td>
                                        </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- 3. ARTIKEL SEJARAH BENDUNG CURUG -->
                <div class="card content-card mb-4" id="container-sejarah" style="display: none;">
                    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
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
                                    <button type="button" class="btn-close-img" onclick="toggleCloseImage()" title="Tutup Gambar">
                                        <i class="fa-solid fa-xmark"></i>
                                    </button>
                                    <img src="/static/CURUGTEMPODULU.jpg" alt="Bendung Curug Tempo Dulu" class="img-fluid rounded-4" id="targetImage">
                                </div>
                                <small class="d-block text-muted mt-2 fst-italic" id="imageCaption">Dokumentasi historis kawasan Bendung Curug.</small>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 4. FORM LAPORAN NORMALISASI & CHECKLIST UTAMA -->
                <div class="card content-card" id="container-form-laporan" style="display: none;">
                    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
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
                                    <div class="alert alert-warning border-0 shadow-sm rounded-4 text-center">
                                        <b>CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)</b>
                                    </div>

                                    <!-- A. RUANG PANEL 6,3 KV -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">A. RUANG PANEL 6,3 KV</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB Panel Trafo 500 KVA / Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_a1" value="Dikelurkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_a1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB Panel Trafo 500 KVA / Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_a2" value="Dikelurkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_a2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a3" value="on" checked></td><td class="text-center">3</td><td>PMT / CB Panel Keluaran 6 MB2</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_a3" value="Dikelurkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_a3"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- B. RUANG PANEL 20 KV BUILDING -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">B. RUANG PANEL 20 KV BUILDING</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB Masukan dari Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b1" value="Dikelurkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB Trafo I 20 / 70 KV 10 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b2" value="Dikelurkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b3" value="on" checked></td><td class="text-center">3</td><td>PMT / CB Trafo II 70 / 6,3 KV 5 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b3" value="Dikelurkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b4" value="on" checked></td><td class="text-center">4</td><td>PMT / CB Trafo III 70 / 6,3 KV 5 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b4" value="Dikelurkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b5" value="on" checked></td><td class="text-center">5</td><td>Riset Semua Gangguan</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b5" value="Clear"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b5"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b6" value="on" checked></td><td class="text-center">6</td><td>Koordinasi dengan Kontrol Building</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b6" value="Siap Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b6"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b7" value="on" checked></td><td class="text-center">7</td><td>PMT / CB Jatiluhur / Kosambi</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b7" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b7"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b8" value="on" checked></td><td class="text-center">8</td><td>PMT / CB Trafo I 20 / 70 KV 10 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b8" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b8"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b9" value="on" checked></td><td class="text-center">9</td><td>PMT / CB Masukan dari Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b9" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b9"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b10" value="on" checked></td><td class="text-center">10</td><td>PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC. ..........</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b10" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b10"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b11" value="on" checked></td><td class="text-center">11</td><td>PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC. ..........</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b11" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b11"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b12" value="on" checked></td><td class="text-center">12</td><td>Riset Semua Gangguan</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b12" value="Clear"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b12"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- C. RUANG PANEL 6 KV -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">C. RUANG PANEL 6 KV</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_c1" value="on" checked></td><td class="text-center">1</td><td>Riset Semua Gangguan</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_c1" value="Clear"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_c1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_c2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB Panel Masukan dari Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_c2" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_c2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_c3" value="on" checked></td><td class="text-center">3</td><td>PMT / CB Panel Masukan dari Trafo III</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_c3" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_c3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_c4" value="on" checked></td><td class="text-center">4</td><td>PMT / CB Panel Trafo 500 KVA / Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_c4" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_c4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_c5" value="on" checked></td><td class="text-center">5</td><td>PMT / CB Panel Trafo 500 KVA / Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_c5" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_c5"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_c6" value="on" checked></td><td class="text-center">6</td><td>PMT / CB Panel Keluaran 6 MB2</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_c6" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_c6"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_c7" value="on" checked></td><td class="text-center">7</td><td>Riset Semua Gangguan</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_c7" value="Clear"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_c7"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- D. CB PANEL DISTRIBUSI 380 V AC TARUM BARAT -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">D. CB PANEL DISTRIBUSI 380 V AC TARUM BARAT</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_d1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB Panel Distribusi 380 V AC Tarum Barat</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_d1" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_d1"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- Catatan / Instruksi Akhir -->
                                    <div class="p-3 bg-light border rounded-3 mt-3">
                                        <h6 class="fw-bold text-dark mb-2">Catatan / Instruksi Prosedur:</h6>
                                        <ol class="small text-secondary mb-0 ps-3">
                                            <li>Melaporkan hasil penanganan gangguan ke Operator Kontrol Building</li>
                                            <li>Koordinasi dengan operator Kontrol Bilding untuk menormalkan Pompa Tarum Timur Divisi II</li>
                                        </ol>
                                    </div>
                                </div>
                            </div>

                            <hr class="my-4">
                            
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
                                <i class="fa-solid fa-file-pdf me-2"></i> Buat Laporan PDF Checklist Sekarang
                            </button>
                        </form>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        const backgroundListPJT = [
            { url: '/static/CURUGTEMPODULU.jpg', name: 'Bendung Curug Tempo Dulu' },
            { url: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1920&q=80', name: 'Waduk Ir. H. Djuanda (Jatiluhur)' },
            { url: 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1920&q=80', name: 'Kawasan Aliran Sungai' }
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
            submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
        }

        function pilihMenu(menu) {
            const formContainer = document.getElementById('container-form-laporan');
            const sejarahContainer = document.getElementById('container-sejarah');
            const historyGangguanContainer = document.getElementById('container-history-gangguan');
            const buatLaporanBaruContainer = document.getElementById('container-buat-laporan-baru');
            
            const btnLaporanGroup = document.getElementById('btnMenuLaporanGangguan');
            const btnSubBuatBaru = document.getElementById('btnSubBuatLaporanBaru');
            const btnSubHistory = document.getElementById('btnSubHistoryGangguan');
            const btnForm = document.getElementById('btnMenuForm');
            const btnSejarah = document.getElementById('btnMenuSejarah');

            formContainer.style.display = 'none';
            sejarahContainer.style.display = 'none';
            historyGangguanContainer.style.display = 'none';
            buatLaporanBaruContainer.style.display = 'none';

            btnLaporanGroup.classList.remove('active');
            btnSubBuatBaru.classList.remove('active');
            btnSubHistory.classList.remove('active');
            btnForm.classList.remove('active');
            btnSejarah.classList.remove('active');

            if (menu === 'buat-laporan-baru') {
                buatLaporanBaruContainer.style.display = 'block';
                btnLaporanGroup.classList.add('active');
                btnSubBuatBaru.classList.add('active');
                document.getElementById('laporan-gangguan-submenu').style.display = 'block';
            } else if (menu === 'history-gangguan') {
                historyGangguanContainer.style.display = 'block';
                btnLaporanGroup.classList.add('active');
                btnSubHistory.classList.add('active');
                document.getElementById('laporan-gangguan-submenu').style.display = 'block';
            } else if (menu === 'form') {
                formContainer.style.display = 'block';
                btnForm.classList.add('active');
            } else if (menu === 'sejarah') {
                sejarahContainer.style.display = 'block';
                btnSejarah.classList.add('active');
            }
        }

        function kosongkanKanan() {
            document.getElementById('container-form-laporan').style.display = 'none';
            document.getElementById('container-sejarah').style.display = 'none';
            document.getElementById('container-history-gangguan').style.display = 'none';
            document.getElementById('container-buat-laporan-baru').style.display = 'none';

            document.getElementById('btnMenuLaporanGangguan').classList.remove('active');
            document.getElementById('btnSubBuatLaporanBaru').classList.remove('active');
            document.getElementById('btnSubHistoryGangguan').classList.remove('active');
            document.getElementById('btnMenuForm').classList.remove('active');
            document.getElementById('btnMenuSejarah').classList.remove('active');
        }

        function switchMode(mode) {
            const secManual = document.getElementById('section-manual');
            const secOtomatis = document.getElementById('section-otomatis');
            const wrapManual = document.getElementById('wrapper-jenis-manual');
            const wrapOtomatis = document.getElementById('wrapper-jenis-otomatis');
            const inputManual = document.getElementById('jenis_gangguan_manual');
            const selectOtomatis = document.getElementById('jenis_gangguan_otomatis');
            
            if (mode === 'manual') {
                secManual.style.display = 'block';
                secOtomatis.style.display = 'none';
                wrapManual.style.display = 'block';
                wrapOtomatis.style.display = 'none';
                inputManual.setAttribute('required', 'required');
                selectOtomatis.removeAttribute('required');
            } else {
                secManual.style.display = 'none';
                secOtomatis.style.display = 'block';
                wrapManual.style.display = 'none';
                wrapOtomatis.style.display = 'block';
                inputManual.removeAttribute('required');
                selectOtomatis.setAttribute('required', 'required');
            }
        }

        function switchOtomatisSub(val) {
            document.getElementById('sub-section-gi-curug').style.display = val.includes("GARDU INDUK") ? 'block' : 'none';
        }

        function updatePreview(val) {
            if (!val) return;
            const dt = new Date(val);
            const hariList = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
            const bulanList = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
            document.getElementById('preview-waktu').innerText = 'Format Tampil: ' + hariList[dt.getDay()] + ', ' + dt.getDate() + ' ' + bulanList[dt.getMonth()] + ' ' + dt.getFullYear() + ' Pukul ' + String(dt.getHours()).padStart(2, '0') + ':' + String(dt.getMinutes()).padStart(2, '0') + ' WIB';
        }

        function tambahBaris() {
            const container = document.getElementById('penanganan-container');
            const newNum = container.getElementsByClassName('penanganan-row').length + 1;
            const newRow = document.createElement('div');
            newRow.className = 'row g-2 mb-2 penanganan-row';
            newRow.innerHTML = '<div class="col-md-1"><input type="text" class="form-control text-center nomor-urut bg-white" value="' + newNum + '" readonly></div>' +
                               '<div class="col-md-5"><input type="text" class="form-control" name="penanganan[]" placeholder="Jenis Penanganan" required></div>' +
                               '<div class="col-md-2"><input type="text" class="form-control text-center" name="jam_item[]" placeholder="Jam" required></div>' +
                               '<div class="col-md-3"><input type="text" class="form-control text-center" name="status_item[]" placeholder="Status" required></div>' +
                               '<div class="col-md-1"><button type="button" class="btn btn-danger w-100 btn-custom" onclick="hapusBaris(this)"><i class="fa-solid fa-trash"></i></button></div>';
            container.appendChild(newRow);
        }

        function hapusBaris(btn) {
            const container = document.getElementById('penanganan-container');
            if (container.getElementsByClassName('penanganan-row').length > 1) {
                btn.closest('.penanganan-row').remove();
            } else {
                alert("Minimal harus ada 1 baris!");
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
                        <p class="text-muted mb-4">Laporan dan file PDF telah berhasil disusun serta otomatis tersimpan ke Hystori Gangguan.</p>
                        <a href="/download/{{ filename }}" class="btn btn-primary w-100 mb-3 shadow-sm" target="_blank">
                            <i class="fa-solid fa-download me-2"></i> Unduh File PDF
                        </a>
                        <a href="https://api.whatsapp.com/send?text={{ wa_message }}" class="btn btn-success w-100 mb-3 shadow-sm" target="_blank">
                            <i class="fa-brands fa-whatsapp me-2"></i> Kirim ke WhatsApp
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
    return render_template_string(HTML_TEMPLATE, pdf_files=pdf_files, history_laporan_baru=HISTORY_LAPORAN_DB)

@app.route("/generate-laporan-baru", methods=["POST"])
def generate_laporan_baru():
    jenis = request.form["baru_jenis_gangguan"]
    waktu = request.form["baru_waktu"]
    tanggal = request.form["baru_tanggal_lengkap"]
    kronologi = request.form["baru_kronologi"]

    clean_jenis = re.sub(r'[^a-zA-Z0-9]', '_', jenis).strip('_')[:30]
    filename = f"laporan_baru_{clean_jenis}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.pdf"
    filepath = os.path.join(PDF_FOLDER, filename)

    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>LAPORAN GANGGUAN OPERASIONAL BARU</b>", ParagraphStyle("Title", parent=styles["Heading1"], alignment=1, fontSize=14, spaceAfter=15)),
        Paragraph(f"<b>Jenis Gangguan:</b> {jenis}", styles["Normal"]),
        Spacer(1, 6),
        Paragraph(f"<b>Waktu Kejadian:</b> Pukul {waktu} WIB", styles["Normal"]),
        Spacer(1, 6),
        Paragraph(f"<b>Tanggal, Bulan & Tahun:</b> {tanggal}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("<b>Kronologi Gangguan:</b>", ParagraphStyle("Sub", parent=styles["Normal"], fontName="Helvetica-Bold")),
        Spacer(1, 4),
        Paragraph(kronologi, styles["Normal"])
    ]
    doc.build(story)

    HISTORY_LAPORAN_DB.insert(0, {
        "jenis": jenis,
        "waktu": f"Pukul {waktu} WIB",
        "tanggal": tanggal,
        "kronologi": kronologi,
        "pdf_name": filename
    })

    raw_msg = f"📢 *LAPORAN GANGGUAN BARU* 📢\n\n⚠ Gangguan: {jenis}\n📅 Tanggal: {tanggal}\n⏰ Waktu: {waktu}\n\n📝 *Kronologi:*\n{kronologi}"
    wa_message = urllib.parse.quote(raw_msg)

    return render_template_string(RESULT_TEMPLATE, filename=filename, wa_message=wa_message)

@app.route("/generate", methods=["POST"])
def generate():
    kategori = request.form["kategori"]
    mode = request.form.get("mode_pencatatan", "manual")
    jenis_gangguan = request.form.get("jenis_gangguan_manual", "-") if mode == "manual" else request.form.get("jenis_gangguan_otomatis", "-")
    waktu_raw = request.form["waktu"]
    
    try:
        dt = datetime.strptime(waktu_raw, "%Y-%m-%dT%H:%M")
        waktu = f"{dt.day} {dt.strftime('%B %Y')} Pukul {dt.strftime('%H:%M')} WIB"
        file_date_str = dt.strftime('%d-%m-%Y_%H%M')
    except:
        waktu = waktu_raw
        file_date_str = datetime.now().strftime('%d-%m-%Y_%H%M')

    clean_jenis = re.sub(r'[^a-zA-Z0-9]', '_', jenis_gangguan).strip('_')[:30]
    filename = f"checklist_{clean_jenis}_{file_date_str}.pdf"
    filepath = os.path.join(PDF_FOLDER, filename)

    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>LAPORAN NORMALISASI & CHECKLIST</b>", ParagraphStyle("Title", parent=styles["Heading1"], alignment=1, fontSize=14, spaceAfter=10)),
        Paragraph(f"<b>Kategori:</b> {kategori}", styles["Normal"]),
        Spacer(1, 4),
        Paragraph(f"<b>Kegiatan:</b> {jenis_gangguan}", styles["Normal"]),
        Spacer(1, 4),
        Paragraph(f"<b>Waktu:</b> {waktu}", styles["Normal"])
    ]
    doc.build(story)

    raw_msg = f"📢 *CHECKLIST NORMALISASI* 📢\n\n📌 Kategori: {kategori}\n⚠ Kegiatan: {jenis_gangguan}\n📅 Waktu: {waktu}"
    wa_message = urllib.parse.quote(raw_msg)

    return render_template_string(RESULT_TEMPLATE, filename=filename, wa_message=wa_message)

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(PDF_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
