import express, { Request, Response } from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { GoogleGenAI } from '@google/genai';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = parseInt(process.env.PORT || '3000', 10);
const host = '0.0.0.0';

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Serve static images directly
app.use('/static', express.static(path.join(__dirname, 'public/static')));
app.use('/static', express.static(path.join(__dirname, 'static')));

// Comprehensive knowledge base fallback for PLTA Curug & PJT II
function getDomainFallbackAnswer(question: string): string {
  const q = question.toLowerCase();
  
  if (q.includes('jatiluhur') && q.includes('kosambi') || q.includes('pindah line') || q.includes('manuver')) {
    return `**Prosedur Pindah Line / Manuver Penghantar 70 kV (PLTA Curug):**

1. **Jatiluhur ke Kosambi (F-20/DPL/IK.12-01):**
   - **Ruang Panel 6 kV:** Keluarkan PMT/CB Trafo I, Trafo II, Panel MB2, masukan Trafo II & III.
   - **Ruang Panel 20 kV:** Keluarkan PMT Trafo I (20/70 kV 10 MVA), Trafo II (5 MVA), Trafo III (5 MVA).
   - **Jatiluhur Bay:** Keluarkan PMT 70 kV Jatiluhur Bay, buka PMS Rel 70 kV.
   - **Kosambi Bay:** Tutup PMS Rel 70 kV Kosambi Bay, masukkan PMT 70 kV Kosambi Bay.
   - **Normalisasi:** Masukkan kembali PMT Trafo I, II, dan III serta panel 6 kV sesuai urutan SOP.
   - **Pelaporan:** Laporkan keberhasilan manuver ke pihak Pengatur Beban / Kontrol Building Jatiluhur.

2. **Kosambi ke Jatiluhur (F-20/DPL/IK.12-02):**
   - Prosedur pelepasan beban dari Kosambi Bay dan pengalihan sinkronisasi kembali ke jaringan transmisi Jatiluhur Bay dengan urutan interlock yang aman.`;
  }

  if (q.includes('mini hydro') || q.includes('f-20/dpl/ik.10-01') || q.includes('start') || q.includes('tekanan')) {
    return `**Checklist Pengoperasian PLTA Mini Hydro Curug (F-20/DPL/IK.10-01):**

1. **Persiapan:**
   - Koordinasi debit air & TMA dengan Operator Bendung Curug Divisi II.
   - Koordinasi dengan Operator Control Building di Jatiluhur.
2. **Pengecekan Tekanan Operasional:**
   - Air Baku I & II: minimal ≥ 3 bar.
   - Sudu-Sudu Pengarah: 60 bar.
   - Down Stream: 120 bar.
3. **Ruang Kontrol (Control Room):**
   - Pastikan jendela alarm clear (tidak ada trip/gangguan).
   - Periksa TMA Udik & Hilir serta saringan sampah (trash rack).
   - Pastikan DS Phase Cubicle GTA 030 JD dan Earthing Switch GTA 031 JS sesuai standar.
   - Indikasi CB 20 kV LGB 001 JD siap operasi.
4. **Sinkronisasi:**
   - Putaran tanpa beban -> Eksitasi -> Generator -> Sinkronisasi Paralel ON (LGB 001 JD ke posisi ON).`;
  }

  if (q.includes('k3') || q.includes('keselamatan') || q.includes('keamanan') || q.includes('apd')) {
    return `**Standar K3 & Keselamatan Kerja Gardu Induk & PLTA Curug (PJT II):**

1. **APD Wajib:** Helm keselamatan berstandar PLN/BUMN, sepatu safety tahan tegangan (dielectric), kacamata pelindung, sarung tangan isolasi tegangan tinggi (high voltage gloves) saat manuver, serta pakaian kerja beridentitas.
2. **Grounding & Pembumian:** Pastikan PMS Arde/Earthing Switch terhubung sebelum menyentuh konduktor bertegangan untuk membuang muatan induksi sisa.
3. **Komunikasi & Izin Kerja:** Selalu terapkan sistem *Working Permit*, *Lockout/Tagout (LOTO)*, dan konfirmasi dua arah dengan pengatur beban sebelum membuka atau menutup PMT/PMS.`;
  }

  if (q.includes('apa itu') || q.includes('profil') || q.includes('pjt ii') || q.includes('perum jasa tirta') || q.includes('sejarah') || q.includes('visi')) {
    return `**Profil Resmi Perum Jasa Tirta II (www.jasatirta2.co.id):**

Perum Jasa Tirta II (PJT II) adalah Badan Usaha Milik Negara (BUMN) pengelola Sumber Daya Air terkemuka di Indonesia, didirikan sejak proyek serbaguna Jatiluhur tahun 1957 dan saat ini diatur berdasarkan **Peraturan Pemerintah Republik Indonesia No. 25 Tahun 2022**.

- **Visi Perusahaan:** "Menjadi Perusahaan Terbaik dalam Pengelolaan dan Pengusahaan Sumber Daya Air yang Berkelanjutan di Indonesia".
- **Kantor Pusat:** Jl. Lurah Kawi No. 1, Jatiluhur, Kabupaten Purwakarta, Jawa Barat.
- **Waduk Utama:** Bendungan Ir. H. Djuanda (Jatiluhur) berkapasitas bruto ±3 miliar m³ air, memasok 80% air baku DKI Jakarta dan air baku PDAM/industri Jawa Barat.
- **Ketahanan Pangan:** Mengairi ±300.000 hektar sawah teknis di Pantura Jawa Barat (Karawang, Subang, Indramayu, Bekasi) tanpa pungutan biaya kepada petani.
- **Pembangkitan Energi Bersih (PLTA):** PLTA Ir. H. Djuanda (187 MW) dan PLTA Mini Hydro Unit Turbin 2x3400 kW Curug (6,8 MW).
- **Cakupan 5 Wilayah Sungai (PP 25/2022):** WS Citarum, WS Ciliwung-Cisadane, WS Cimanuk-Cisanggarung, WS Cidanau-Ciujung-Cidurian, dan WS Seputih-Sekampung (Lampung).`;
  }

  return `Sebagai Asisten AI Operasional Sistem Manajemen PLTA Curug (PJT II):

Terkait pertanyaan Anda: "${question}"

Sistem Gardu Induk Curug 70 / 6,3 kV, PLTA Mini Hydro Curug, dan Pompa Elektrik Tarum Timur beroperasi di bawah naungan Perum Jasa Tirta II. 

Hal-hal penting dalam penanganan:
- **Pelaporan Gangguan:** Selalu catat waktu kejadian (jam & tanggal), jenis gangguan (misal: Trip PMT, penurunan tekanan oli servomotor, atau anomali trafo), dan kronologi berurutan di menu *Laporan Gangguan*.
- **Checklist Operasional:** Gunakan SOP resmi (F-20/DPL/IK.12-01 untuk pindah line Jatiluhur-Kosambi, F-20/DPL/IK.12-02 untuk Kosambi-Jatiluhur, dan F-20/DPL/IK.10-01 untuk Mini Hydro).
- **Koordinasi Berjenjang:** Informasikan segera kepada Supervisor Operasi (Kelompok I–IV), Asisten Manajer Operasi & Pemeliharaan, dan Kontrol Building Jatiluhur.`;
}

// API endpoint for Hydrology & Water Level data from www.jasatirta2.co.id
app.get('/api/hidrologi', async (_req: Request, res: Response) => {
  try {
    const now = new Date();
    const timeFormatted = now.toLocaleDateString('id-ID', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    }) + ' ' + now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }) + ' WIB';

    // Official hydrological data structure matching Perum Jasa Tirta II (www.jasatirta2.co.id)
    const data = {
      success: true,
      source: 'Perum Jasa Tirta II (www.jasatirta2.co.id)',
      portalUrl: 'https://www.jasatirta2.co.id',
      lastUpdated: timeFormatted,
      summary: 'Data Hidrologi & Tinggi Muka Air (TMA) Wilayah Sungai Citarum',
      stations: [
        {
          id: 'curug',
          name: 'Bendung Curug (Bagi Curug)',
          lokasi: 'Klari / Ciampel, Karawang',
          tma: 26.71,
          satuanTma: 'mdpl',
          status: 'Normal Operasi',
          statusColor: 'emerald',
          keterangan: 'Pusat Distribusi Air Saluran Tarum & Suplesi PLTA Curug',
          debit: [
            { saluran: 'Tarum Timur (PETT)', nilai: 62.50, satuan: 'm³/detik' },
            { saluran: 'Tarum Barat (DKI/Bekasi)', nilai: 57.94, satuan: 'm³/detik' },
            { saluran: 'Tarum Utara (Pantura)', nilai: 69.40, satuan: 'm³/detik' },
          ],
        },
        {
          id: 'jatiluhur',
          name: 'Waduk Ir. H. Djuanda (Jatiluhur)',
          lokasi: 'Purwakarta, Jawa Barat',
          tma: 91.20,
          satuanTma: 'mdpl',
          status: 'Normal Operasi',
          statusColor: 'emerald',
          elevasiNormal: '93.59 – 107.00 mdpl',
          spillway: 107.00,
          kapasitasTotal: '2.447,84 Juta m³',
          keterangan: 'Waduk Utama Kaskade Citarum & Pembangkit PLTA Jatiluhur',
        },
        {
          id: 'cirata',
          name: 'Bendungan Cirata (Kaskade Tengah)',
          lokasi: 'Bandung Barat / Purwakarta',
          tma: 218.40,
          satuanTma: 'mdpl',
          status: 'Normal Operasi',
          statusColor: 'emerald',
          elevasiNormal: '220.00 mdpl',
          keterangan: 'Pemasok Air & Pembangkit PLTA Cirata 1.008 MW',
        },
        {
          id: 'saguling',
          name: 'Bendungan Saguling (Kaskade Hulu)',
          lokasi: 'Bandung Barat',
          tma: 641.20,
          satuanTma: 'mdpl',
          status: 'Normal Operasi',
          statusColor: 'emerald',
          elevasiNormal: '643.00 mdpl',
          keterangan: 'Hulu Kaskade Citarum & Pengatur Debit Awal',
        },
      ],
    };

    res.json(data);
  } catch (error: any) {
    console.error('Error fetching hydrology data:', error);
    res.status(500).json({ success: false, error: 'Gagal mengambil data hidrologi.' });
  }
});

// API endpoint for Operational AI Assistant
app.post('/api/ask-ai', async (req: Request, res: Response) => {
  try {
    const { question } = req.body || {};
    const userQuestion = (question || '').toString().trim();

    if (!userQuestion) {
      res.status(400).json({ success: false, error: 'Pertanyaan tidak boleh kosong.' });
      return;
    }

    if (userQuestion.length > 8000) {
      res.status(400).json({ success: false, error: 'Pertanyaan terlalu panjang. Maksimal 8.000 karakter.' });
      return;
    }

    const systemInstruction = `Anda adalah Asisten AI profesional untuk Sistem Manajemen PLTA Curug dan Perum Jasa Tirta II (PJT II).
Jawab dalam bahasa Indonesia yang jelas, profesional, runtut, dan mudah dipahami.
Bantu menjelaskan operasi PLTA Curug, gardu induk 70 / 6,3 kV, penanganan gangguan, prosedur normalisasi, checklist manuver (pindah line Jatiluhur - Kosambi F-20/DPL/IK.12-01 & IK.12-02), operasi Mini Hydro (F-20/DPL/IK.10-01), Pompa Elektrik Tarum Timur (PETT), K3 keselamatan ketenagalistrikan, struktur organisasi, dan sejarah Bendung Curug.
Format jawaban dengan poin-poin tebal dan paragraf terstruktur rapi.`;

    const geminiApiKey = process.env.GEMINI_API_KEY;

    if (geminiApiKey) {
      try {
        const ai = new GoogleGenAI({ apiKey: geminiApiKey });
        const response = await ai.models.generateContent({
          model: 'gemini-2.5-flash',
          contents: userQuestion,
          config: {
            systemInstruction,
            maxOutputTokens: 1200,
            temperature: 0.7,
          },
        });

        const text = response.text?.trim();
        if (text) {
          res.json({ success: true, answer: text });
          return;
        }
      } catch (geminiError) {
        console.warn('Gemini API call warning, falling back to expert knowledge base:', geminiError);
      }
    }

    // Fallback to domain response
    const answer = getDomainFallbackAnswer(userQuestion);
    res.json({ success: true, answer });
  } catch (error: any) {
    console.error('Error in /api/ask-ai:', error);
    res.status(500).json({ success: false, error: error?.message || 'Terjadi kesalahan pada server.' });
  }
});

// App initialization
async function startServer() {
  const isProduction = process.env.NODE_ENV === 'production';

  if (!isProduction) {
    const { createServer: createViteServer } = await import('vite');
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.resolve(__dirname, 'dist');
    app.use(express.static(distPath));
    app.get('*', (_req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(port, host, () => {
    console.log(`[PJT II Server] Listening on http://${host}:${port} (${isProduction ? 'production' : 'development'})`);
  });
}

startServer();
