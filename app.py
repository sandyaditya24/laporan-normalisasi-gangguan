from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Direktori penyimpanan file PDF hasil laporan
UPLOAD_FOLDER = 'static/reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy data sementara untuk riwayat laporan
riwayat_laporan = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form_laporan():
    return render_template('form.html')

@app.route('/history')
def history():
    return render_template('history.html', laporan=riwayat_laporan)

@app.route('/generate', methods=['POST'])
def generate_report():
    # Ambil data dari form
    lokasi = request.form.get('lokasi')
    tanggal = request.form.get('tanggal')
    petugas = request.form.get('petugas')
    mode_checklist = request.form.get('mode_checklist')
    prosedur_otomatis = request.form.get('prosedur_otomatis')
    
    # Tentukan detail checklist berdasarkan pilihan
    langkah_checklist = []
    
    if mode_checklist == 'otomatis':
        if prosedur_otomatis == '1':
            judul_prosedur = "Pengamanan gangguan/trip Gardu Induk 70 / 6,3 kV Curug"
            langkah_checklist = [
                "1. Periksa indikator relai proteksi pada panel kontrol GI.",
                "2. Laporkan status trip kepada Piknik UPK / Manajer Unit.",
                "3. Lakukan pengecekan visual pada peralatan pemutus tenaga (PMT) dan transformator.",
                "4. Catat waktu kejadian dan parameter gangguan ke dalam log sheet."
            ]
        elif prosedur_otomatis == '2':
            judul_prosedur = "Pindah line penghantar 70 kV dari Jatiluhur ke Kosambi (F-20/DPL/IK.12-01)"
            langkah_checklist = [
                "1. Pastikan komunikasi koordinasi dengan dispatch Center siap.",
                "2. Buka PMT Line Jatiluhur sesuai prosedur F-20/DPL/IK.12-01.",
                "3. Masukkan PMT Line Kosambi secara berurutan.",
                "4. Verifikasi tegangan dan sinkronisasi fasa dalam kondisi normal."
            ]
        elif prosedur_otomatis == '3':
            judul_prosedur = "Pindah line penghantar 70 kV dari Kosambi ke Jatiluhur (F-20/DPL/IK.12-02)"
            langkah_checklist = [
                "1. Koordinasi dengan operator dispatch terkait perpindahan beban.",
                "2. Buka PMT Line Kosambi sesuai SOP F-20/DPL/IK.12-02.",
                "3. Masukkan PMT Line Jatiluhur secara hati-hati.",
                "4. Pastikan parameter arus dan tegangan stabil."
            ]
        elif prosedur_otomatis == '4':
            judul_prosedur = "Operasi PLTA Mini Hydro Curug (F-20/DPL/IK.10-01)"
            langkah_checklist = [
                "1. Lakukan pengecekan level air forebay dan saluran pelimpah.",
                "2. Pastikan sistem pelumasan dan governor turbin berfungsi.",
                "3. Jalankan prosedur Start Unit PLTA Mini Hydro sesuai SOP F-20/DPL/IK.10-01.",
                "4. Monitor beban generator hingga mencapai kapasitas optimal."
            ]
        else:
            judul_prosedur = "Prosedur Otomatis Standar"
            langkah_checklist = ["- Tidak ada prosedur spesifik yang dipilih."]
    else:
        judul_prosedur = "Mode Manual / Penanganan Khusus"
        # Ambil input manual dari form jika ada
        keterangan_manual = request.form.get('keterangan_manual', 'Laporan pemeliharaan rutin.')
        langkah_checklist = [f"- {keterangan_manual}"]

    # Nama file PDF yang akan digenerate
    filename = f"Laporan_{lokasi.replace(' ', '_')}_{tanggal}.pdf"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Proses pembuatan dokumen PDF menggunakan ReportLab
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = height, width # Mengatur orientasi jika diperlukan
    
    # Header Dokumen
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "PERUM JASA TIRTA II - PLTA CURUG")
    c.setFont("Helvetica", 10)
    c.drawString(50, 735, f"Sistem Manajemen Laporan & Checklist Unit: {lokasi}")
    
    # Informasi Umum
    c.drawString(50, 705, f"Tanggal Pelaksanaan : {tanggal}")
    c.drawString(50, 690, f"Petugas Pelapor    : {petugas}")
    c.drawString(50, 675, f"Jenis Mode / SOP   : {judul_prosedur}")
    
    # Garis Pembatas
    c.line(50, 660, 560, 660)
    
    # Isi Checklist / Langkah-langkah
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 635, "Rincian Prosedur / Langkah Kerja:")
    
    c.setFont("Helvetica", 10)
    y_pos = 615
    for langkah in langkah_checklist:
        c.drawString(60, y_pos, langkah)
        y_pos -= 20
        
    # Catatan Kaki / Tanda Tangan
    c.drawString(50, y_pos - 40, "Mengetahui,")
    c.drawString(50, y_pos - 95, "( Pengawas / Supervisor Shift )")
    
    c.save()

    # Simpan ke riwayat lokal sementara
    riwayat_laporan.append({
        'lokasi': lokasi,
        'tanggal': tanggal,
        'petugas': petugas,
        'prosedur': judul_prosedur,
        'file': filename
    })

    return redirect(url_for('history'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
