from flask import Flask, render_template_string, request, send_file, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
import re
import urllib.parse
import traceback
from datetime import datetime

app = Flask(__name__)

PDF_FOLDER = "static"
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

# (Gunakan HTML_TEMPLATE dan RESULT_TEMPLATE yang sama seperti sebelumnya)
# ...

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        kategori = request.form.get("kategori", "-")
        mode = request.form.get("mode_pencatatan", "manual")
        
        if mode == "manual":
            jenis_gangguan = request.form.get("jenis_gangguan_manual", "-")
        else:
            jenis_gangguan = request.form.get("jenis_gangguan_otomatis", "-")

        waktu_raw = request.form.get("waktu", "")
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
        except Exception:
            waktu = waktu_raw if waktu_raw else "-"
            default_jam = "00:00"
            file_date_str = datetime.now().strftime('%d-%m-%Y')

        clean_jenis = re.sub(r'[^a-zA-Z0-9]', '_', jenis_gangguan)
        clean_jenis = re.sub(r'_+', '_', clean_jenis).strip('_')
        if len(clean_jenis) > 40:
            clean_jenis = clean_jenis[:40]
        
        filename = f"laporan_{clean_jenis}_{file_date_str}.pdf"

        styles = getSampleStyleSheet()
        cell_style = ParagraphStyle("CellStyle", parent=styles["Normal"], fontSize=8, leading=10)
        cell_center = ParagraphStyle("CellCenter", parent=cell_style, alignment=1)
        sec_style = ParagraphStyle("SecStyle", parent=styles["Normal"], fontSize=8, leading=10, fontName="Helvetica-Bold")

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
                # Logika PLTA Curug
                plta_sections = [
                    ("A. RUANG PANEL CONTROL ROOM", [
                        ('chk_plta_a1', 'Pada jendela alarm tidak ada indikasi gangguan', '-', 'TMA Udik 26-36 mohon diperhatikan apabila Beban sudah turun dan air Udik kecil, maka Mini Hydro Stop...'),
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
                            pos = request.form.get(f"pos_{item_id}", default_pos)
                            paraf = request.form.get(f"paraf_{item_id}", "-")
                            ket = request.form.get(f"ket_{item_id}", default_ket)

                            table_data.append([
                                Paragraph(str(global_idx) if not sec_title.startswith("C.") else ("C" if "Tekan" in desc else "D"), cell_center),
                                Paragraph(desc, cell_style),
                                Paragraph(pos, cell_center),
                                Paragraph(paraf, cell_center),
                                Paragraph(ket, cell_center)
                            ])
                            wa_details.append(f"{global_idx}. {desc} - Posisi: {pos} (Ket: {ket})")
                            global_idx += 1
            else:
                # Untuk checklist gardu induk / pindah line, gunakan perulangan aman
                sections = []
                if "KOSAMBI KE PENGHANTAR 70 KV JATILUHUR" in jenis_gangguan or "JATILUHUR KE PENGHANTAR 70 KV KOSAMBI" in jenis_gangguan:
                    prefix = "q" if "KOSAMBI" in jenis_gangguan and "JATILUHUR" in jenis_gangguan else "p"
                    # Format ringkas penanganan section pindah line
                    sections = [
                        ("A. RUANG PANEL 6 KV", [(f"{prefix}a1", 'PMT/CB panel Trafo 500 KVA / Trafo I'), (f"{prefix}a2", 'PMT/CB panel Trafo 500 KVA / Trafo II'), (f"{prefix}a3", 'PMT/CB panel keluaran 6 MB2'), (f"{prefix}a4", 'PMT/CB panel masukan dari Trafo II'), (f"{prefix}a5', 'PMT/CB panel masukan dari Trafo III')]),
                        ("B. RUANG PANEL 20 KV BUILDING", [(f"{prefix}b1", 'PMT/CB Masukan dari trafo I'), (f"{prefix}b2", 'PMT/CB Trafo I 20 / 70 KV 10 MVA'), (f"{prefix}b3", 'PMT/CB Trafo II 70 / 6,3 KV 5 MVA'), (f"{prefix}b4', 'PMT/CB Trafo III 70 / 6,3 KV 5 MVA')]),
                        ("C. PMT BAY", [(f"{prefix}c1", 'PMT / CB 70 KV Bay'), (f"{prefix}c2', 'PMS / DS Line 70 KV Bay'), (f"{prefix}c3", 'PMS / DS Arde Line 70 KV Bay'), (f"{prefix}c4", 'PMS / DS Rel 70 KV Bay'), (f"{prefix}c5", 'PMS / DS Arde Rel 70 KV Bay')]),
                        ("D. PMT BAY SEBERANG", [(f"{prefix}d1', 'PMS / DS Arde Line 70 KV Seberang'), (f"{prefix}d2", 'PMS / DS Line 70 KV Seberang'), (f"{prefix}d3', 'PMS / DS Arde Rel 70 KV Seberang'), (f"{prefix}d4", 'PMS / DS Rel 70 KV Seberang'), (f"{prefix}d5", 'PMT / CB 70 KV Seberang')]),
                        ("E. RUANG PANEL 20 KV BUILDING", [(f"{prefix}e1", 'PMT / CB Trafo I 20 / 70 KV 10 MVA'), (f"{prefix}e2", 'PMT / CB Masukan dari Trafo I'), (f"{prefix}e3_custom", 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC'), (f"{prefix}e4_custom', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC')]),
                        ("F. RUANG PANEL 6 KV", [(f"{prefix}f1", 'PMT / CB panel masukan dari Trafo II'), (f"{prefix}f2", 'PMT / CB panel masukan dari Trafo III'), (f"{prefix}f3", 'PMT / CB panel Trafo 500 KVA / Trafo I'), (f"{prefix}f4", 'PMT / CB panel Trafo 500 KVA / Trafo II'), (f"{prefix}f5', 'PMT / CB panel keluaran 6 MB2')])
                    ]
                else:
                    sections = [
                        ("A. RUANG PANEL 6,3 KV", [('chk_a1', 'PMT / CB Panel Trafo 500 KVA / Trafo I'), ('chk_a2', 'PMT / CB Panel Trafo 500 KVA / Trafo II'), ('chk_a3', 'PMT / CB Panel Keluaran 6 MB2')]),
                        ("B. RUANG PANEL 20 KV BUILDING", [('chk_b1', 'PMT / CB Masukan dari Trafo I'), ('chk_b2', 'PMT / CB Trafo I 20 / 70 KV 10 MVA'), ('chk_b3', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA'), ('chk_b4', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA'), ('chk_b5', 'Riset Semua Gangguan'), ('chk_b6', 'Koordinasi dengan Kontrol Building'), ('chk_b7', 'PMT / CB Jatiluhur / Kosambi'), ('chk_b8', 'PMT / CB Trafo I 20 / 70 KV 10 MVA'), ('chk_b9', 'PMT / CB Masukan dari Trafo I'), ('chk_b10', 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC'), ('chk_b11', 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC'), ('chk_b12', 'Riset Semua Gangguan')]),
                        ("C. RUANG PANEL 6 KV", [('chk_c1', 'Riset Semua Gangguan'), ('chk_c2', 'PMT / CB Panel Masukan dari Trafo II'), ('chk_c3', 'PMT / CB Panel Masukan dari Trafo III'), ('chk_c4', 'PMT / CB Panel Trafo 500 KVA / Trafo I'), ('chk_c5', 'PMT / CB Panel Trafo 500 KVA / Trafo II'), ('chk_c6', 'PMT / CB Panel Keluaran 6 MB2'), ('chk_c7', 'Riset Semua Gangguan')]),
                        ("D. CB PANEL DISTRIBUSI 380 V AC TARUM BARAT", [('chk_d1', 'CB Panel Distribusi 380 V AC Tarum Barat')])
                    ]

                global_idx = 1
                for sec_title, items in sections:
                    table_data.append([Paragraph(sec_title, sec_style), "", "", "", ""])
                    for item_id, desc in items:
                        # Cek apakah dicentang atau ambil default jika form tidak mengirimkan checkbox kosong
                        pukul = request.form.get(f"jam_{item_id}", default_jam)
                        keadaan = request.form.get(f"pos_{item_id}", "-")
                        ket = request.form.get(f"ket_{item_id}", "-")
                        
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

        filepath = os.path.join(PDF_FOLDER, filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        story = []

        title_style = ParagraphStyle("TitleStyle", parent=styles["Heading1"], alignment=1, fontSize=13, spaceAfter=10)

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

    except Exception as e:
        # Menampilkan detail error di browser agar mudah dilacak
        error_detail = traceback.format_exc()
        return f"<h3>Terjadi Kesalahan (Internal Server Error):</h3><pre>{error_detail}</pre>", 500

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(PDF_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
