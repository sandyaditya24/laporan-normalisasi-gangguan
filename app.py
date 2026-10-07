from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
import os
from datetime import datetime
from pegawai import pegawai_bp
from faq import faq_bp
from normalisasi import normalisasi_bp  # Mengimpor blueprint normalisasi
from google import genai  # Pustaka untuk Google Gemini AI
from pdf_helper import generate_pdf_laporan  # Mengimpor fungsi pembuat PDF terpisah

app = Flask(__name__)
app.register_blueprint(pegawai_bp)
app.register_blueprint(faq_bp)
app.register_blueprint(normalisasi_bp)  # Mendaftarkan blueprint normalisasi

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
    return render_template('index.html', pdf_files=pdf_files, history_laporan_baru=HISTORY_LAPORAN_DB)

@app.route("/ai-chat", methods=["GET"])
def ai_chat_page():
    """Halaman antarmuka Asisten AI Q&A."""
    return render_template('ai_chat.html')

@app.route("/api/ask-ai", methods=["POST"])
def ask_ai():
    """Endpoint untuk memproses pertanyaan menggunakan Google Gemini."""
    data = request.get_json(silent=True) or {}
    user_question = str(data.get("question", "")).strip()

    if not user_question:
        return jsonify({"success": False, "error": "Pertanyaan tidak boleh kosong."}), 400

    if len(user_question) > 8000:
        return jsonify({"success": False, "error": "Pertanyaan terlalu panjang. Maksimal 8.000 karakter."}), 400

    system_instruction = (
        "Anda adalah Asisten AI profesional untuk Sistem Manajemen PLTA Curug dan PJT II. "
        "Jawab dalam bahasa Indonesia yang jelas dan profesional. "
        "Bantu menjelaskan operasi PLTA, gardu induk, gangguan, normalisasi, checklist, SOP, "
        "keselamatan kerja, dan informasi umum. Jangan mengarang data teknis, setting proteksi, "
        "nomor SOP, atau instruksi switching. Jika data tidak tersedia, sarankan verifikasi "
        "dengan SOP resmi dan petugas berwenang."
    )

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY belum diset.")

        try:
            from google.genai import types
            client = genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(timeout=45000)
            )
        except Exception:
            client = get_ai_client()

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_question,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.4,
                "max_output_tokens": 1200,
            },
        )

        answer = getattr(response, "text", None)
        if not answer:
            return jsonify({"success": False, "error": "Gemini tidak mengembalikan jawaban teks."}), 502

        return jsonify({"success": True, "answer": answer.strip()})

    except Exception as e:
        print(f"[AI ERROR] {type(e).__name__}: {e}")
        err = str(e).lower()

        if "api key" in err or "gemini_api_key" in err:
            msg = "API Gemini belum dikonfigurasi. Set GEMINI_API_KEY pada environment server."
        elif "quota" in err or "resource_exhausted" in err:
            msg = "Kuota Gemini sedang habis atau terbatas. Silakan coba lagi nanti."
        elif "permission" in err or "unauthorized" in err:
            msg = "API key Gemini tidak memiliki izin yang diperlukan."
        elif "not found" in err or "404" in err:
            msg = "Model Gemini tidak tersedia pada API key atau versi API yang digunakan."
        elif "timeout" in err or "timed out" in err:
            msg = "Koneksi ke layanan AI terlalu lama. Periksa internet/server lalu coba lagi."
        else:
            msg = "Terjadi kesalahan saat menghubungi layanan AI. Cek terminal Flask untuk detail."

        return jsonify({"success": False, "error": msg}), 500

@app.route("/generate-laporan-baru", methods=["POST"])
def generate_laporan_baru():
    jenis = request.form.get("baru_jenis_gangguan")
    waktu = request.form.get("baru_waktu")
    tanggal = request.form.get("baru_tanggal_lengkap")
    kronologi = request.form.get("baru_kronologi")
    
    # Memanggil fungsi pembuatan PDF dari file terpisah (pdf_helper.py)
    pdf_name = generate_pdf_laporan(jenis, waktu, tanggal, kronologi, PDF_FOLDER)
    
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
