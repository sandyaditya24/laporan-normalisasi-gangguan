from flask import Flask, render_template_string, request, send_file, redirect, url_for, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
import re
import urllib.parse
from datetime import datetime
from pegawai import pegawai_bp
from faq import faq_bp
from google import genai  # Pustaka untuk Google Gemini AI

app = Flask(__name__)
app.register_blueprint(pegawai_bp)
app.register_blueprint(faq_bp)

PDF_FOLDER = "static"
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

# Google GenAI Client dibuat saat endpoint AI dipanggil.
def get_ai_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY belum diset. Set environment variable GEMINI_API_KEY terlebih dahulu."
        )
    return genai.Client(api_key=api_key)

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
                                <i class="fa-solid fa-shield-halved me-1"></i> Enterprise v3.4
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

                        <button type="button" class="btn menu-btn" id="btnMenuPegawai" onclick="pilihMenu('struktural-pegawai')">
                            <i class="fa-solid fa-sitemap fa-fw"></i> Struktural Pegawai
                        </button>

                        <!-- TOMBOL MENU BARU UNTUK ASISTEN AI Q&A -->
                        <a href="/ai-chat" class="btn menu-btn text-decoration-none" id="btnMenuAI">
                            <i class="fa-solid fa-robot fa-fw text-info"></i> Asisten AI Q&A
                        </a>
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

                <!-- STRUKTURAL PEGAWAI (DIMUAT DARI pegawai.py VIA FETCH) -->
                <div id="container-struktural-pegawai-wrapper"></div>

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
                                    <option value="CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV JATILUHUR KE PENGHANTAR 70 KV KOSAMBI (PLN)">2. CHECK LIST PINDAH LINE (JATILUHUR -> KOSAMBI)</option>
                                    <option value="CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV KOSAMBI KE PENGHANTAR 70 KV JATILUHUR (PLN)">3. CHECK LIST PINDAH LINE (KOSAMBI -> JATILUHUR)</option>
                                    <option value="CHECK LIST OPERASI PLTA MINI HYDRO CURUG">4. CHECK LIST OPERASI PLTA MINI HYDRO CURUG (F-20/DPL/IK.10-01)</option>
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
                                
                                <!-- SUB-SECTION 1: GI CURUG TRIP -->
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
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB Panel Trafo 500 KVA / Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_a1" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_a1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB Panel Trafo 500 KVA / Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_a2" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_a2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_a3" value="on" checked></td><td class="text-center">3</td><td>PMT / CB Panel Keluaran 6 MB2</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_a3" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_a3"></td></tr>
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
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB Masukan dari Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b1" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB Trafo I 20 / 70 KV 10 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b2" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b3" value="on" checked></td><td class="text-center">3</td><td>PMT / CB Trafo II 70 / 6,3 KV 5 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b3" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b4" value="on" checked></td><td class="text-center">4</td><td>PMT / CB Trafo III 70 / 6,3 KV 5 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b4" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b5" value="on" checked></td><td class="text-center">5</td><td>Riset Semua Gangguan</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b5" value="Clear"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b5"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b6" value="on" checked></td><td class="text-center">6</td><td>Koordinasi dengan Kontrol Building</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b6" value="Siap Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b6"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b7" value="on" checked></td><td class="text-center">7</td><td>PMT / CB Jatiluhur / Kosambi</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b7" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b7"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b8" value="on" checked></td><td class="text-center">8</td><td>PMT / CB Trafo I 20 / 70 KV 10 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b8" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b8"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b9" value="on" checked></td><td class="text-center">9</td><td>PMT / CB Masukan dari Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_b9" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_b9"></td></tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b10" value="on" checked></td>
                                                    <td class="text-center">10</td>
                                                    <td>
                                                        PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC. 
                                                        <select class="form-select form-select-sm d-inline-block w-auto" name="tc_b10" style="display:inline-block; width:80px;">
                                                            {% for i in range(1, 21) %}
                                                            <option value="{{ i }}">{{ i }}</option>
                                                            {% endfor %}
                                                        </select>
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_b10" value="Dimasukan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_b10"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_b11" value="on" checked></td>
                                                    <td class="text-center">11</td>
                                                    <td>
                                                        PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC. 
                                                        <select class="form-select form-select-sm d-inline-block w-auto" name="tc_b11" style="display:inline-block; width:80px;">
                                                            {% for i in range(1, 21) %}
                                                            <option value="{{ i }}">{{ i }}</option>
                                                            {% endfor %}
                                                        </select>
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_b11" value="Dimasukan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_b11"></td>
                                                </tr>
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
                                </div>

                                <!-- SUB-SECTION 2: CHECK LIST PINDAH LINE (JATILUHUR -> KOSAMBI) -->
                                <div id="sub-section-pindah-line-jtl-ksb" style="display: none;">
                                    <div class="alert alert-primary border-0 shadow-sm rounded-4 text-center">
                                        <b>CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI JATILUHUR KE KOSAMBI (F-20/DPL/IK.12-01)</b>
                                    </div>

                                    <!-- A. RUANG PANEL 6 KV -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">A. RUANG PANEL 6 KV</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_a1" value="on" checked></td><td class="text-center">1</td><td>PMT/CB panel Trafo 500 KVA / Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_a1" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_a1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_a2" value="on" checked></td><td class="text-center">2</td><td>PMT/CB panel Trafo 500 KVA / Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_a2" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_a2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_a3" value="on" checked></td><td class="text-center">3</td><td>PMT/CB panel keluaran 6 MB2</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_a3" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_a3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_a4" value="on" checked></td><td class="text-center">4</td><td>PMT/CB panel masukan dari Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_a4" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_a4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_a5" value="on" checked></td><td class="text-center">5</td><td>PMT/CB panel masukan dari Trafo III</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_a5" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_a5"></td></tr>
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
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_b1" value="on" checked></td><td class="text-center">1</td><td>PMT/CB Masukan dari trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_b1" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_b1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_b2" value="on" checked></td><td class="text-center">2</td><td>PMT/CB Trafo I 20 / 70 KV 10 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_b2" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_b2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_b3" value="on" checked></td><td class="text-center">3</td><td>PMT/CB Trafo II 70 / 6,3 KV 5 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_b3" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_b3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_b4" value="on" checked></td><td class="text-center">4</td><td>PMT/CB Trafo III 70 / 6,3 KV 5 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_b4" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_b4"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- C. PMT JATILUHUR BAY -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">C. PMT JATILUHUR BAY</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_c1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_c1" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_c1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_c2" value="on" checked></td><td class="text-center">2</td><td>PMS / DS Line 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_c2" value="Tdk. dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_c2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_c3" value="on" checked></td><td class="text-center">3</td><td>PMS / DS Arde Line 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_c3" value="Keluar"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_c3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_c4" value="on" checked></td><td class="text-center">4</td><td>PMS / DS Rel 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_c4" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_c4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_c5" value="on" checked></td><td class="text-center">5</td><td>PMS / DS Arde Rel 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_c5" value="Keluar"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_c5"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- D. PMT KOSAMBI BAY -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">D. PMT KOSAMBI BAY</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_d1" value="on" checked></td><td class="text-center">1</td><td>PMS / DS Arde Line 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_d1" value="Keluar"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_d1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_d2" value="on" checked></td><td class="text-center">2</td><td>PMS / DS Line 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_d2" value="Masuk"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_d2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_d3" value="on" checked></td><td class="text-center">3</td><td>PMS / DS Arde Rel 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_d3" value="Keluar"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_d3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_d4" value="on" checked></td><td class="text-center">4</td><td>PMS / DS Rel 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_d4" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_d4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_d5" value="on" checked></td><td class="text-center">5</td><td>PMT / CB 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_d5" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_d5"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- E. RUANG PANEL 20 KV BUILDING -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">E. RUANG PANEL 20 KV BUILDING</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_e1" value="on" checked></td><td class="text-center">1</td><td>PMT/CB Trafo I 20 / 70 KV 10 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_e1" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_e1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_e2" value="on" checked></td><td class="text-center">2</td><td>PMT/CB Masukan dari trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_e2" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_e2"></td></tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_e3" value="on" checked></td>
                                                    <td class="text-center">3</td>
                                                    <td>
                                                        PMT/CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC. 
                                                        <select class="form-select form-select-sm d-inline-block w-auto" name="tc_pl_e3" style="display:inline-block; width:80px;">
                                                            {% for i in range(1, 21) %}
                                                            <option value="{{ i }}">{{ i }}</option>
                                                            {% endfor %}
                                                        </select>
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_e3" value="Dimasukan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_e3"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_e4" value="on" checked></td>
                                                    <td class="text-center">4</td>
                                                    <td>
                                                        PMT/CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC. 
                                                        <select class="form-select form-select-sm d-inline-block w-auto" name="tc_pl_e4" style="display:inline-block; width:80px;">
                                                            {% for i in range(1, 21) %}
                                                            <option value="{{ i }}">{{ i }}</option>
                                                            {% endfor %}
                                                        </select>
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_e4" value="Dimasukan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_e4"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- F. RUANG PANEL 6 KV -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">F. RUANG PANEL 6 KV</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_f1" value="on" checked></td><td class="text-center">1</td><td>PMT/CB panel masukan dari Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_f1" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_f1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_f2" value="on" checked></td><td class="text-center">2</td><td>PMT/CB panel masukan dari Trafo III</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_f2" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_f2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_f3" value="on" checked></td><td class="text-center">3</td><td>PMT/CB panel Trafo 500 KVA / Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_f3" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_f3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_f4" value="on" checked></td><td class="text-center">4</td><td>PMT/CB panel Trafo 500 KVA / Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_f4" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_f4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_pl_f5" value="on" checked></td><td class="text-center">5</td><td>PMT/CB panel keluaran 6 MB2</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_pl_f5" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_pl_f5"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- Pelaporan Akhir -->
                                    <div class="p-3 bg-light border rounded-3 mt-3">
                                        <h6 class="fw-bold text-dark mb-2">Instruksi Akhir:</h6>
                                        <p class="small text-secondary mb-0">IV. Melaporkan hasil pelaksanaan manuver (pindah line) ke kontrol Building.</p>
                                    </div>
                                </div>

                                <!-- SUB-SECTION 3: CHECK LIST PINDAH LINE (KOSAMBI -> JATILUHUR) [F-20/DPL/IK.12-02] -->
                                <div id="sub-section-pindah-line-ksb-jtl" style="display: none;">
                                    <div class="alert alert-success border-0 shadow-sm rounded-4 text-center">
                                        <b>CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI KOSAMBI KE JATILUHUR (F-20/DPL/IK.12-02)</b>
                                    </div>

                                    <!-- A. RUANG PANEL 6 KV -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">A. RUANG PANEL 6 KV</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_a1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB panel trafo 500 KVA / Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_a1" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_a1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_a2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB panel trafo 500 KVA / Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_a2" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_a2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_a3" value="on" checked></td><td class="text-center">3</td><td>PMT / CB panel keluaran 6 MB2</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_a3" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_a3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_a4" value="on" checked></td><td class="text-center">4</td><td>PMT / CB panel masukan dari Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_a4" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_a4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_a5" value="on" checked></td><td class="text-center">5</td><td>PMT / CB panel masukan dari Trafo III</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_a5" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_a5"></td></tr>
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
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_b1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB Masukan dari trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_b1" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_b1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_b2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB Trafo I 20 / 70 KV 10 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_b2" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_b2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_b3" value="on" checked></td><td class="text-center">3</td><td>PMT / CB Trafo II 70 / 6,3 KV 5 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_b3" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_b3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_b4" value="on" checked></td><td class="text-center">4</td><td>PMT / CB Trafo III 70 / 6,3 KV 5 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_b4" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_b4"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- C. PMT KOSAMBI BAY -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">C. PMT KOSAMBI BAY</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_c1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_c1" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_c1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_c2" value="on" checked></td><td class="text-center">2</td><td>PMS / DS Line 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_c2" value="Tdk. dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_c2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_c3" value="on" checked></td><td class="text-center">3</td><td>PMS / DS Arde Line 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_c3" value="Keluar"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_c3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_c4" value="on" checked></td><td class="text-center">4</td><td>PMS / DS Rel 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_c4" value="Dikeluarkan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_c4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_c5" value="on" checked></td><td class="text-center">5</td><td>PMS / DS Arde Rel 70 KV Kosambi Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_c5" value="Keluar"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_c5"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- D. PMT JATILUHUR BAY -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">D. PMT JATILUHUR BAY</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_d1" value="on" checked></td><td class="text-center">1</td><td>PMS / DS Arde Line 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_d1" value="Keluar"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_d1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_d2" value="on" checked></td><td class="text-center">2</td><td>PMS / DS Line 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_d2" value="Masuk"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_d2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_d3" value="on" checked></td><td class="text-center">3</td><td>PMS / DS Arde Rel 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_d3" value="Keluar"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_d3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_d4" value="on" checked></td><td class="text-center">4</td><td>PMS / DS Rel 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_d4" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_d4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_d5" value="on" checked></td><td class="text-center">5</td><td>PMT / CB 70 KV Jatiluhur Bay</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_d5" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_d5"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- E. RUANG PANEL 20 KV BUILDING -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">E. RUANG PANEL 20 KV BUILDING</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_e1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB Trafo I 20 / 70 KV 10 MVA</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_e1" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_e1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_e2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB Masukan dari trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_e2" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_e2"></td></tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_e3" value="on" checked></td>
                                                    <td class="text-center">3</td>
                                                    <td>
                                                        PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC. 
                                                        <select class="form-select form-select-sm d-inline-block w-auto" name="tc_ksb_e3" style="display:inline-block; width:80px;">
                                                            {% for i in range(1, 21) %}
                                                            <option value="{{ i }}">{{ i }}</option>
                                                            {% endfor %}
                                                        </select>
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_e3" value="Dimasukan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_e3"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_e4" value="on" checked></td>
                                                    <td class="text-center">4</td>
                                                    <td>
                                                        PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC. 
                                                        <select class="form-select form-select-sm d-inline-block w-auto" name="tc_ksb_e4" style="display:inline-block; width:80px;">
                                                            {% for i in range(1, 21) %}
                                                            <option value="{{ i }}">{{ i }}</option>
                                                            {% endfor %}
                                                        </select>
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_e4" value="Dimasukan"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_e4"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- F. RUANG PANEL 6 KV -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">F. RUANG PANEL 6 KV</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Keadaan / Posisi</th><th width="20%">Pukul (Jam)</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_f1" value="on" checked></td><td class="text-center">1</td><td>PMT / CB panel masukan dari Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_f1" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_f1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_f2" value="on" checked></td><td class="text-center">2</td><td>PMT / CB panel masukan dari Trafo III</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_f2" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_f2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_f3" value="on" checked></td><td class="text-center">3</td><td>PMT / CB panel Trafo 500 KVA / Trafo I</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_f3" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_f3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_f4" value="on" checked></td><td class="text-center">4</td><td>PMT / CB panel Trafo 500 KVA / Trafo II</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_f4" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_f4"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_ksb_f5" value="on" checked></td><td class="text-center">5</td><td>PMT / CB panel keluaran 6 MB2</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_ksb_f5" value="Dimasukan"></td><td><input type="text" class="form-control form-control-sm text-center" name="jam_ksb_f5"></td></tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- Pelaporan Akhir -->
                                    <div class="p-3 bg-light border rounded-3 mt-3">
                                        <h6 class="fw-bold text-dark mb-2">Instruksi Akhir:</h6>
                                        <p class="small text-secondary mb-0">IV. Melaporkan hasil pelaksanaan manuver (pindah line) ke kontrol Building.</p>
                                    </div>
                                </div>

                                <!-- SUB-SECTION 4: CHECK LIST OPERASI PLTA MINI HYDRO CURUG [F-20/DPL/IK.10-01] -->
                                <div id="sub-section-mini-hydro" style="display: none;">
                                    <div class="alert alert-info border-0 shadow-sm rounded-4 text-center">
                                        <b>CHECK LIST OPERASI PLTA MINI HYDRO CURUG (F-20/DPL/IK.10-01)</b>
                                    </div>

                                    <!-- I. PERSIAPAN -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">I. PERSIAPAN</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="50%">Uraian Kegiatan Persiapan</th><th width="25%">Status / Keterangan</th><th width="15%">Paraf</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_i1" value="on" checked></td>
                                                    <td class="text-center">1</td>
                                                    <td>Koordinasi debit air / Tinggi Muka air dengan Operator Bendung Curug Divisi II</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_i1" value="Sudah"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_i1"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_i2" value="on" checked></td>
                                                    <td class="text-center">2</td>
                                                    <td>Koordinasi dengan Operator Control Building di Jatiluhur</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_i2" value="Sudah"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_i2"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- II & III & IV & V. PELAKSANAAN & PENGECEKAN AWAL -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">II, III, IV, V. PELAKSANAAN & PENGECEKAN TEKANAN</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="50%">Uraian Pengecekan</th><th width="25%">Nilai / Target</th><th width="15%">Paraf</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_p1" value="on" checked></td>
                                                    <td class="text-center">1</td>
                                                    <td>Pelaksanaan Pengoperasian Unit Mini Hydro</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_p1" value="Normal"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_p1"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_p2" value="on" checked></td>
                                                    <td class="text-center">2</td>
                                                    <td>Pengecekan Air Baku I & II (Tekanan 3 bar / lebih)</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_p2" value=">= 3 bar"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_p2"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_p3" value="on" checked></td>
                                                    <td class="text-center">3</td>
                                                    <td>Pengecekan Sudu - Sudu (Tekanan 60 bar)</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_p3" value="60 bar"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_p3"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_p4" value="on" checked></td>
                                                    <td class="text-center">4</td>
                                                    <td>Pengecekan Down Stream (Tekanan 120 bar)</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_p4" value="120 bar"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_p4"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- A. RUANG PANEL CONTROL ROOM -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">A. RUANG PANEL CONTROL ROOM</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="45%">Uraian</th><th width="25%">Posisi / Isian</th><th width="15%">Paraf</th><th width="10%">Jam</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a1" value="on" checked></td>
                                                    <td class="text-center">1</td>
                                                    <td>Pada jendela alarm tidak ada indikasi gangguan</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a1" value="Clear / Aman"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a1"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a1"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a2" value="on" checked></td>
                                                    <td class="text-center">2</td>
                                                    <td>
                                                        Tinggi Muka Air:<br>
                                                        - Tinggi Air Udik: <input type="text" class="form-control form-control-sm d-inline-block mt-1" name="pos_mh_udik" placeholder="Isi Tinggi Air Udik"><br>
                                                        - Tinggi Air Hilir: <input type="text" class="form-control form-control-sm d-inline-block mt-1" name="pos_mh_hilir" placeholder="Isi Tinggi Air Hilir"><br>
                                                        - Posisi saring sampah unit: <input type="text" class="form-control form-control-sm d-inline-block mt-1" name="pos_mh_sampah" placeholder="Posisi saring sampah">
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a2" value="Normal"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a2"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a2"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a3" value="on" checked></td>
                                                    <td class="text-center">3</td>
                                                    <td>Kriteria berhenti pada posisi stabil / indikator tombol stop</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a3" value="Stabil"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a3"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a3"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a4" value="on" checked></td>
                                                    <td class="text-center">4</td>
                                                    <td>Posisi Pintu Pembuangan</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a4" value="Tutup"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a4"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a4"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a5" value="on" checked></td>
                                                    <td class="text-center">5</td>
                                                    <td>Indikasi DS Phase Cubicle</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a5" value="GTA 030 JD"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a5"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a5"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a6" value="on" checked></td>
                                                    <td class="text-center">6</td>
                                                    <td>Indikasi Earthing Switch</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a6" value="GTA 031 JS"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a6"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a6"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a7" value="on" checked></td>
                                                    <td class="text-center">7</td>
                                                    <td>Indikasi CB 20 KV</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a7" value="LGB 001 JD"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a7"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a7"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a8" value="on" checked></td>
                                                    <td class="text-center">8</td>
                                                    <td>Indikasi Earthing Switch</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a8" value="LGB 031 JS"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a8"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a8"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_a9" value="on" checked></td>
                                                    <td class="text-center">9</td>
                                                    <td>Indikasi Unit Siap Jalan</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_a9" value="Ready / Siap"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_mh_a9"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="jam_mh_a9"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- B. CARA PENGOPERASIAAN -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">B. CARA PENGOPERASIAAN</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="50%">Tahapan Pengoperasian / Sinkronisasi</th><th width="25%">Posisi / Status</th><th width="15%">Keterangan</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_b1" value="on" checked></td><td class="text-center">1</td><td>Sistim Pengatur Unit</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_b1" value="Normal"></td><td><input type="text" class="form-control form-control-sm text-center" name="ket_mh_b1"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_b2" value="on" checked></td><td class="text-center">2</td><td>Sistim Komando Unit</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_b2" value="Manual / Auto"></td><td><input type="text" class="form-control form-control-sm text-center" name="ket_mh_b2"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_b3" value="on" checked></td><td class="text-center">3</td><td>Sinkronisasi (Jika manual, hubungkan alat sinkronisasi portable)</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_b3" value="Terkoneksi"></td><td><input type="text" class="form-control form-control-sm text-center" name="ket_mh_b3"></td></tr>
                                                <tr><td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_b4" value="on" checked></td><td class="text-center">4</td><td>Duga Muka Air / Kontrol water level</td><td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_b4" value="Terkontrol"></td><td><input type="text" class="form-control form-control-sm text-center" name="ket_mh_b4"></td></tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_b5" value="on" checked></td>
                                                    <td class="text-center">5</td>
                                                    <td>
                                                        Pengoperasian Unit (Manual / Auto):<br>
                                                        - Tekan "Putaran Tanpa Beban"<br>
                                                        - Tekan "Eksitasi"<br>
                                                        - Tekan "Generator"
                                                    </td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_b5" value="Executed"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_mh_b5" value="Tunggu s/d tdk berkedip"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_b6" value="on" checked></td>
                                                    <td class="text-center">6</td>
                                                    <td>Sinkronisasi (Auto / Manual & CB LGB001JD ke posisi ON)</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_b6" value="Paralel ON"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_mh_b6" placeholder="Pukul ... wib"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- C. PENGATURAN BEBAN & D. CATATAN -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded-3">C. PENGATURAN BEBAN & D. CATATAN RUTIN</h6>
                                    <div class="table-responsive mb-3">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr><th width="5%">Pilih</th><th width="5%">No</th><th width="50%">Uraian Pengaturan</th><th width="25%">Target / Posisi</th><th width="15%">Keterangan</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_mh_c1" value="on" checked></td>
                                                    <td class="text-center">1</td>
                                                    <td>Tekan Tombol Pengatur Beban / Frekuensi (naik/turun) hingga stabil</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_mh_c1" value="Stabil"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_mh_c1"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- D. PENCATATAN RUTIN -->
                                    <div class="p-3 bg-light border rounded-3 mt-3">
                                        <h6 class="fw-bold text-dark mb-2">D. Catatan Rutin:</h6>
                                        <p class="small text-secondary mb-0">Selanjutnya pencatatan rutin dengan blangko laporan harian.</p>
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

        // Ambil data struktural pegawai dari blueprint secara asinkron saat pertama kali dimuat
        window.addEventListener('DOMContentLoaded', () => {
            fetch('/get-struktural-pegawai')
                .then(res => res.text())
                .then(html => {
                    document.getElementById('container-struktural-pegawai-wrapper').innerHTML = html;
                });
        });

        function pilihMenu(menu) {
            const formContainer = document.getElementById('container-form-laporan');
            const sejarahContainer = document.getElementById('container-sejarah');
            const historyGangguanContainer = document.getElementById('container-history-gangguan');
            const buatLaporanBaruContainer = document.getElementById('container-buat-laporan-baru');
            const pegawaiContainer = document.getElementById('container-struktural-pegawai');
            
            const btnLaporanGroup = document.getElementById('btnMenuLaporanGangguan');
            const btnSubBuatBaru = document.getElementById('btnSubBuatLaporanBaru');
            const btnSubHistory = document.getElementById('btnSubHistoryGangguan');
            const btnForm = document.getElementById('btnMenuForm');
            const btnSejarah = document.getElementById('btnMenuSejarah');
            const btnPegawai = document.getElementById('btnMenuPegawai');

            formContainer.style.display = 'none';
            sejarahContainer.style.display = 'none';
            historyGangguanContainer.style.display = 'none';
            buatLaporanBaruContainer.style.display = 'none';
            if (pegawaiContainer) pegawaiContainer.style.display = 'none';

            // Reset active classes
            btnSubBuatBaru.classList.remove('active');
            btnSubHistory.classList.remove('active');
            btnForm.classList.remove('active');
            btnSejarah.classList.remove('active');
            btnPegawai.classList.remove('active');
            btnLaporanGroup.classList.remove('active');

            if (menu === 'buat-laporan-baru') {
                buatLaporanBaruContainer.style.display = 'block';
                btnSubBuatBaru.classList.add('active');
                btnLaporanGroup.classList.add('active');
            } else if (menu === 'history-gangguan') {
                historyGangguanContainer.style.display = 'block';
                btnSubHistory.classList.add('active');
                btnLaporanGroup.classList.add('active');
            } else if (menu === 'form') {
                formContainer.style.display = 'block';
                btnForm.classList.add('active');
            } else if (menu === 'sejarah') {
                sejarahContainer.style.display = 'block';
                btnSejarah.classList.add('active');
            } else if (menu === 'struktural-pegawai') {
                if (pegawaiContainer) pegawaiContainer.style.display = 'block';
                btnPegawai.classList.add('active');
            }
        }

        function kosongkanKanan() {
            document.getElementById('container-form-laporan').style.display = 'none';
            document.getElementById('container-sejarah').style.display = 'none';
            document.getElementById('container-history-gangguan').style.display = 'none';
            document.getElementById('container-buat-laporan-baru').style.display = 'none';
            const pegawaiContainer = document.getElementById('container-struktural-pegawai');
            if (pegawaiContainer) pegawaiContainer.style.display = 'none';

            // Remove active states
            document.querySelectorAll('.menu-btn, .submenu-btn').forEach(btn => btn.classList.remove('active'));
        }

        function toggleCloseImage() {
            const wrapper = document.getElementById('imageWrapper');
            wrapper.style.display = 'none';
        }

        function switchMode(mode) {
            const manualSec = document.getElementById('section-manual');
            const otomatisSec = document.getElementById('section-otomatis');
            const wrapperManual = document.getElementById('wrapper-jenis-manual');
            const wrapperOtomatis = document.getElementById('wrapper-jenis-otomatis');

            if (mode === 'manual') {
                manualSec.style.display = 'block';
                otomatisSec.style.display = 'none';
                wrapperManual.style.display = 'block';
                wrapperOtomatis.style.display = 'none';
            } else {
                manualSec.style.display = 'none';
                otomatisSec.style.display = 'block';
                wrapperManual.style.display = 'none';
                wrapperOtomatis.style.display = 'block';
            }
        }

        function switchOtomatisSub(val) {
            const subGiCurug = document.getElementById('sub-section-gi-curug');
            const subPindahLineJtlKsb = document.getElementById('sub-section-pindah-line-jtl-ksb');
            const subPindahLineKsbJtl = document.getElementById('sub-section-pindah-line-ksb-jtl');
            const subMiniHydro = document.getElementById('sub-section-mini-hydro');

            subGiCurug.style.display = 'none';
            subPindahLineJtlKsb.style.display = 'none';
            subPindahLineKsbJtl.style.display = 'none';
            subMiniHydro.style.display = 'none';

            if (val.includes('GARDU INDUK 70')) {
                subGiCurug.style.display = 'block';
            } else if (val.includes('JATILUHUR KE KOSAMBI')) {
                subPindahLineJtlKsb.style.display = 'block';
            } else if (val.includes('KOSAMBI KE JATILUHUR')) {
                subPindahLineKsbJtl.style.display = 'block';
            } else if (val.includes('MINI HYDRO')) {
                subMiniHydro.style.display = 'block';
            }
        }

        function updatePreview(val) {
            if(val) {
                const formatted = val.replace('T', ' Pukul ');
                document.getElementById('preview-waktu').innerText = 'Waktu terpilih: ' + formatted + ' WIB';
            } else {
                document.getElementById('preview-waktu').innerText = '';
            }
        }

        function tambahBaris() {
            const container = document.getElementById('penanganan-container');
            const rows = container.getElementsByClassName('penanganan-row');
            const newIndex = rows.length + 1;

            const newRow = document.createElement('div');
            newRow.className = 'row g-2 mb-2 penanganan-row';
            newRow.innerHTML = `
                <div class="col-md-1">
                    <input type="text" class="form-control text-center nomor-urut bg-white" value="${newIndex}" readonly>
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
            `;
            container.appendChild(newRow);
        }

        function hapusBaris(btn) {
            const row = btn.closest('.penanganan-row');
            row.remove();
            perbaruiNomorUrut();
        }

        function perbaruiNomorUrut() {
            const rows = document.getElementsByClassName('penanganan-row');
            for (let i = 0; i < rows.length; i++) {
                rows[i].getElementsByClassName('nomor-urut')[0].value = i + 1;
            }
        }
    </script>
</body>
</html>
"""

# HTML template terpisah khusus untuk halaman antarmuka Asisten AI Q&A
AI_CHAT_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asisten AI Q&A - Sistem Manajemen PLTA Curug</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, rgba(7, 15, 30, 0.85), rgba(15, 23, 42, 0.9)), url('/static/CURUGTEMPODULU.jpg') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: #1e293b;
            padding: 2rem 0;
        }
        .chat-wrapper { max-width: 950px; margin: 0 auto; }
        .chat-card { border-radius: 20px; background: rgba(255, 255, 255, 0.97); backdrop-filter: blur(16px); box-shadow: 0 20px 40px rgba(0,0,0,0.25); border: 1px solid rgba(255, 255, 255, 0.5); overflow: hidden; }
        .chat-header { background: linear-gradient(135deg, #0f172a, #1e293b); padding: 1.5rem 2rem; color: white; }
        .chat-box { height: 500px; overflow-y: auto; padding: 1.75rem; background: #f8fafc; display: flex; flex-direction: column; gap: 1rem; }
        .message { display: flex; gap: 12px; max-width: 85%; animation: fadeIn 0.3s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        .message.user { margin-left: auto; flex-direction: row-reverse; }
        .message.ai { margin-right: auto; }
        .avatar { width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.95rem; flex-shrink: 0; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .user .avatar { background: #2563eb; color: white; }
        .ai .avatar { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; }
        .bubble { padding: 0.9rem 1.25rem; border-radius: 16px; font-size: 0.95rem; line-height: 1.6; word-break: break-word; white-space: pre-wrap; }
        .user .bubble { background-color: #2563eb; color: white; border-bottom-right-radius: 4px; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }
        .ai .bubble { background-color: #ffffff; color: #1e293b; border-bottom-left-radius: 4px; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
        .typing-dots span { height: 8px; width: 8px; float: left; margin: 0 2px; background-color: #94a3b8; border-radius: 50%; display: inline-block; animation: bounce 1.3s infinite ease-in-out; }
        .typing-dots span:nth-child(2) { animation-delay: -1.1s; }
        .typing-dots span:nth-child(3) { animation-delay: -0.9s; }
        @keyframes bounce { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-6px); } }
        /* Tambahan untuk merapikan teks dan poin jawaban AI */
    .chat-message-content {
        line-height: 1.6;
        font-size: 14px;
    }
    .chat-message-content p {
        margin-bottom: 10px;
    }
    .chat-message-content ul, 
    .chat-message-content ol {
        margin-top: 5px;
        margin-bottom: 10px;
        padding-left: 20px;
    }
    .chat-message-content li {
        margin-bottom: 6px;
    }
</style>
    </style>
</head>
<body>
    <div class="container chat-wrapper">
        <div class="chat-card">
            <div class="chat-header d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center gap-3">
                    <div style="background: rgba(255,255,255,0.15); width: 45px; height: 45px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        <i class="fa-solid fa-robot text-info fs-4"></i>
                    </div>
                    <div>
                        <h3 class="mb-0 fw-bold fs-5">Asisten AI Q&A Operasional</h3>
                        <p class="mb-0 text-white-50 small">Didukung oleh Google AI (Gemini)</p>
                    </div>
                </div>
                <a href="/" class="btn btn-outline-light btn-sm px-3 rounded-pill fw-semibold">
                    <i class="fa-solid fa-arrow-left me-1"></i> Kembali
                </a>
            </div>
            
            <div class="chat-box" id="chatBox">
                <div class="message ai">
                    <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                    <div class="bubble">Halo! Saya Asisten AI untuk Sistem Manajemen PLTA Curug & PJT II. Silakan tanyakan hal seputar prosedur penanganan gangguan, operasional gardu induk, atau informasi SOP terkait.</div>
                </div>
            </div>
            
            <div class="p-3 p-md-4 bg-white border-top">
                <form id="chatForm" class="d-flex gap-2">
                    <input type="text" id="userInput" class="form-control form-control-lg fs-6" placeholder="Ketik pertanyaan atau konsultasi SOP di sini..." autocomplete="off" required>
                    <button type="submit" class="btn btn-primary px-4 fw-semibold" id="sendBtn" style="border-radius: 12px;">
                        <i class="fa-solid fa-paper-plane me-1"></i> Kirim
                    </button>
                </form>
            </div>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chatBox');
        const chatForm = document.getElementById('chatForm');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const question = userInput.value.trim();
            if (!question) return;

            appendMessage(question, 'user');
            userInput.value = '';
            userInput.disabled = true;
            sendBtn.disabled = true;

            const loadingId = appendTypingIndicator();

            try {
                const response = await fetch('/api/ask-ai', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });

                const data = await response.json();
                removeElement(loadingId);

                if (response.ok && data.success !== false && data.answer) {
                    appendMessage(data.answer, 'ai');
                } else {
                    appendMessage('Maaf: ' + (data.error || 'Gagal merespons'), 'ai');
                }
            } catch (error) {
                removeElement(loadingId);
                appendMessage('Terjadi kesalahan koneksi ke server.', 'ai');
            } finally {
                userInput.disabled = false;
                sendBtn.disabled = false;
                userInput.focus();
            }
        });

        function appendMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const avatarDiv = document.createElement('div');
            avatarDiv.className = 'avatar';
            avatarDiv.innerHTML = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
            
            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'bubble';
            bubbleDiv.textContent = text;
            
            messageDiv.appendChild(avatarDiv);
            messageDiv.appendChild(bubbleDiv);
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function appendTypingIndicator() {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ai';
            const uniqueId = 'typing-' + Date.now();
            messageDiv.id = uniqueId;
            
            const avatarDiv = document.createElement('div');
            avatarDiv.className = 'avatar';
            avatarDiv.innerHTML = '<i class="fa-solid fa-robot"></i>';
            
            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'bubble';
            bubbleDiv.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
            
            messageDiv.appendChild(avatarDiv);
            messageDiv.appendChild(bubbleDiv);
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            
            return uniqueId;
        }

        function removeElement(id) {
            const el = document.getElementById(id);
            if (el) el.remove();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    # Mengambil daftar file PDF tersimpan di folder static untuk riwayat
    pdf_files = []
    if os.path.exists(PDF_FOLDER):
        for f in os.listdir(PDF_FOLDER):
            if f.endswith(".pdf"):
                file_path = os.path.join(PDF_FOLDER, f)
                mod_time = os.path.getmtime(file_path)
                date_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                pdf_files.append({"name": f, "date": date_str})
    
    # Urutkan berdasarkan waktu terbaru
    pdf_files = sorted(pdf_files, key=lambda x: x['date'], reverse=True)
    return render_template_string(HTML_TEMPLATE, pdf_files=pdf_files, history_laporan_baru=HISTORY_LAPORAN_DB)

@app.route("/ai-chat", methods=["GET"])
def ai_chat_page():
    """Halaman antarmuka Asisten AI Q&A."""
    return render_template_string(AI_CHAT_TEMPLATE)

import time  # Pastikan modul time sudah diimpor di bagian atas app.py jika belum

import time  # Pastikan modul time ada di bagian paling atas file app.py

@app.route("/api/ask-ai", methods=["POST"])
def ask_ai():
    data = request.get_json(silent=True) or {}
    user_question = str(data.get("question", "")).strip()

    if not user_question:
        return jsonify({"success": False, "error": "Pertanyaan tidak boleh kosong."}), 400

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return jsonify({"success": False, "error": "API Gemini belum dikonfigurasi."}), 500

        client = genai.Client(api_key=api_key)
        
       formatted_prompt = (
            "Anda adalah Asisten AI profesional untuk Sistem Manajemen PLTA Curug & PJT II. "
            "Berikan jawaban secara langsung, to the point, dan terstruktur rapi menggunakan poin-poin. "
            "JANGAN gunakan kalimat basa-basi pembuka seperti 'Selamat siang', 'Selamat malam', atau 'Terima kasih atas pertanyaan Anda'. "
            "Langsung masuk ke inti jawaban.\n\n"
            f"Pertanyaan: {user_question}"
        )

        # Menggunakan model produksi terbaru yang aktif di akun Google AI Studio Anda
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=formatted_prompt,
        )

        answer = getattr(response, "text", None)
        if not answer:
            return jsonify({"success": False, "error": "AI tidak mengembalikan jawaban."}), 502

        return jsonify({"success": True, "answer": answer.strip()})
        
    except Exception as e:
        print(f"[AI ERROR] {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/generate-laporan-baru", methods=["POST"])
def generate_laporan_baru():
    jenis = request.form.get("baru_jenis_gangguan")
    waktu = request.form.get("baru_waktu")
    tanggal = request.form.get("baru_tanggal_lengkap")
    kronologi = request.form.get("baru_kronologi")
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_name = f"Laporan_Gangguan_Baru_{timestamp_str}.pdf"
    pdf_path = os.path.join(PDF_FOLDER, pdf_name)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=14,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#0f172a')
    )
    
    story.append(Paragraph("<b>PERUM JASA TIRTA II</b>", title_style))
    story.append(Paragraph("<b>LAPORAN GANGGUAN OPERASIONAL & KRONOLOGI</b>", title_style))
    story.append(Spacer(1, 15))
    
    data_info = [
        [Paragraph("<b>Jenis Gangguan:</b>", styles['Normal']), Paragraph(jenis, styles['Normal'])],
        [Paragraph("<b>Tanggal Kejadian:</b>", styles['Normal']), Paragraph(tanggal, styles['Normal'])],
        [Paragraph("<b>Waktu (Jam):</b>", styles['Normal']), Paragraph(waktu, styles['Normal'])],
    ]
    t_info = Table(data_info, colWidths=[120, 420])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Kronologi Kejadian:</b>", styles['Heading3']))
    story.append(Spacer(1, 5))
    story.append(Paragraph(kronologi.replace('\n', '<br/>'), styles['Normal']))
    
    doc.build(story)
    
    HISTORY_LAPORAN_DB.append({
        "jenis": jenis,
        "tanggal": tanggal,
        "waktu": waktu,
        "kronologi": kronologi,
        "pdf_name": pdf_name
    })
    
    return redirect(url_for('index'))

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(PDF_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
