import React, { useState } from 'react';

export type ActiveMenu =
  | 'buat-laporan-baru'
  | 'history-gangguan'
  | 'form'
  | 'sejarah'
  | 'struktural-pegawai'
  | 'faq'
  | 'edukasi-video'
  | null;

export const SOP_OPTIONS_DATA = [
  {
    id: 'gi-curug',
    code: 'F-20/GI-CRG/01',
    label: 'Trip GI Curug 70 / 6,3 kV',
    icon: 'fa-solid fa-bolt-lightning text-warning',
    value: 'CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)',
  },
  {
    id: 'pindah-line-jtl-ksb',
    code: 'IK.12-01',
    label: 'Pindah Line: JTL ➔ KSB',
    icon: 'fa-solid fa-arrow-right-arrow-left text-primary',
    value: 'CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV JATILUHUR KE PENGHANTAR 70 KV KOSAMBI (PLN)',
  },
  {
    id: 'pindah-line-ksb-jtl',
    code: 'IK.12-02',
    label: 'Pindah Line: KSB ➔ JTL',
    icon: 'fa-solid fa-repeat text-success',
    value: 'CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV KOSAMBI KE PENGHANTAR 70 KV JATILUHUR (PLN)',
    highlight: true,
  },
  {
    id: 'mini-hydro',
    code: 'IK.10-01',
    label: 'PLTA Mini Hydro Unit Turbin 2x3400 kW',
    icon: 'fa-solid fa-water text-info',
    value: 'CHECK LIST OPERASI PLTA MINI HYDRO CURUG',
  },
];

interface SidebarProps {
  activeMenu: ActiveMenu;
  onSelectMenu: (menu: ActiveMenu) => void;
  onSelectSop?: (sopValue: string) => void;
  selectedSopValue?: string;
  onOpenAiChat: () => void;
  laporanCount: number;
  checklistCount: number;
  isMobile?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeMenu,
  onSelectMenu,
  onSelectSop,
  selectedSopValue,
  onOpenAiChat,
  laporanCount,
  checklistCount,
  isMobile = false,
  onCloseMobile,
}) => {
  const isLaporanSubmenuActive =
    activeMenu === 'buat-laporan-baru' || activeMenu === 'history-gangguan';
  const [laporanSubmenuOpen, setLaporanSubmenuOpen] = useState<boolean>(true);
  const [sopSubmenuOpen, setSopSubmenuOpen] = useState<boolean>(true);

  const handleMenuSelect = (menu: ActiveMenu) => {
    onSelectMenu(menu);
    if (isMobile && onCloseMobile) {
      onCloseMobile();
    }
  };

  const handleSopClick = (val: string) => {
    onSelectMenu('form');
    if (onSelectSop) {
      onSelectSop(val);
    }
    if (isMobile && onCloseMobile) {
      onCloseMobile();
    }
  };

  return (
    <div className={isMobile ? 'w-100' : 'menu-sidebar-container'}>
      <div className={`menu-sidebar ${!isMobile ? 'sticky-top' : ''}`} style={!isMobile ? { top: '1.5rem' } : {}}>
        {/* Mobile Header Bar if inside mobile overlay/sheet */}
        {isMobile && (
          <div className="d-flex align-items-center justify-content-between pb-3 mb-3 border-bottom">
            <div className="d-flex align-items-center gap-2">
              <span className="badge bg-primary text-white p-2 rounded-circle">
                <i className="fa-solid fa-layer-group"></i>
              </span>
              <div>
                <h6 className="fw-bold text-dark mb-0 fs-6">Navigasi Menu Lengkap</h6>
                <small className="text-muted" style={{ fontSize: '0.72rem' }}>Pilih modul operasional PLTA &amp; GI Curug</small>
              </div>
            </div>
            {onCloseMobile && (
              <button
                type="button"
                className="btn btn-sm btn-light border rounded-pill px-3 py-1"
                onClick={onCloseMobile}
              >
                <i className="fa-solid fa-xmark me-1 text-danger"></i> Tutup
              </button>
            )}
          </div>
        )}

        {/* Section 1: Operasional & Manuver */}
        <div className="sidebar-category-title mb-2">
          <span>Modul Operasional</span>
          <span className="badge bg-primary-subtle text-primary border small">SOP PJT II</span>
        </div>

        <div className="d-grid gap-2 mb-4">
          {/* 1. Laporan Gangguan Dropdown */}
          <div>
            <button
              type="button"
              className={`btn menu-btn ${isLaporanSubmenuActive ? 'active' : ''}`}
              onClick={() => setLaporanSubmenuOpen(!laporanSubmenuOpen)}
            >
              <i className="fa-solid fa-triangle-exclamation fa-fw text-warning fs-6"></i>
              <span className="flex-grow-1 text-start">Laporan Gangguan</span>
              <span className="badge bg-warning-subtle text-dark border px-2 py-0.5 rounded-pill small tabular-nums">
                {laporanCount}
              </span>
              <i
                className={`fa-solid fa-chevron-${laporanSubmenuOpen ? 'down' : 'right'} ms-1 fs-7 text-muted`}
              ></i>
            </button>

            {laporanSubmenuOpen && (
              <div className="submenu-container mt-2">
                <button
                  type="button"
                  className={`btn submenu-btn ${
                    activeMenu === 'buat-laporan-baru' ? 'active' : ''
                  }`}
                  onClick={() => handleMenuSelect('buat-laporan-baru')}
                >
                  <i className="fa-solid fa-file-circle-plus text-primary"></i>
                  <span>Buat Laporan Baru</span>
                </button>

                <button
                  type="button"
                  className={`btn submenu-btn ${
                    activeMenu === 'history-gangguan' ? 'active' : ''
                  }`}
                  onClick={() => handleMenuSelect('history-gangguan')}
                >
                  <i className="fa-solid fa-clock-rotate-left text-secondary"></i>
                  <span>Hystori Gangguan</span>
                  <span className="ms-auto text-muted small tabular-nums">({laporanCount})</span>
                </button>
              </div>
            )}
          </div>

          {/* 2. Form Normalisasi & Checklist Main Menu */}
          <div>
            <button
              type="button"
              className={`btn menu-btn ${activeMenu === 'form' ? 'active' : ''}`}
              onClick={() => {
                handleMenuSelect('form');
                setSopSubmenuOpen(true);
              }}
            >
              <i className="fa-solid fa-clipboard-check fa-fw text-primary fs-6"></i>
              <span className="flex-grow-1 text-start">Form SOP &amp; Checklist</span>
              <span className="badge bg-primary-subtle text-primary border border-primary-subtle px-2 py-0.5 rounded-pill small tabular-nums">
                {checklistCount}
              </span>
              <i
                className={`fa-solid fa-chevron-${sopSubmenuOpen ? 'down' : 'right'} ms-1 fs-7 text-muted`}
                onClick={(e) => {
                  e.stopPropagation();
                  setSopSubmenuOpen(!sopSubmenuOpen);
                }}
              ></i>
            </button>

            {/* Submenu Mode Otomatis: Jenis Gangguan / Pengoperasian */}
            {sopSubmenuOpen && (
              <div className="sop-sidebar-list mt-2">
                <div className="px-2 py-1 small fw-bold text-muted" style={{ fontSize: '0.72rem' }}>
                  JENIS GANGGUAN / MODE OTOMATIS:
                </div>
                {SOP_OPTIONS_DATA.map((sop) => {
                  const isCurrent =
                    activeMenu === 'form' && selectedSopValue === sop.value;
                  return (
                    <button
                      type="button"
                      key={sop.id}
                      className={`sop-sidebar-item ${isCurrent ? 'active' : ''}`}
                      onClick={() => handleSopClick(sop.value)}
                      title={sop.value}
                    >
                      <i className={`${sop.icon} fa-fw`}></i>
                      <span className="flex-grow-1 text-truncate text-start">{sop.label}</span>
                      <span
                        className={`badge ${
                          isCurrent
                            ? 'bg-white text-primary'
                            : sop.highlight
                            ? 'bg-success text-white'
                            : 'bg-light text-secondary border'
                        } small py-0.5 px-1.5`}
                        style={{ fontSize: '0.68rem' }}
                      >
                        {sop.code}
                      </span>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Section 2: Data & Organisasi */}
        <div className="sidebar-category-title mb-2">
          <span>Institusi &amp; Sejarah</span>
        </div>

        <div className="d-grid gap-2 mb-4">
          {/* 3. Sejarah Bendung Curug */}
          <button
            type="button"
            className={`btn menu-btn ${activeMenu === 'sejarah' ? 'active' : ''}`}
            onClick={() => handleMenuSelect('sejarah')}
          >
            <i className="fa-solid fa-landmark fa-fw text-warning fs-6"></i>
            <span className="text-start">Sejarah Bendung Curug</span>
          </button>

          {/* 4. Struktural Pegawai */}
          <button
            type="button"
            className={`btn menu-btn ${
              activeMenu === 'struktural-pegawai' ? 'active' : ''
            }`}
            onClick={() => handleMenuSelect('struktural-pegawai')}
          >
            <i className="fa-solid fa-sitemap fa-fw text-success fs-6"></i>
            <span className="text-start">Struktural Pegawai</span>
          </button>

          {/* 5. Pusat Informasi & FAQ */}
          <button
            type="button"
            className={`btn menu-btn ${activeMenu === 'faq' ? 'active' : ''}`}
            onClick={() => handleMenuSelect('faq')}
          >
            <i className="fa-solid fa-water fa-fw text-info fs-6"></i>
            <span className="text-start">Pusat Informasi &amp; Pengetahuan PJT II</span>
          </button>

          {/* 6. Edukasi Animasi & Video Panduan PLTA Curug */}
          <button
            type="button"
            className={`btn menu-btn ${activeMenu === 'edukasi-video' ? 'active' : ''}`}
            onClick={() => handleMenuSelect('edukasi-video')}
          >
            <i className="fa-solid fa-circle-play fa-fw text-danger fs-6"></i>
            <span className="text-start flex-grow-1">Edukasi Animasi &amp; Video PLTA</span>
            <span className="badge bg-danger-subtle text-danger border border-danger-subtle px-1.5 py-0.5 rounded-pill small" style={{ fontSize: '0.68rem' }}>
              Video 4K
            </span>
          </button>

          {/* 7. Asisten AI Operasional */}
          <button
            type="button"
            className="btn menu-btn border-primary-subtle"
            style={{ background: 'linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%)' }}
            onClick={() => {
              onOpenAiChat();
              if (isMobile && onCloseMobile) {
                onCloseMobile();
              }
            }}
          >
            <i className="fa-solid fa-robot fa-fw text-primary fs-6"></i>
            <span className="fw-bold text-primary flex-grow-1 text-start">Asisten AI Operasional</span>
            <span className="badge bg-primary text-white px-2 py-0.5 rounded-pill small">AI</span>
          </button>
        </div>

        {/* Status Sistem Gardu Induk */}
        <div className="p-3 bg-light rounded-4 border">
          <div className="d-flex align-items-center justify-content-between mb-2">
            <span className="text-muted fw-semibold small">Status Siaga GI Curug:</span>
            <span className="badge bg-success-subtle text-success border border-success-subtle px-2 py-0.5 rounded-pill small">
              Siap Operasi
            </span>
          </div>
          <div className="d-flex align-items-center text-dark fw-bold small">
            <span className="spinner-grow spinner-grow-sm me-2 text-success" role="status"></span>
            Transmisi 70 kV Normal
          </div>
          <div className="mt-2 pt-2 border-top text-muted small" style={{ fontSize: '0.75rem' }}>
            <i className="fa-solid fa-shield-halved text-primary me-1"></i>
            Interlock PMT/PMS Aktif &amp; Terkalibrasi
          </div>
        </div>

        {/* Mobile footer close button */}
        {isMobile && onCloseMobile && (
          <div className="mt-3 pt-3 border-top text-center">
            <button
              type="button"
              className="btn btn-primary w-100 rounded-pill py-2.5 shadow-sm fw-semibold"
              onClick={onCloseMobile}
            >
              <i className="fa-solid fa-check me-2"></i> Tutup &amp; Lihat Tampilan
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
