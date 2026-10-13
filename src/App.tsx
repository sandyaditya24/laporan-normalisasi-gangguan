import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Sidebar, ActiveMenu } from './components/Sidebar';
import { LaporanBaruForm } from './components/LaporanBaruForm';
import { HistoryGangguan } from './components/HistoryGangguan';
import { SejarahCurug } from './components/SejarahCurug';
import { StrukturalPegawai } from './components/StrukturalPegawai';
import { FaqSection } from './components/FaqSection';
import { EdukasiVideoOperasional } from './components/EdukasiVideoOperasional';
import { ChecklistForm } from './components/ChecklistForm';
import { AiAssistantModal } from './components/AiAssistantModal';
import { LaporanBaru, ChecklistArchive } from './types';
import { generateLaporanBaruPdf } from './utils/pdfGenerator';

const BACKGROUND_LIST = [
  { url: '/static/CURUGTEMPODULU.jpg', name: 'Curug Tempo Dulu' },
  {
    url: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1920&q=80',
    name: 'Waduk Ir. H. Djuanda (Jatiluhur)',
  },
  {
    url: 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1920&q=80',
    name: 'Kawasan Aliran Sungai',
  },
];

const SEED_LAPORAN: LaporanBaru[] = [
  {
    id: 'lap-seed-1',
    jenis: 'Trip PMT 70 kV Jatiluhur Bay',
    tanggal: '2026-10-10',
    waktu: '14:25',
    kronologi:
      'Terjadi indikasi lonjakan arus pada penghantar 70 kV jalur Jatiluhur akibat sambaran petir di dekat tower transmisi. Proteksi OCR/GFR bekerja mengeluarkan PMT 70 kV. Petugas piket regu operasi melakukan pengecekan visual, isolasi gangguan, koordinasi dengan kontrol building Jatiluhur, dan berhasil melakukan penutupan kembali secara aman setelah kondisi clear.',
    pdf_name: 'Laporan_Gangguan_Baru_20261010_142500.pdf',
    createdAt: '10/10/2026, 14:30',
  },
];

const SEED_CHECKLIST: ChecklistArchive[] = [
  {
    id: 'chk-seed-1',
    name: 'Checklist_Normalisasi_Curug_Operasi_20261010.pdf',
    date: '2026-10-10 Pukul 14:45 WIB',
    kategori: 'Gardu Induk Curug',
    jenisGangguan:
      'CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)',
    mode: 'manual',
    namaGroup: 'Regu 1 (Piket Siaga)',
    namaPetugas: 'Saepudin, Ibnu Aulia, Willy Wiriawan',
    manualRows: [
      { no: 1, penanganan: 'Pengecekan Jendela Alarm & Annunciator Relai', jam: '14:26', status: 'Clear / Tidak ada anomali' },
      { no: 2, penanganan: 'Keluarkan PMT/CB Panel Trafo 500 KVA Trafo I & II', jam: '14:30', status: 'Posisi Terbuka (Open)' },
      { no: 3, penanganan: 'Koordinasi Manuver dengan Kontrol Building Jatiluhur', jam: '14:35', status: 'Disetujui untuk Re-energize' },
      { no: 4, penanganan: 'Penutupan kembali PMT 70 kV Jatiluhur Bay', jam: '14:40', status: 'Tegangan Normal 70 kV' },
      { no: 5, penanganan: 'Normalisasi beban ruang panel 6,3 kV & 20 kV', jam: '14:45', status: 'Selesai & Aman' },
    ],
  },
];

export const App: React.FC = () => {
  const [bgIndex, setBgIndex] = useState(0);
  const [activeMenu, setActiveMenu] = useState<ActiveMenu>('form');
  const [activeSopValue, setActiveSopValue] = useState<string>(
    'CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)'
  );
  const [aiModalOpen, setAiModalOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Alert state
  const [recentlyCreatedPdf, setRecentlyCreatedPdf] = useState<{
    name: string;
    item?: LaporanBaru;
  } | null>(null);

  // Storage states
  const [laporanList, setLaporanList] = useState<LaporanBaru[]>(() => {
    try {
      const saved = localStorage.getItem('PJT_LAPORAN_LIST');
      return saved ? JSON.parse(saved) : SEED_LAPORAN;
    } catch {
      return SEED_LAPORAN;
    }
  });

  const [checklistList, setChecklistList] = useState<ChecklistArchive[]>(() => {
    try {
      const saved = localStorage.getItem('PJT_CHECKLIST_LIST');
      return saved ? JSON.parse(saved) : SEED_CHECKLIST;
    } catch {
      return SEED_CHECKLIST;
    }
  });

  // Sync background to body
  useEffect(() => {
    const current = BACKGROUND_LIST[bgIndex];
    document.body.style.backgroundImage = `linear-gradient(135deg, rgba(5, 11, 20, 0.88), rgba(11, 19, 43, 0.92)), url('${current.url}')`;
  }, [bgIndex]);

  // Background auto-rotation every 14 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      setBgIndex((prev) => (prev + 1) % BACKGROUND_LIST.length);
    }, 14000);
    return () => clearInterval(timer);
  }, []);

  // Save to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('PJT_LAPORAN_LIST', JSON.stringify(laporanList));
    } catch (e) {
      console.warn('Storage save error:', e);
    }
  }, [laporanList]);

  useEffect(() => {
    try {
      localStorage.setItem('PJT_CHECKLIST_LIST', JSON.stringify(checklistList));
    } catch (e) {
      console.warn('Storage save error:', e);
    }
  }, [checklistList]);

  const handleCycleBackground = () => {
    setBgIndex((prev) => (prev + 1) % BACKGROUND_LIST.length);
  };

  const handleSaveLaporan = (laporan: LaporanBaru) => {
    setLaporanList((prev) => [laporan, ...prev]);
    setRecentlyCreatedPdf({ name: laporan.pdf_name, item: laporan });
  };

  const handleSaveChecklist = (archive: ChecklistArchive) => {
    setChecklistList((prev) => [archive, ...prev]);
    setRecentlyCreatedPdf({ name: archive.name });
  };

  const handleSelectSopFromSidebar = (sopValue: string) => {
    setActiveSopValue(sopValue);
    setActiveMenu('form');
    setMobileMenuOpen(false);
  };

  const getMenuTitle = (menu: ActiveMenu) => {
    switch (menu) {
      case 'form':
        return 'Form SOP & Checklist';
      case 'buat-laporan-baru':
        return 'Buat Laporan Baru';
      case 'history-gangguan':
        return 'Hystori Gangguan';
      case 'sejarah':
        return 'Sejarah Bendung Curug';
      case 'struktural-pegawai':
        return 'Struktural Pegawai';
      case 'faq':
        return 'Pusat Info & FAQ PJT II';
      case 'edukasi-video':
        return 'Edukasi & Video Panduan';
      default:
        return 'Beranda Sistem Operasi';
    }
  };

  return (
    <div className="container mt-2 mt-md-3 mb-5 enterprise-wrapper">
      {/* SUCCESS BANNER ALERT */}
      {recentlyCreatedPdf && (
        <div
          className="alert alert-success alert-dismissible fade show shadow-sm mb-3 mb-md-4 rounded-4 border-success"
          role="alert"
        >
          <div className="d-flex align-items-center">
            <i className="fa-solid fa-circle-check fs-4 text-success me-3"></i>
            <div>
              <strong className="fs-6">
                Laporan berhasil disimpan dan PDF berhasil dibuat!
              </strong>
              <div className="text-secondary small mt-0.5">
                Nama Berkas: <span className="font-monospace fw-bold">{recentlyCreatedPdf.name}</span>
              </div>
            </div>
          </div>
          <div className="mt-2 pt-2 border-top d-flex gap-2">
            {recentlyCreatedPdf.item ? (
              <button
                type="button"
                className="btn btn-sm btn-success rounded-pill px-3"
                onClick={() => generateLaporanBaruPdf(recentlyCreatedPdf.item!)}
              >
                <i className="fa-solid fa-download me-1"></i> Unduh PDF Laporan
              </button>
            ) : null}
            <button
              type="button"
              className="btn btn-sm btn-outline-success rounded-pill px-3"
              onClick={() => {
                setActiveMenu('history-gangguan');
                setRecentlyCreatedPdf(null);
              }}
            >
              Lihat Riwayat Berkas
            </button>
          </div>
          <button
            type="button"
            className="btn-close"
            onClick={() => setRecentlyCreatedPdf(null)}
            aria-label="Tutup"
          ></button>
        </div>
      )}

      {/* DASHBOARD HEADER WITH HYDROLOGICAL DATA */}
      <Header
        currentBgName={BACKGROUND_LIST[bgIndex].name}
        onCycleBg={handleCycleBackground}
        totalLaporan={laporanList.length}
        totalChecklist={checklistList.length}
      />

      {/* MOBILE ADAPTIVE CONTROL BAR (Visible on Mobile/Tablet < 992px) */}
      <div className="mobile-nav-hub d-lg-none mb-3">
        <div className="card shadow-sm border-0 rounded-4 overflow-hidden" style={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(16px)' }}>
          <div className="p-3 d-flex align-items-center justify-content-between border-bottom">
            <div className="d-flex align-items-center gap-2.5">
              <span className="badge bg-primary text-white p-2 rounded-circle shadow-xs">
                <i className="fa-solid fa-bars-staggered"></i>
              </span>
              <div>
                <div className="text-muted small" style={{ fontSize: '0.68rem', letterSpacing: '0.04em', textTransform: 'uppercase' }}>
                  Modul Aktif:
                </div>
                <div className="fw-bold text-dark text-truncate" style={{ maxWidth: '190px', fontSize: '0.9rem' }}>
                  {getMenuTitle(activeMenu)}
                </div>
              </div>
            </div>

            <div className="d-flex align-items-center gap-2">
              <button
                type="button"
                className={`btn btn-sm ${mobileMenuOpen ? 'btn-danger' : 'btn-primary'} rounded-pill px-3 py-1.5 shadow-xs fw-semibold d-flex align-items-center gap-1.5`}
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                style={{ fontSize: '0.8rem' }}
              >
                <i className={`fa-solid ${mobileMenuOpen ? 'fa-xmark' : 'fa-compass'}`}></i>
                <span>{mobileMenuOpen ? 'Tutup Menu' : 'Pilih Menu'}</span>
              </button>
            </div>
          </div>

          {/* Touch-Friendly Horizontal Quick Actions Strip for Mobile */}
          <div className="p-2 bg-light bg-opacity-75 overflow-x-auto d-flex gap-1.5 no-scrollbar">
            <button
              type="button"
              className={`btn btn-sm rounded-pill text-nowrap px-3 ${activeMenu === 'form' ? 'btn-primary shadow-xs' : 'btn-white bg-white text-secondary border'}`}
              onClick={() => { setActiveMenu('form'); setMobileMenuOpen(false); }}
              style={{ fontSize: '0.78rem' }}
            >
              <i className="fa-solid fa-clipboard-check me-1.5 text-info"></i> Form SOP
            </button>
            <button
              type="button"
              className={`btn btn-sm rounded-pill text-nowrap px-3 ${activeMenu === 'form' && activeSopValue.includes('KOSAMBI KE PENGHANTAR 70 KV JATILUHUR') ? 'btn-success text-white' : 'btn-white bg-white text-secondary border'}`}
              onClick={() => handleSelectSopFromSidebar('CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV KOSAMBI KE PENGHANTAR 70 KV JATILUHUR (PLN)')}
              style={{ fontSize: '0.78rem' }}
            >
              <i className="fa-solid fa-repeat me-1.5 text-success"></i> KSB ➔ JTL (IK.12-02)
            </button>
            <button
              type="button"
              className={`btn btn-sm rounded-pill text-nowrap px-3 ${activeMenu === 'buat-laporan-baru' ? 'btn-primary shadow-xs' : 'btn-white bg-white text-secondary border'}`}
              onClick={() => { setActiveMenu('buat-laporan-baru'); setMobileMenuOpen(false); }}
              style={{ fontSize: '0.78rem' }}
            >
              <i className="fa-solid fa-file-circle-plus me-1.5 text-warning"></i> Laporan Baru
            </button>
            <button
              type="button"
              className={`btn btn-sm rounded-pill text-nowrap px-3 ${activeMenu === 'history-gangguan' ? 'btn-primary shadow-xs' : 'btn-white bg-white text-secondary border'}`}
              onClick={() => { setActiveMenu('history-gangguan'); setMobileMenuOpen(false); }}
              style={{ fontSize: '0.78rem' }}
            >
              <i className="fa-solid fa-clock-rotate-left me-1.5 text-secondary"></i> Riwayat ({laporanList.length})
            </button>
            <button
              type="button"
              className={`btn btn-sm rounded-pill text-nowrap px-3 ${activeMenu === 'faq' ? 'btn-primary shadow-xs' : 'btn-white bg-white text-secondary border'}`}
              onClick={() => { setActiveMenu('faq'); setMobileMenuOpen(false); }}
              style={{ fontSize: '0.78rem' }}
            >
              <i className="fa-solid fa-water me-1.5 text-info"></i> Info PJT II
            </button>
            <button
              type="button"
              className={`btn btn-sm rounded-pill text-nowrap px-3 ${activeMenu === 'edukasi-video' ? 'btn-danger text-white shadow-xs' : 'btn-white bg-white text-secondary border'}`}
              onClick={() => { setActiveMenu('edukasi-video'); setMobileMenuOpen(false); }}
              style={{ fontSize: '0.78rem' }}
            >
              <i className="fa-solid fa-circle-play me-1.5 text-danger"></i> Video Panduan
            </button>
            <button
              type="button"
              className="btn btn-sm rounded-pill text-nowrap px-3 btn-dark text-cyan-300"
              onClick={() => { setAiModalOpen(true); setMobileMenuOpen(false); }}
              style={{ fontSize: '0.78rem' }}
            >
              <i className="fa-solid fa-robot me-1.5 text-cyan-400"></i> Tanya AI
            </button>
          </div>
        </div>

        {/* Mobile Full Menu Drawer Dropdown */}
        {mobileMenuOpen && (
          <div className="mobile-menu-drawer mt-2 animate-fade-in">
            <Sidebar
              activeMenu={activeMenu}
              onSelectMenu={(menu) => {
                setActiveMenu(menu);
                setMobileMenuOpen(false);
              }}
              onSelectSop={handleSelectSopFromSidebar}
              selectedSopValue={activeSopValue}
              onOpenAiChat={() => {
                setAiModalOpen(true);
                setMobileMenuOpen(false);
              }}
              laporanCount={laporanList.length}
              checklistCount={checklistList.length}
              isMobile={true}
              onCloseMobile={() => setMobileMenuOpen(false)}
            />
          </div>
        )}
      </div>

      {/* MAIN WORKSPACE: SIDEBAR (LAPTOP) + CONTENT */}
      <div className="row g-3 g-lg-4">
        {/* DESKTOP SIDEBAR NAVIGATION (Hidden on mobile phones, shown on laptop/desktop) */}
        <div className="col-lg-3 d-none d-lg-block">
          <Sidebar
            activeMenu={activeMenu}
            onSelectMenu={(menu) => setActiveMenu(menu)}
            onSelectSop={handleSelectSopFromSidebar}
            selectedSopValue={activeSopValue}
            onOpenAiChat={() => setAiModalOpen(true)}
            laporanCount={laporanList.length}
            checklistCount={checklistList.length}
            isMobile={false}
          />
        </div>

        {/* CONTENT AREA: Takes 100% width on Mobile, 75% width on Laptop */}
        <div className="col-12 col-lg-9">
          {activeMenu === 'buat-laporan-baru' && (
            <LaporanBaruForm
              onSaveLaporan={handleSaveLaporan}
              onClose={() => setActiveMenu(null)}
            />
          )}

          {activeMenu === 'history-gangguan' && (
            <HistoryGangguan
              laporanList={laporanList}
              checklistList={checklistList}
              onClose={() => setActiveMenu(null)}
            />
          )}

          {activeMenu === 'sejarah' && (
            <SejarahCurug onClose={() => setActiveMenu(null)} />
          )}

          {activeMenu === 'struktural-pegawai' && (
            <StrukturalPegawai onClose={() => setActiveMenu(null)} />
          )}

          {activeMenu === 'faq' && (
            <FaqSection onClose={() => setActiveMenu(null)} />
          )}

          {activeMenu === 'edukasi-video' && (
            <EdukasiVideoOperasional onClose={() => setActiveMenu(null)} />
          )}

          {activeMenu === 'form' && (
            <ChecklistForm
              onSaveChecklist={handleSaveChecklist}
              onClose={() => setActiveMenu(null)}
              initialSopValue={activeSopValue}
              onSopChange={(val) => setActiveSopValue(val)}
            />
          )}

          {activeMenu === null && (
            <div className="card content-card p-4 p-md-5 text-center">
              <i className="fa-solid fa-bolt-lightning text-primary fs-1 mb-3"></i>
              <h4 className="fw-bold text-dark">Sistem Manajemen PLTA Curug</h4>
              <p className="text-muted max-w-md mx-auto mb-4">
                Silakan pilih menu di atas atau di samping untuk membuat laporan gangguan, membuka form checklist normalisasi, menonton video edukasi panduan operasional, meninjau sejarah, atau berkonsultasi dengan asisten AI operasional.
              </p>
              <div className="d-flex flex-wrap justify-content-center gap-2">
                <button
                  type="button"
                  className="btn btn-primary px-4 py-2.5 rounded-pill shadow-sm"
                  onClick={() => setActiveMenu('form')}
                >
                  <i className="fa-solid fa-clipboard-list me-2"></i> Buka Form Checklist
                </button>
                <button
                  type="button"
                  className="btn btn-outline-danger px-4 py-2.5 rounded-pill shadow-xs"
                  onClick={() => setActiveMenu('edukasi-video')}
                >
                  <i className="fa-solid fa-circle-play me-2"></i> Edukasi &amp; Video Panduan
                </button>
                <button
                  type="button"
                  className="btn btn-outline-primary px-4 py-2.5 rounded-pill"
                  onClick={() => setActiveMenu('buat-laporan-baru')}
                >
                  <i className="fa-solid fa-file-circle-plus me-2"></i> Buat Laporan Baru
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* AI ASSISTANT OPERATIONAL MODAL */}
      <AiAssistantModal
        isOpen={aiModalOpen}
        onClose={() => setAiModalOpen(false)}
      />
    </div>
  );
};
