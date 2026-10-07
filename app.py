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
    <title>Aplikasi Laporan Normalisasi Gangguan</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.75)), url('/static/CURUGTEMPODULU.jpg') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .card {
            border: none;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            background-color: rgba(255, 255, 255, 0.95);
        }
        .card-header {
            border-top-left-radius: 12px !important;
            border-top-right-radius: 12px !important;
            background: linear-gradient(135deg, #0d6efd, #0b5ed7) !important;
            padding: 1.25rem;
        }
        .form-control, .form-select {
            border-radius: 8px;
            padding: 0.6rem 0.75rem;
        }
        .form-control:focus, .form-select:focus {
            box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
        }
        .btn {
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container mt-5 mb-5">
        <div class="row justify-content-center">
            <div class="col-md-11">
                <div class="card shadow-lg">
                    <div class="card-header text-white text-center">
                        <h3 class="mb-0 fw-bold">FORM LAPORAN NORMALISASI GANGGUAN</h3>
                        <p class="mb-0 text-white-50 small mt-1">Sistem Pencatatan & Pelaporan Operasional Gardu Induk / Unit Terkait</p>
                    </div>
                    <div class="card-body p-4">
                        <form method="POST" action="/generate">
                            <div class="mb-3">
                                <label for="kategori" class="form-label fw-bold text-secondary">Pilih Kategori / Lokasi:</label>
                                <select class="form-select" id="kategori" name="kategori" required>
                                    <option value="" disabled selected>-- Pilih Jenis Normalisasi --</option>
                                    <option value="Gardu Induk Curug">1. Gardu Induk Curug</option>
                                    <option value="Mini Hydro">2. Mini Hydro</option>
                                    <option value="Pompa Elektrik Tarum Timur">3. Pompa Elektrik Tarum Timur</option>
                                </select>
                            </div>

                            <!-- PILIHAN MODE PENCATATAN -->
                            <div class="mb-3 p-3 bg-light border rounded-3">
                                <label class="form-label fw-bold text-primary mb-2">Pilih Mode Pencatatan Penanganan:</label>
                                <div class="btn-group w-100" role="group">
                                    <input type="radio" class="btn-check" name="mode_pencatatan" id="modeManual" value="manual" autocomplete="off" checked onclick="switchMode('manual')">
                                    <label class="btn btn-outline-primary" for="modeManual">Mode Manual</label>

                                    <input type="radio" class="btn-check" name="mode_pencatatan" id="modeOtomatis" value="otomatis" autocomplete="off" onclick="switchMode('otomatis')">
                                    <label class="btn btn-outline-success" for="modeOtomatis">Mode Otomatis</label>
                                </div>
                            </div>

                            <!-- INPUT / PILIHAN JENIS GANGGUAN BERDASARKAN MODE -->
                            <div class="mb-3" id="wrapper-jenis-manual">
                                <label for="jenis_gangguan_manual" class="form-label fw-bold text-secondary">Jenis Gangguan</label>
                                <input type="text" class="form-control" id="jenis_gangguan_manual" name="jenis_gangguan_manual" placeholder="Contoh: Gangguan Trafo / Trip PMT">
                            </div>

                            <div class="mb-3" id="wrapper-jenis-otomatis" style="display: none;">
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
                                            <button type="button" class="btn btn-danger w-100" onclick="hapusBaris(this)">X</button>
                                        </div>
                                    </div>
                                </div>
                                <button type="button" class="btn btn-outline-secondary btn-sm mb-4 px-3" onclick="tambahBaris()">+ Tambah Baris</button>
                            </div>

                            <!-- KONTAINER MODE OTOMATIS -->
                            <div id="section-otomatis" style="display: none;" class="mb-4">
                                
                                <!-- SUB SECTION 1: PENGAMANAN GANGGUAN / TRIP -->
                                <div id="sub-section-gi-curug" style="display: none;">
                                    <div class="alert alert-warning border-0 shadow-sm">
                                        <b>CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)</b><br>
                                        <small>Centang item yang dikerjakan, lalu sesuaikan Keadaan/Posisi serta Pukul (Jam).</small>
                                    </div>

                                    <!-- Bagian A -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded">A. RUANG PANEL 6,3 KV</h6>
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

                                    <!-- Bagian B -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded mt-3">B. RUANG PANEL 20 KV BUILDING</h6>
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

                                    <!-- Bagian C -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded mt-3">C. RUANG PANEL 6 KV</h6>
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

                                    <!-- Bagian D -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded mt-3">D. CB PANEL DISTRIBUSI 380 V AC TARUM BARAT</h6>
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

                                <!-- SUB SECTION 2: PINDAH LINE JATILUHUR -> KOSAMBI -->
                                <div id="sub-section-pindah-line" style="display: none;">
                                    <div class="alert alert-info border-0 shadow-sm">
                                        <b>CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV JATILUHUR KE PENGHANTAR 70 KV KOSAMBI (PLN)</b><br>
                                        <small>I. Koordinasi dengan Kontrol Building Jatiluhur.<br>II. Pelaksanaan Manuver (Pemindahan Line).</small>
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
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded mt-3">{{ p_title }}</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="35%">Uraian</th>
                                                    <th width="25%">Keadaan / Posisi</th>
                                                    <th width="15%">Pukul (Jam)</th>
                                                    <th width="15%">Keterangan</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% for item_id, item_desc, item_default, item_ket in p_items %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_{{ item_id }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>
                                                        {{ item_desc }}
                                                        {% if 'Posisi TC' in item_desc %}
                                                        <br><input type="text" class="form-control form-control-sm mt-1" name="tc_val_{{ item_id }}" placeholder="Ketik nilai TC disini...">
                                                        {% endif %}
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

                                <!-- SUB SECTION 3: PINDAH LINE KOSAMBI -> JATILUHUR -->
                                <div id="sub-section-pindah-line-kj" style="display: none;">
                                    <div class="alert alert-success border-0 shadow-sm">
                                        <b>CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV KOSAMBI (PLN) KE PENGHANTAR 70 KV JATILUHUR</b><br>
                                        <small>I. Koordinasi dengan Kontrol Building Jatiluhur.<br>II. Pelaksanaan Manuver (Pemindahan Line).</small>
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
                                            ('qc2', 'PMS / DS Line 70 KV Kosambi Bay', 'Tdk. dikeluarkan', 'Untuk monitoring'),
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
                                            ('qe3_custom', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC', 'Dimasukan', 'Posisi TC harus sama'),
                                            ('qe4_custom', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC', 'Dimasukan', 'Posisi TC harus sama')
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
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded mt-3">{{ p_title }}</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="35%">Uraian</th>
                                                    <th width="25%">Keadaan / Posisi</th>
                                                    <th width="15%">Pukul (Jam)</th>
                                                    <th width="15%">Keterangan</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% for item_id, item_desc, item_default, item_ket in p_items %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_{{ item_id }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>
                                                        {{ item_desc }}
                                                        {% if 'Posisi TC' in item_desc %}
                                                        <br><input type="text" class="form-control form-control-sm mt-1" name="tc_val_{{ item_id }}" placeholder="Ketik nilai TC disini...">
                                                        {% endif %}
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

                                <!-- SUB SECTION 4: CHECK LIST OPERASI PLTA MINI HYDRO CURUG -->
                                <div id="sub-section-plta-curug" style="display: none;">
                                    <div class="alert alert-primary border-0 shadow-sm">
                                        <b>CHECK LIST OPERASI PLTA MINI HYDRO CURUG</b><br>
                                        <small>Formulir No: F-20/DPL/1K.10-01 (Lampiran : 2)</small>
                                    </div>

                                    <div class="row g-3 mb-3 bg-white p-3 border rounded shadow-sm">
                                        <div class="col-md-6">
                                            <label class="form-label fw-bold">UNIT No. :</label>
                                            <input type="text" class="form-control" name="plta_unit_no" placeholder="Contoh: Unit 1">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label fw-bold">Jam Kerja Unit ( TM ) :</label>
                                            <input type="text" class="form-control" name="plta_jam_kerja" placeholder="Contoh: 120 Jam">
                                        </div>
                                    </div>

                                    <div class="alert alert-light border p-3 small mb-3">
                                        <b>I. Persiapan</b><br>
                                        1. Koordinasi debit air / Tinggi Muka air dengan Operator Bendung Curug Divisi II<br>
                                        2. Koordinasi dengan Operator Control Building di Jatiluhur<br><br>
                                        <b>II. Pelaksanaan Pengoperasian</b><br>
                                        <b>III. Pengecekan Air Baku I & II Tekanan 3 bar / lebih</b><br>
                                        <b>IV. Pengecekan Sudu - Sudu Tekanan 60 bar</b><br>
                                        <b>V. Pengecekan Down Strem 120 bar</b>
                                    </div>

                                    <!-- Bagian A: Ruang Panel Control Room -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded">A. RUANG PANEL CONTROL ROOM</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="35%">Uraian</th>
                                                    <th width="20%">Posisi</th>
                                                    <th width="15%">Paraf</th>
                                                    <th width="20%">Keterangan</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% set plta_a = [
                                                    ("Pada jendela alarm tidak ada indikasi gangguan", "-", "TMA Udik 26-36 mohon diperhatikan apabila Beban sudah turun dan air Udik kecil, maka Mini Hydro Stop (utamakan air Tr. TT & Tr Barat)"),
                                                    ("Tinggi Muka Air : Tinggi Air Udik, Tinggi Air Hilir, Posisi saringan sampah unit .....", "-", "-"),
                                                    ("Kriteria berhenti pada posisi stabil / indikator tombol stop", "Menyala", "-"),
                                                    ("Posisi Pintu Pembuangan \" Tutup \"", "Menyala", "-"),
                                                    ("Indikasi DS Phase Cubicle / .... GTA 030 JD", "Masuk", "-"),
                                                    ("Indikasi Earthing Switch / .... GTA 031 JS", "Keluar", "-"),
                                                    ("Indikasi CB 20 KV / ..... LGB 001 JD", "Keluar", "TPL Menyala"),
                                                    ("Indikasi Earthing Switch / .... LGB 031 JS", "Keluar", "-"),
                                                    ("Indikasi Unit Siap Jalan", "Menyala", "-")
                                                ] %}
                                                {% for desc, default_pos, default_ket in plta_a %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_plta_a{{ loop.index }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>{{ desc }}</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_plta_a{{ loop.index }}" value="{{ default_pos }}"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_plta_a{{ loop.index }}"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_plta_a{{ loop.index }}" value="{{ default_ket }}"></td>
                                                </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- Bagian B: Cara Pengoperasian -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded mt-3">B. CARA PENGOPERASIAAN</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="35%">Uraian</th>
                                                    <th width="20%">Posisi</th>
                                                    <th width="15%">Paraf</th>
                                                    <th width="20%">Keterangan</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% set plta_b = [
                                                    ("Sistim Pengatur Unit", "Lokal", "-"),
                                                    ("Sistim Komando Unit .....", "Manual / Auto", "-"),
                                                    ("Sinkronisasi (Jika dipilih cara manual, hubungkan alat sinkronisasi portible)", "-", "-"),
                                                    ("Duga Muka Air / Kontrol water level", "ON / OFF", "-"),
                                                    ("Pengoperasian Unit (Manual / Auto)", "Berkedip", "Tunggu sampai tombol tdk berkedip"),
                                                    ("Sinkronisasi (Auto / Manual)", "TPL Berkedip", "Putar ke posisi ON")
                                                ] %}
                                                {% for desc, default_pos, default_ket in plta_b %}
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_plta_b{{ loop.index }}" value="on" checked></td>
                                                    <td class="text-center">{{ loop.index }}</td>
                                                    <td>{{ desc }}</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_plta_b{{ loop.index }}" value="{{ default_pos }}"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_plta_b{{ loop.index }}"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_plta_b{{ loop.index }}" value="{{ default_ket }}"></td>
                                                </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    </div>

                                    <!-- Bagian C & D -->
                                    <h6 class="fw-bold bg-secondary text-white p-2 rounded mt-3">C. PENGATURAN BEBAN & D. PENCATATAN RUTIN</h6>
                                    <div class="table-responsive">
                                        <table class="table table-bordered table-sm bg-white align-middle shadow-sm">
                                            <thead class="table-light text-center">
                                                <tr>
                                                    <th width="5%">Pilih</th>
                                                    <th width="5%">No</th>
                                                    <th width="35%">Uraian</th>
                                                    <th width="20%">Posisi</th>
                                                    <th width="15%">Paraf</th>
                                                    <th width="20%">Keterangan</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_plta_c1" value="on" checked></td>
                                                    <td class="text-center">C</td>
                                                    <td>Tekan Tombol Pengatur Beban / Frekwensi ( naik / turun ), hingga :</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_plta_c1" value="........ MW"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_plta_c1"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_plta_c1" value="Secara Bertahap"></td>
                                                </tr>
                                                <tr>
                                                    <td class="text-center"><input class="form-check-input" type="checkbox" name="chk_plta_d1" value="on" checked></td>
                                                    <td class="text-center">D</td>
                                                    <td>Selanjutnya pencatatan rutin dengan blangko laporan harian</td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="pos_plta_d1" value="-"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="paraf_plta_d1"></td>
                                                    <td><input type="text" class="form-control form-control-sm text-center" name="ket_plta_d1" value="-"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>

                            </div>

                            <hr class="my-4">
                            <!-- FITUR PEMBUAT LAPORAN -->
                            <div class="card p-3 mb-4 bg-light border-0 shadow-sm">
                                <h6 class="fw-bold text-primary mb-3">Informasi Pembuat Laporan</h6>
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

                            <button type="submit" class="btn btn-primary w-100 py-2 shadow-sm fs-5">Buat Laporan PDF</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
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
                               '<div class="col-md-1"><button type="button" class="btn btn-danger w-100" onclick="hapusBaris(this)">X</button></div>';
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

        window.onload = function() {
            switchMode('manual');
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
    <style>
        body {
            background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.75)), url('/static/CURUGTEMPODULU.jpg') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .card {
            border: none;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            background-color: rgba(255, 255, 255, 0.95);
        }
        .card-header {
            border-top-left-radius: 12px !important;
            border-top-right-radius: 12px !important;
            background: linear-gradient(135deg, #198754, #157347) !important;
            padding: 1.25rem;
        }
        .btn {
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow-lg text-center">
                    <div class="card-header text-white">
                        <h4 class="mb-0 fw-bold">Laporan Berhasil Dibuat!</h4>
                    </div>
                    <div class="card-body p-4">
                        <p class="text-muted mb-4">File PDF laporan gangguan Anda sudah siap diunduh atau dikirimkan langsung ke Grup WhatsApp.</p>
                        <a href="/download/{{ filename }}" class="btn btn-primary w-100 mb-3 py-2 shadow-sm" target="_blank">Unduh File PDF</a>
                        <a href="https://api.whatsapp.com/send?text={{ wa_message }}" class="btn btn-success w-100 mb-3 py-2 shadow-sm" target="_blank">Kirim ke Grup WhatsApp</a>
                        <a href="/" class="btn btn-outline-secondary w-100 py-2">Kembali ke Form</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

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
        
        file_date_str = dt.strftime('%d-%m-%Y')
    except:
        waktu = waktu_raw
        default_jam = "00:00"
        file_date_str = datetime.now().strftime('%d-%m-%Y')

    clean_jenis = re.sub(r'[^a-zA-Z0-9]', '_', jenis_gangguan)
    clean_jenis = re.sub(r'_+', '_', clean_jenis).strip('_')
    if len(clean_jenis) > 40:
        clean_jenis = clean_jenis[:40]
    
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
            Paragraph("<b>POSISI</b>", cell_center),
            Paragraph("<b>PARAF</b>", cell_center),
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
                ("A. RUANG PANEL CONTROL ROOM", [
                    ('chk_plta_a1', 'Pada jendela alarm tidak ada indikasi gangguan', '-', 'TMA Udik 26-36 mohon diperhatikan apabila Beban sudah turun dan air Udik kecil, maka Mini Hydro Stop (utamakan air Tr. TT & Tr Barat)'),
                    ('chk_plta_a2', 'Tinggi Muka Air : Tinggi Air Udik, Tinggi Air Hilir, Posisi saringan sampah unit .....', '-', '-'),
                    ('chk_plta_a3', 'Kriteria berhenti pada posisi stabil / indikator tombol stop', 'Menyala', '-'),
                    ('chk_plta_a4', 'Posisi Pintu Pembuangan " Tutup "', 'Menyala', '-'),
                    ('chk_plta_a5', 'Indikasi DS Phase Cubicle / .... GTA 030 JD', 'Masuk', '-'),
                    ('chk_plta_a6', 'Indikasi Earthing Switch / .... GTA 031 JS', 'Keluar', '-'),
                    ('chk_plta_a7', 'Indikasi CB 20 KV / ..... LGB 001 JD', 'Keluar', 'TPL Menyala'),
                    ('chk_plta_a8', 'Indikasi Earthing Switch / .... LGB 031 JS', 'Keluar', '-'),
                    ('chk_plta_a9', 'Indikasi Unit Siap Jalan', 'Menyala', '-')
                ]),
                ("B. CARA PENGOPERASIAAN", [
                    ('chk_plta_b1', 'Sistim Pengatur Unit', 'Lokal', '-'),
                    ('chk_plta_b2', 'Sistim Komando Unit .....', 'Manual / Auto', '-'),
                    ('chk_plta_b3', 'Sinkronisasi (Jika dipilih cara manual, hubungkan alat sinkronisasi portible)', '-', '-'),
                    ('chk_plta_b4', 'Duga Muka Air / Kontrol water level', 'ON / OFF', '-'),
                    ('chk_plta_b5', 'Pengoperasian Unit (Manual / Auto)', 'Berkedip', 'Tunggu sampai tombol tdk berkedip'),
                    ('chk_plta_b6', 'Sinkronisasi (Auto / Manual)', 'TPL Berkedip', 'Putar ke posisi ON')
                ]),
                ("C. PENGATURAN BEBAN & D. PENCATATAN RUTIN", [
                    ('chk_plta_c1', 'Tekan Tombol Pengatur Beban / Frekwensi ( naik / turun ), hingga : ...... MW', '........ MW', 'Secara Bertahap'),
                    ('chk_plta_d1', 'Selanjutnya pencatatan rutin dengan blangko laporan harian', '-', '-')
                ])
            ]

            global_idx = 1
            for sec_title, items in plta_sections:
                table_data.append([Paragraph(sec_title, sec_style), "", "", "", ""])
                for item_id, desc, default_pos, default_ket in items:
                    chk_val = request.form.get(item_id)
                    if chk_val == "on":
                        pos = request.form.get(f"pos_{item_id}") or default_pos
                        paraf = request.form.get(f"paraf_{item_id}") or "-"
                        ket = request.form.get(f"ket_{item_id}") or default_ket

                        table_data.append([
                            Paragraph(str(global_idx) if not sec_title.startswith("C.") else ("C" if "Tekan" in desc else "D"), cell_center),
                            Paragraph(desc, cell_style),
                            Paragraph(pos, cell_center),
                            Paragraph(paraf, cell_center),
                            Paragraph(ket, cell_center)
                        ])
                        wa_details.append(f"{global_idx}. {desc} - Posisi: {pos} (Ket: {ket})")
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
            global_idx = 1
            for sec_title, items in sections:
                table_data.append([Paragraph(sec_title, sec_style), "", "", "", ""])
                for item_id, desc in items:
                    chk_val = request.form.get(f"chk_{item_id}")
                    if chk_val == "on" or True:
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
                        wa_details.append(f"{global_idx}. [{pukul}] {final_desc} - {keadaan} ({ket})")
                        global_idx += 1
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
            global_idx = 1
            for sec_title, items in sections:
                table_data.append([Paragraph(sec_title, sec_style), "", "", "", ""])
                for item_id, desc in items:
                    chk_val = request.form.get(f"chk_{item_id}")
                    if chk_val == "on" or True:
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
                        wa_details.append(f"{global_idx}. [{pukul}] {final_desc} - {keadaan} ({ket})")
                        global_idx += 1
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
            global_idx = 1
            for sec_title, items in sections:
                table_data.append([Paragraph(sec_title, sec_style), "", "", "", ""])
                for item_id, desc in items:
                    chk_val = request.form.get(f"chk_{item_id}") or request.form.get(item_id)
                    if chk_val == "on":
                        pukul = request.form.get(f"jam_{item_id}") or default_jam
                        keadaan = request.form.get(f"pos_{item_id}") or "-"
                        ket = request.form.get(f"ket_{item_id}") or "-"

                        table_data.append([
                            Paragraph(str(global_idx), cell_center),
                            Paragraph(desc, cell_style),
                            Paragraph(pukul, cell_center),
                            Paragraph(keadaan, cell_center),
                            Paragraph(ket, cell_center)
                        ])
                        wa_details.append(f"{global_idx}. [{pukul}] {desc} - {keadaan} ({ket})")
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

    t = Table(table_data, colWidths=[25, 237, 85, 125, 80])

    table_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
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
            table_styles.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#e9ecef')))
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
