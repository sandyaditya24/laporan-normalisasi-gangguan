import React, { useState } from 'react';
import { FaqItem } from '../types';

interface FaqSectionProps {
  onClose: () => void;
}

const FAQ_DATA: FaqItem[] = [
  // 1. PROFIL & DASAR HUKUM
  {
    id: 'profil-1',
    kategori: 'profil',
    question: 'Apa profil resmi dan dasar hukum pendirian Perum Jasa Tirta II (PJT II)?',
    badge: 'Dasar Hukum & Legalitas BUMN',
    highlights: ['PP No. 25 Tahun 2022', 'Didirikan Sejak 1957', 'BUMN Pengelola SDA Terkemuka'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/profil-perusahaan',
    answer:
      'Perum Jasa Tirta II (PJT II) adalah Badan Usaha Milik Negara (BUMN) yang ditugaskan oleh Pemerintah Republik Indonesia untuk menyelenggarakan pengelolaan dan pengusahaan sumber daya air yang terpadu dan berkelanjutan. Berawal dari Proyek Serbaguna Jatiluhur tahun 1957 dan kelembagaan Perum Otorita Jatiluhur (POJ - PP No. 20/1970), status perusahaan bertransformasi menjadi Perum Jasa Tirta II melalui PP No. 94/1999 dan PP No. 7/2010. Kini, berdasarkan regulasi terbaru Peraturan Pemerintah Republik Indonesia No. 25 Tahun 2022, mandat penugasan PJT II diperluas untuk mengoptimalkan potensi sumber daya air nasional demi ketahanan pangan, energi, dan air baku.',
  },
  {
    id: 'profil-2',
    kategori: 'profil',
    question: 'Apa Visi, Misi, dan Nilai Utama (Core Values) Perum Jasa Tirta II?',
    badge: 'Visi, Misi & AKHLAK',
    highlights: ['Visi SDA Berkelanjutan', 'Digitalisasi Teknologi Air', 'Core Values AKHLAK'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/visi-misi',
    answer:
      'Visi Resmi: "Menjadi Perusahaan Terbaik dalam Pengelolaan dan Pengusahaan Sumber Daya Air yang Berkelanjutan di Indonesia".\n\nMisi Utama:\n1. Mengoptimalkan pemanfaatan sumber daya air secara efektif, efisien, inovatif, dan berkelanjutan untuk pelestarian SDA dan ekosistem sungai.\n2. Meningkatkan kapasitas dan kapabilitas SDM yang unggul dan profesional dalam pengelolaan SDA.\n3. Mengembangkan digitalisasi sistem, teknologi hidrologi terintegrasi, dan otomasi keandalan infrastruktur air.\n4. Memperkuat peran strategis BUMN dalam mendukung ketahanan pangan nasional, transisi energi bersih terbarukan, dan pemenuhan air baku perkotaan/industri.\n\nTata Nilai Perusahaan: Mengadopsi Core Values BUMN "AKHLAK" (Amanah, Kompeten, Harmonis, Loyal, Adaptif, Kolaboratif).',
  },
  {
    id: 'profil-3',
    kategori: 'profil',
    question: 'Di mana lokasi Kantor Pusat dan struktur operasional PJT II?',
    badge: 'Kantor Pusat & Wilayah',
    highlights: ['Kantor Pusat: Jatiluhur, Purwakarta', 'Divisi Operasi WS Citarum', 'Sektor Curug & Karawang'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/kontak',
    answer:
      'Kantor Pusat Perum Jasa Tirta II berlokasi di Jl. Lurah Kawi No. 1, Jatiluhur, Kabupaten Purwakarta, Jawa Barat (41152). Struktur operasional terbagi ke dalam unit-unit divisi pengelolaan air, divisi pembangkitan listrik (PLTA), divisi pemeliharaan prasarana sumber daya air, laboratorium kualitas air terakreditasi KAN, serta kantor-kantor seksi operasional di wilayah Purwakarta, Karawang (termasuk Kompleks Bendung Curug), Bekasi, Subang, Indramayu, hingga kantor perwakilan WS Seputih-Sekampung di Lampung.',
  },

  // 2. BENDUNGAN & PENGELOLAAN AIR
  {
    id: 'bendungan-1',
    kategori: 'bendungan',
    question: 'Bagaimana profil teknis dan fungsi Waduk Ir. H. Djuanda (Jatiluhur)?',
    badge: 'Waduk Terbesar di Indonesia',
    highlights: ['Kapasitas Tampung 3 Miliar m³', 'Pasok 80% Air Baku DKI Jakarta', 'Diresmikan 26 Agustus 1967'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/layanan/air-baku',
    answer:
      'Bendungan Ir. H. Djuanda (Waduk Jatiluhur) merupakan bendungan serbaguna terbesar di Indonesia yang terletak di Kabupaten Purwakarta, Jawa Barat. Diresmikan pada tanggal 26 Agustus 1967 oleh Presiden Republik Indonesia, waduk ini membendung Sungai Citarum dengan kapasitas tampung bruto ±3 miliar meter kubik air dan luas genangan danau ±8.300 hektar. Waduk Jatiluhur menyuplai 80% kebutuhan air baku ibukota DKI Jakarta melalui Saluran Tarum Barat, memasok air baku PDAM dan kawasan industri strategis Jawa Barat, mengairi ratusan ribu hektar sawah, menggerakkan turbin PLTA 187 MW, serta berfungsi efektif mengendalikan banjir di wilayah hilir Citarum.',
  },
  {
    id: 'bendungan-2',
    kategori: 'bendungan',
    question: 'Apa fungsi vital Bendung Curug (Bagi Curug) dan Pompa Elektrik Tarum Timur (PETT)?',
    badge: 'Pengatur Air Utama (Bagi Curug)',
    highlights: ['Dibangun Tahun 1968 di Karawang', 'Saluran Tarum Barat, Timur & Utara', 'Pompa Irigasi Subang-Indramayu'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/infrastruktur/bendung-curug',
    answer:
      'Bendung Curug terletak di Desa Curug, Kecamatan Klari/Ciampel, Kabupaten Karawang, dibangun pada tahun 1968. Bendung ini berfungsi sebagai bangunan pengatur pembagian air utama (Bagi Curug) dari aliran Sungai Citarum ke 3 Saluran Induk strategis:\n• Saluran Induk Tarum Barat (Kalimalang): Menyalurkan pasokan air baku vital menuju DKI Jakarta, Kota & Kabupaten Bekasi, dan kawasan industri Karawang.\n• Saluran Induk Tarum Timur: Bersama fasilitas Pompa Elektrik Tarum Timur (PETT), mengalirkan suplai irigasi untuk ratusan ribu hektar lumbung padi di Karawang, Subang, dan Indramayu.\n• Saluran Induk Tarum Utara: Memasok kebutuhan irigasi lahan pertanian dan tambak di kawasan utara Karawang.',
  },
  {
    id: 'bendungan-3',
    kategori: 'bendungan',
    question: 'Bagaimana pola operasi kaskade (cascade system) tiga waduk Sungai Citarum?',
    badge: 'Kaskade Citarum',
    highlights: ['Saguling ➔ Cirata ➔ Jatiluhur', 'Prinsip Equal Sharing', 'Telemetri Real-Time TMA'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/hidrologi',
    answer:
      'Pengelolaan air Sungai Citarum beroperasi dengan pola kaskade terintegrasi (cascade system) menerapkan prinsip "equal sharing" antara tiga waduk besar:\n1. Waduk Saguling (Hulu - Elevasi Normal 643.00 mdpl)\n2. Waduk Cirata (Tengah - Elevasi Normal 220.00 mdpl)\n3. Waduk Jatiluhur (Hilir - Elevasi Normal 107.00 mdpl)\nPola pengoperasian waduk dikoordinasikan secara berkelanjutan berdasarkan data Tinggi Muka Air (TMA), curah hujan, dan rencana debit air yang keluar melalui turbin pembangkit sehingga air yang keluar dari waduk hulu dan tengah dimanfaatkan secara maksimal kembali di Waduk Jatiluhur dan Bendung Curug.',
  },
  {
    id: 'bendungan-4',
    kategori: 'bendungan',
    question: 'Berapa kontribusi pengelolaan irigasi PJT II bagi ketahanan pangan nasional?',
    badge: 'Ketahanan Pangan Nasional',
    highlights: ['Irigasi ±300.000 Hektar Sawah', 'Produksi ±3,3 Juta Ton Padi/Tahun', 'Bebas Biaya Bagi Petani'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/tugas-dan-fungsi',
    answer:
      'PJT II menyalurkan air irigasi untuk mengairi lahan sawah teknis seluas ±240.000 hingga 300.000 hektar di kawasan Pantai Utara (Pantura) Jawa Barat, mencakup Kabupaten Karawang, Subang, Indramayu, dan Bekasi. Dari luasan irigasi ini dihasilkan rata-rata ±3,3 juta ton padi per tahun atau menyumbang sekitar 19% produksi padi Jawa Barat (sekitar 3-4% produksi beras nasional). Seluruh pasokan air irigasi ini disalurkan secara cuma-cuma tanpa pungutan biaya kepada petani sebagai wujud pengabdian negara.',
  },

  // 3. PLTA & ENERGI TERBARUKAN
  {
    id: 'plta-1',
    kategori: 'plta',
    question: 'Berapa kapasitas terpasang dan produksi energi listrik PLTA Ir. H. Djuanda?',
    badge: 'Pembangkit Utama 187 MW',
    highlights: ['Kapasitas 187 MW (6 Turbin Francis)', 'Produksi ±900 Juta kWh/Tahun', 'Transmisi 150 kV & 70 kV GI Curug'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/layanan/energi-listrik',
    answer:
      'PLTA Ir. H. Djuanda dioperasikan pertama kali pada 26 Agustus 1967. Pembangkit ini memiliki kapasitas terpasang total sebesar 187 MW yang dihasilkan dari 6 unit turbin air tipe Francis (Unit I s/d V masing-masing ±31 MW dan Unit VI sebesar 32 MW). Rata-rata produksi listrik hijau mencapai ±900 juta kWh per tahun. Energi listrik disalurkan ke sistem interkoneksi kelistrikan Jawa-Bali melalui transmisi 150 kV milik PT PLN (Persero), serta jalur transmisi 70 kV khusus yang terhubung ke Gardu Induk Curug dan Gardu Induk Ciganea.',
  },
  {
    id: 'plta-2',
    kategori: 'plta',
    question: 'Bagaimana spesifikasi dan operasional PLTA Mini Hydro Unit Turbin 2x3400 kW Curug?',
    badge: 'PLTA Mini Hydro Curug',
    highlights: ['Kapasitas Total 6.800 kW (2x3400 kW)', 'SOP Resmi F-20/DPL/IK.10-01', 'Terkoneksi Switchgear GI Curug'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/layanan/energi-listrik',
    answer:
      'PLTA Mini Hydro Curug berlokasi di kawasan kompleks Bendung Curug, memanfaatkan energi kinetik dan potensial aliran air dengan 2 unit turbin air berdaya masing-masing 3.400 kW (kapasitas total 6.800 kW / 6,8 MW). Pengoperasian unit mengikuti prosedur resmi SOP PJT II (F-20/DPL/IK.10-01), meliputi:\n• Koordinasi debit air dan TMA hulu (+10.5 m) / hilir (+2.1 m) dengan operator Bendung Curug Divisi II.\n• Pemantauan tekanan hidrolik oli governor 60/120 bar dan sistem pendingin turbin.\n• Sinkronisasi otomatis cubicle LGB001JD dan transfer daya listrik ke Gardu Induk Curug 70 / 6,3 kV.',
  },
  {
    id: 'plta-3',
    kategori: 'plta',
    question: 'Bagaimana komitmen PJT II dalam pengembangan Energi Baru Terbarukan (EBT)?',
    badge: 'Inovasi EBT Hijau',
    highlights: ['Pengembangan PLTS Terapung', 'Dukungan Net Zero Emission', 'Pembangkit Listrik Tenaga Mikrohidro (PLTM)'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/berita',
    answer:
      'Mendukung target Net Zero Emission Indonesia pada tahun 2060, PJT II secara aktif memanfaatkan potensi danau waduk dan saluran air untuk pengembangan EBT ramah lingkungan. Inisiatif strategis meliputi pemanfaatan permukaan waduk kaskade untuk Pembangkit Listrik Tenaga Surya (PLTS) Terapung (Floating Solar PV), pengembangan PLTM mikrohidro di berbagai titik bendung sekunder, serta modernisasi turbin pembangkit yang efisien dan minim emisi karbon.',
  },
  {
    id: 'plta-4',
    kategori: 'plta',
    question: 'Bagaimana mekanisme manuver pindah line transmisi 70 kV Curug?',
    badge: 'Manuver Gardu Induk 70 kV',
    highlights: ['SOP IK.12-01 (JTL ➔ KSB)', 'SOP IK.12-02 (KSB ➔ JTL)', 'Interlock PMT & PMS Bay 70 kV'],
    sourceUrl: 'https://www.jasatirta2.co.id',
    answer:
      'Manuver pengalihan beban transmisi 70 kV di Gardu Induk Curug (antara Penghantar Jatiluhur dan Penghantar Kosambi PLN) diatur secara ketat melalui instruksi kerja resmi F-20/DPL/IK.12-01 dan F-20/DPL/IK.12-02. Setiap manuver mewajibkan pelepasan/pemasukan berurutan pada PMT dan PMS di Bay Kosambi, Bay Jatiluhur, penyesuaian Tap Changer (TC) trafo, verifikasi posisi di ruang panel 6 kV & 20 kV, serta koordinasi radio/telepon langsung dengan Operator Control Building Jatiluhur.',
  },

  // 4. WILAYAH KERJA PJT II
  {
    id: 'wilayah-1',
    kategori: 'wilayah',
    question: 'Apa saja 5 Wilayah Sungai (WS) penugasan PJT II berdasarkan PP No. 25 Tahun 2022?',
    badge: 'Perluasan Wilayah Kerja',
    highlights: ['WS Citarum', 'WS Ciliwung-Cisadane', 'WS Cimanuk-Cisanggarung', 'WS Cidanau-Ciujung-Cidurian', 'WS Seputih-Sekampung (Lampung)'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/profil-perusahaan',
    answer:
      'Berdasarkan amanat Peraturan Pemerintah No. 25 Tahun 2022, ruang lingkup operasional Perum Jasa Tirta II diperluas mencakup 5 Wilayah Sungai (WS) strategis:\n1. Wilayah Sungai Citarum (Jawa Barat & DKI Jakarta) - Wilayah operasional utama.\n2. Wilayah Sungai Ciliwung - Cisadane (sebagian wilayah hilir distribusi air baku).\n3. Wilayah Sungai Cimanuk - Cisanggarung (mencakup Garut, Sumedang, Majalengka, Cirebon, Indramayu, Kuningan, dan Brebes).\n4. Wilayah Sungai Cidanau - Ciujung - Cidurian (Provinsi Banten).\n5. Wilayah Sungai Seputih - Sekampung (Provinsi Lampung, Pulau Sumatera) untuk memperluas ketahanan pangan dan energi air nasional.',
  },
  {
    id: 'wilayah-2',
    kategori: 'wilayah',
    question: 'Kabupaten dan Kota mana saja yang dilayani dalam Wilayah Sungai Citarum?',
    badge: 'Cakupan WS Citarum',
    highlights: ['Bandung Raya & Cimahi', 'Purwakarta & Cianjur', 'Karawang, Subang & Bekasi', 'Provinsi DKI Jakarta'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/wilayah-kerja',
    answer:
      'Dalam Wilayah Sungai Citarum dengan luas catchment area ±12.000 km², PJT II melayani 11 daerah tingkat kabupaten/kota serta Provinsi DKI Jakarta, antara lain: Kota Bandung, Kabupaten Bandung, Kabupaten Bandung Barat, Kota Cimahi, Kabupaten Sumedang, Kabupaten Cianjur, Kabupaten Purwakarta, Kabupaten Karawang, Kabupaten Subang, Kota Bekasi, Kabupaten Bekasi, serta suplai air baku harian untuk DKI Jakarta.',
  },

  // 5. LAYANAN & BISNIS KOMERSIAL
  {
    id: 'bisnis-1',
    kategori: 'bisnis',
    question: 'Apa saja portofolio bisnis dan layanan komersial yang disediakan PJT II?',
    badge: 'Layanan & Portofolio Bisnis',
    highlights: ['Pengusahaan Air Baku Industri & PDAM', 'Pembangkitan Listrik Hijau', 'Laboratorium Lingkungan KAN', 'Pariwisata Jatiluhur Valley'],
    sourceUrl: 'https://www.jasatirta2.co.id/id/layanan',
    answer:
      'Selain tugas pelayanan publik (PSO) mengalirkan air irigasi gratis bagi para petani, PJT II menyelenggarakan layanan komersial berbasis Good Corporate Governance:\n• Air Baku Industri & PDAM: Menyalurkan air baku bermutu untuk kawasan industri manufaktur terpadu, utilitas PLTU/pembangkit, serta air curah PDAM perkotaan.\n• Ketenagalistrikan & EBT: Menjual energi listrik hijau terbarukan dari PLTA Jatiluhur dan PLTA Mini Hydro Curug kepada PT PLN (Persero).\n• Laboratorium Kualitas Air & Lingkungan: Layanan pengujian air terakreditasi KAN (LP-629-IDN) untuk uji parameter fisik, kimia, logam berat, dan mikrobiologi.\n• Pariwisata & Hospitality: Pengelolaan destinasi wisata Jatiluhur Valley & Resort, Hotel Graha Vidya Jatiluhur, fasilitas rekreasi air, dan eduwisata bendungan.',
  },
  {
    id: 'bisnis-2',
    kategori: 'bisnis',
    question: 'Bagaimana standar mutu dan sertifikasi yang dimiliki Perum Jasa Tirta II?',
    badge: 'Sertifikasi & Mutu ISO',
    highlights: ['ISO 9001 (Mutu)', 'ISO 14001 (Lingkungan)', 'ISO 37001 (Anti Suap)', 'ISO 45001 (K3)'],
    sourceUrl: 'https://www.jasatirta2.co.id',
    answer:
      'Perum Jasa Tirta II telah tersertifikasi standar internasional dalam seluruh proses operasionalnya, mencakup:\n• ISO 9001:2015 - Sistem Manajemen Mutu Pengelolaan Sumber Daya Air dan Ketenagalistrikan.\n• ISO 14001:2015 - Sistem Manajemen Lingkungan dan Konservasi DAS Citarum.\n• ISO 45001:2018 - Sistem Manajemen Keselamatan dan Kesehatan Kerja (SMK3).\n• ISO 37001:2016 - Sistem Manajemen Anti Penyuapan (SMAP) BUMN Berintegritas.\n• Akreditasi KAN ISO/IEC 17025 untuk Laboratorium Pengujian Kualitas Air.',
  },
];

export const FaqSection: React.FC<FaqSectionProps> = ({ onClose }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [openItem, setOpenItem] = useState<string | null>('profil-1');

  const filteredFaqs = FAQ_DATA.filter((item) => {
    const matchesCategory =
      selectedCategory === 'all' || item.kategori === selectedCategory;
    const query = searchTerm.toLowerCase();
    const matchesSearch =
      item.question.toLowerCase().includes(query) ||
      item.answer.toLowerCase().includes(query) ||
      (item.badge && item.badge.toLowerCase().includes(query)) ||
      (item.highlights && item.highlights.some((h) => h.toLowerCase().includes(query)));
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="card content-card mb-4" id="container-faq-pjt2">
      <button
        type="button"
        className="btn-close-red-container"
        onClick={onClose}
        title="Tutup"
      >
        <i className="fa-solid fa-xmark"></i>
      </button>

      {/* HEADER SECTION */}
      <div
        className="card-header-custom text-white text-center py-4 px-3"
        style={{ background: 'linear-gradient(135deg, #09172e 0%, #032b43 50%, #081b2e 100%)' }}
      >
        <div className="d-flex align-items-center justify-content-center gap-2 mb-2">
          <span className="badge bg-cyan-500 text-dark px-3 py-1 rounded-pill small fw-bold">
            <i className="fa-solid fa-certificate me-1"></i> Data Resmi Terverifikasi
          </span>
          <span className="badge bg-slate-800 text-cyan-300 border border-slate-700 px-3 py-1 rounded-pill small">
            PP No. 25 Tahun 2022
          </span>
        </div>
        <h3 className="mb-1 fw-bold fs-4 text-white">
          <i className="fa-solid fa-water me-2 text-cyan-400"></i> PUSAT INFORMASI &amp; PENGETAHUAN PERUM JASA TIRTA II
        </h3>
        <p className="mb-0 text-cyan-100 small mt-1 max-w-xl mx-auto" style={{ lineHeight: 1.6 }}>
          Kenali lebih dekat profil perusahaan, bendungan, kaskade Citarum, PLTA Mini Hydro 2x3400 kW, dan wilayah kerja resmi yang bersumber dari portal korporasi <strong>www.jasatirta2.co.id</strong>
        </p>

        <div className="mt-3 d-flex flex-wrap align-items-center justify-content-center gap-2">
          <a
            href="https://www.jasatirta2.co.id"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-sm btn-outline-info rounded-pill px-3 py-1 text-white shadow-xs"
            style={{ fontSize: '0.78rem', borderColor: 'rgba(56, 189, 248, 0.4)', background: 'rgba(56, 189, 248, 0.1)' }}
          >
            <i className="fa-solid fa-globe me-1 text-cyan-300"></i> Portal Resmi: <strong>www.jasatirta2.co.id</strong>
            <i className="fa-solid fa-arrow-up-right-from-square ms-1.5 small text-cyan-300"></i>
          </a>
        </div>
      </div>

      <div className="card-body p-3 p-md-4 faq-container">
        {/* HIGHLIGHT FACT METRIC CARDS */}
        <div className="row g-2 mb-4">
          <div className="col-6 col-md-3">
            <div className="p-2.5 rounded-3 border bg-white shadow-xs text-center h-100">
              <div className="text-primary fw-bold fs-6 tabular-nums">±3 Miliar m³</div>
              <div className="text-muted small" style={{ fontSize: '0.7rem' }}>Kapasitas Waduk Jatiluhur</div>
            </div>
          </div>
          <div className="col-6 col-md-3">
            <div className="p-2.5 rounded-3 border bg-white shadow-xs text-center h-100">
              <div className="text-success fw-bold fs-6 tabular-nums">187 MW + 6,8 MW</div>
              <div className="text-muted small" style={{ fontSize: '0.7rem' }}>PLTA Djuanda &amp; Curug</div>
            </div>
          </div>
          <div className="col-6 col-md-3">
            <div className="p-2.5 rounded-3 border bg-white shadow-xs text-center h-100">
              <div className="text-warning fw-bold fs-6 tabular-nums">±300.000 Ha</div>
              <div className="text-muted small" style={{ fontSize: '0.7rem' }}>Irigasi Pantura Jabar</div>
            </div>
          </div>
          <div className="col-6 col-md-3">
            <div className="p-2.5 rounded-3 border bg-white shadow-xs text-center h-100">
              <div className="text-info fw-bold fs-6 tabular-nums">5 Wilayah Sungai</div>
              <div className="text-muted small" style={{ fontSize: '0.7rem' }}>Mandat PP No. 25/2022</div>
            </div>
          </div>
        </div>

        {/* SEARCH BAR */}
        <div className="input-group mb-3 shadow-xs">
          <span className="input-group-text bg-white border-end-0 text-muted">
            <i className="fa-solid fa-magnifying-glass"></i>
          </span>
          <input
            type="text"
            className="form-control border-start-0 ps-0"
            placeholder="Cari topik seputar PJT II (misal: Jatiluhur, PLTA Curug 2x3400 kW, Wilayah Sungai, Irigasi)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {searchTerm && (
            <button
              className="btn btn-outline-secondary border-start-0"
              type="button"
              onClick={() => setSearchTerm('')}
            >
              <i className="fa-solid fa-xmark"></i>
            </button>
          )}
        </div>

        {/* CATEGORY FILTER BUTTONS */}
        <div className="d-flex flex-wrap gap-1.5 mb-4 justify-content-center">
          <button
            type="button"
            className={`btn btn-sm category-btn ${
              selectedCategory === 'all' ? 'btn-primary text-white shadow-xs' : 'btn-outline-secondary bg-white'
            }`}
            onClick={() => setSelectedCategory('all')}
          >
            <i className="fa-solid fa-border-all me-1"></i> Semua Topik ({FAQ_DATA.length})
          </button>
          <button
            type="button"
            className={`btn btn-sm category-btn ${
              selectedCategory === 'profil' ? 'btn-primary text-white shadow-xs' : 'btn-outline-secondary bg-white'
            }`}
            onClick={() => setSelectedCategory('profil')}
          >
            <i className="fa-solid fa-building me-1"></i> Profil &amp; Visi Misi
          </button>
          <button
            type="button"
            className={`btn btn-sm category-btn ${
              selectedCategory === 'bendungan' ? 'btn-primary text-white shadow-xs' : 'btn-outline-secondary bg-white'
            }`}
            onClick={() => setSelectedCategory('bendungan')}
          >
            <i className="fa-solid fa-water me-1"></i> Bendungan &amp; Air
          </button>
          <button
            type="button"
            className={`btn btn-sm category-btn ${
              selectedCategory === 'plta' ? 'btn-primary text-white shadow-xs' : 'btn-outline-secondary bg-white'
            }`}
            onClick={() => setSelectedCategory('plta')}
          >
            <i className="fa-solid fa-bolt me-1"></i> PLTA &amp; Energi Hijau
          </button>
          <button
            type="button"
            className={`btn btn-sm category-btn ${
              selectedCategory === 'wilayah' ? 'btn-primary text-white shadow-xs' : 'btn-outline-secondary bg-white'
            }`}
            onClick={() => setSelectedCategory('wilayah')}
          >
            <i className="fa-solid fa-map-location-dot me-1"></i> Wilayah Kerja (WS)
          </button>
          <button
            type="button"
            className={`btn btn-sm category-btn ${
              selectedCategory === 'bisnis' ? 'btn-primary text-white shadow-xs' : 'btn-outline-secondary bg-white'
            }`}
            onClick={() => setSelectedCategory('bisnis')}
          >
            <i className="fa-solid fa-briefcase me-1"></i> Portofolio Bisnis
          </button>
        </div>

        {/* ACCORDION KNOWLEDGE BASE */}
        <div className="accordion" id="accordionPJT2">
          {filteredFaqs.length > 0 ? (
            filteredFaqs.map((item) => {
              const isOpen = openItem === item.id;
              return (
                <div
                  className="accordion-item mb-2.5 shadow-xs rounded-3 overflow-hidden border"
                  key={item.id}
                  style={{ borderColor: isOpen ? '#93c5fd' : '#e2e8f0' }}
                >
                  <h2 className="accordion-header">
                    <button
                      className={`accordion-button ${isOpen ? '' : 'collapsed'} py-3 px-3.5`}
                      type="button"
                      onClick={() => setOpenItem(isOpen ? null : item.id)}
                      style={{
                        backgroundColor: isOpen ? '#f0f9ff' : '#ffffff',
                        color: isOpen ? '#0369a1' : '#1e293b',
                      }}
                    >
                      <div className="w-100 pe-2">
                        <div className="d-flex align-items-center justify-content-between mb-1">
                          <span
                            className="badge bg-primary-subtle text-primary border border-primary-subtle small fw-semibold"
                            style={{ fontSize: '0.68rem' }}
                          >
                            {item.badge || 'Informasi PJT II'}
                          </span>
                          <span className="text-muted small" style={{ fontSize: '0.7rem' }}>
                            Sumber: www.jasatirta2.co.id
                          </span>
                        </div>
                        <div className="fw-bold text-dark fs-6 d-flex align-items-center gap-2">
                          <i className="fa-solid fa-circle-question text-primary small"></i>
                          <span>{item.question}</span>
                        </div>
                      </div>
                    </button>
                  </h2>
                  {isOpen && (
                    <div className="accordion-collapse show">
                      <div className="accordion-body bg-white text-secondary p-3.5 border-top">
                        <p style={{ whiteSpace: 'pre-line', lineHeight: 1.8, marginBottom: '0.75rem' }}>
                          {item.answer}
                        </p>

                        {/* Highlights & Tags */}
                        {item.highlights && item.highlights.length > 0 && (
                          <div className="d-flex flex-wrap gap-1.5 pt-2 border-top">
                            {item.highlights.map((h, i) => (
                              <span
                                key={i}
                                className="badge bg-light text-dark border px-2 py-1 small fw-normal"
                                style={{ fontSize: '0.72rem' }}
                              >
                                <i className="fa-solid fa-check text-success me-1"></i>
                                {h}
                              </span>
                            ))}
                          </div>
                        )}

                        {/* Source Link */}
                        <div className="mt-2.5 pt-2 border-top d-flex align-items-center justify-content-between small text-muted">
                          <span style={{ fontSize: '0.72rem' }}>
                            <i className="fa-solid fa-building-columns text-primary me-1"></i> Data Resmi Perum Jasa Tirta II
                          </span>
                          <a
                            href={item.sourceUrl || 'https://www.jasatirta2.co.id'}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-primary text-decoration-none fw-semibold"
                            style={{ fontSize: '0.74rem' }}
                          >
                            Pelajari Selengkapnya di Web Resmi <i className="fa-solid fa-arrow-up-right-from-square ms-0.5"></i>
                          </a>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })
          ) : (
            <div className="text-center py-5 bg-white rounded-3 border">
              <i className="fa-solid fa-folder-open text-muted fs-2 mb-2"></i>
              <div className="text-dark fw-bold">Tidak ada informasi yang sesuai</div>
              <small className="text-muted">
                Tidak ditemukan hasil pencarian untuk "{searchTerm}". Silakan gunakan kata kunci lain seperti Jatiluhur, PLTA, Curug, atau Wilayah Sungai.
              </small>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
