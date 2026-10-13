import React from 'react';

interface StrukturalPegawaiProps {
  onClose: () => void;
}

export const StrukturalPegawai: React.FC<StrukturalPegawaiProps> = ({ onClose }) => {
  return (
    <div className="card content-card mb-4" id="container-struktural-pegawai">
      <button
        type="button"
        className="btn-close-red-container"
        onClick={onClose}
        title="Tutup"
      >
        <i className="fa-solid fa-xmark"></i>
      </button>

      <div className="card-header-custom text-white text-center">
        <h3 className="mb-0 fw-bold fs-4">
          <i className="fa-solid fa-atom me-2 text-info"></i> STRUKTUR LABORATORIUM ENERGI (PLTA CURUG)
        </h3>
        <p className="mb-0 text-white-50 small mt-1">
          Reaksi Sinergi Operasional (Kiri) &amp; Pemeliharaan (Kanan) — PJT II
        </p>
      </div>

      <div className="card-body p-4 p-md-4 chemistry-plant-container">
        <div className="tree-grid">
          {/* LEVEL 1: PIMPINAN PUNCAK */}
          <div className="chem-card card-puncak">
            <span className="chem-badge badge-puncak">
              <i className="fa-solid fa-flask-vial me-1"></i> Inti Reaktor Utama
            </span>
            <h5 className="fw-bold mb-1 text-white">BUDIYO, ST</h5>
            <p className="small text-white-50 mb-0">General Manajer PLTA</p>
          </div>

          <div className="connector-line"></div>

          {/* LEVEL 2: MANAJEMEN OPERASIONAL JARINGAN */}
          <div className="chem-level">
            <div className="chem-card card-manajemen">
              <span className="chem-badge badge-manajemen">
                <i className="fa-solid fa-network-wired me-1"></i> Katalisator Sektor
              </span>
              <h6 className="fw-bold mb-1 text-dark">CARTONO, ST</h6>
              <p className="small text-primary fw-semibold mb-0">
                Manajer Operasional Jaringan
              </p>
            </div>
          </div>

          <div className="connector-line"></div>

          {/* LEVEL 3: ASISTEN MANAJER (KIRI: OPERASIONAL, KANAN: PEMELIHARAAN) */}
          <div className="chem-level" style={{ gap: '40px' }}>
            {/* KIRI: ASISTEN MANAJER OPERASI */}
            <div className="chem-card card-operasional">
              <span className="chem-badge badge-operasional">
                <i className="fa-solid fa-droplet me-1"></i> Formula Operasi
              </span>
              <h6 className="fw-bold mb-1 text-dark">Endang Maryadi</h6>
              <p className="small fw-semibold mb-0" style={{ color: '#0d9488' }}>
                Asisten Manajer Operasi Jaringan
              </p>
            </div>

            {/* KANAN: ASISTEN MANAJER PEMELIHARAAN */}
            <div className="chem-card card-pemeliharaan">
              <span className="chem-badge badge-pemeliharaan">
                <i className="fa-solid fa-bolt me-1"></i> Formula Pemeliharaan
              </span>
              <h6 className="fw-bold mb-1 text-dark">SUMITRA DJARNUDJI, ST</h6>
              <p className="small text-warning-emphasis fw-semibold mb-0">
                Asisten Manajer Pemeliharaan
              </p>
              <span className="team-badge" style={{ borderLeftColor: '#ca8a04' }}>
                Gardu Induk Curug, PLTA Mini Hydro (2x3400 kW), dll
              </span>
            </div>
          </div>

          <div className="connector-line"></div>
          <div
            className="text-center fw-bold text-info small my-2"
            style={{ letterSpacing: '1px' }}
          >
            <i className="fa-solid fa-dna me-1"></i> ⚛️ JALUR KANDUNGAN TIM LAPANGAN: OPERASIONAL (KIRI) VS PEMELIHARAAN (KANAN) ⚛️
          </div>

          {/* LEVEL 4: PEMISAHAN KOLOM (KIRI = OPERASI, KANAN = PEMELIHARAAN) */}
          <div className="branch-container">
            {/* KOLOM KIRI: OPERASIONAL (KELOMPOK I - IV) */}
            <div className="branch-column">
              <div
                className="branch-title text-white"
                style={{ background: '#0d9488' }}
              >
                <i className="fa-solid fa-arrows-split-up-and-left me-1"></i> Sektor Operasional (Kiri)
              </div>

              {/* 1. Saepudin (Kelompok I) */}
              <div className="chem-card card-operasional w-100" style={{ maxWidth: '100%' }}>
                <span className="chem-badge badge-operasional">Kelompok I</span>
                <h6 className="fw-bold mb-1 text-dark">Saepudin</h6>
                <p className="small text-muted mb-1">
                  Supervisor Operasi Mini Hydro, GI &amp; PETT
                </p>
                <span className="team-badge">
                  <strong>Tim:</strong> Ibnu Aulia, Willy Wiriawan
                </span>
              </div>

              {/* 2. Yadi Suwarma (Kelompok II) */}
              <div className="chem-card card-operasional w-100" style={{ maxWidth: '100%' }}>
                <span className="chem-badge badge-operasional">Kelompok II</span>
                <h6 className="fw-bold mb-1 text-dark">Yadi Suwarma</h6>
                <p className="small text-muted mb-1">
                  Supervisor Operasi Mini Hydro, GI &amp; PETT
                </p>
                <span className="team-badge">
                  <strong>Tim:</strong> Achmad Hidayat, Angga Hermawan
                </span>
              </div>

              {/* 3. Andriana (Kelompok III) */}
              <div className="chem-card card-operasional w-100" style={{ maxWidth: '100%' }}>
                <span className="chem-badge badge-operasional">Kelompok III</span>
                <h6 className="fw-bold mb-1 text-dark">Andriana, ST</h6>
                <p className="small text-muted mb-1">
                  Supervisor Operasi Mini Hydro, GI &amp; PETT
                </p>
                <span className="team-badge">
                  <strong>Tim:</strong> Ejan Suryadi, Yanuar Utomo
                </span>
              </div>

              {/* 4. Ahlan Sopiana (Kelompok IV) */}
              <div className="chem-card card-operasional w-100" style={{ maxWidth: '100%' }}>
                <span className="chem-badge badge-operasional">Kelompok IV</span>
                <h6 className="fw-bold mb-1 text-dark">Ahlan Sopiana</h6>
                <p className="small text-muted mb-1">
                  Supervisor Operasi Mini Hydro, GI &amp; PETT
                </p>
                <span className="team-badge">
                  <strong>Tim:</strong> Lugi Rama Diansyah, Rizal Kurniawan
                </span>
              </div>
            </div>

            {/* KOLOM KANAN: PEMELIHARAAN */}
            <div className="branch-column">
              <div
                className="branch-title text-dark"
                style={{ background: '#eab308' }}
              >
                <i className="fa-solid fa-gears me-1"></i> Sektor Pemeliharaan (Kanan)
              </div>

              {/* Mulyadi */}
              <div className="chem-card card-pemeliharaan w-100" style={{ maxWidth: '100%' }}>
                <span className="chem-badge badge-pemeliharaan">Mini Hydro &amp; GI</span>
                <h6 className="fw-bold mb-1 text-dark">Mulyadi</h6>
                <p className="small text-muted mb-1">
                  Supervisor Pemeliharaan Mini Hydro &amp; GI Curug
                </p>
                <span className="team-badge">
                  <strong>Tim:</strong> Kholidin Tri Sandy, Sandy Aditya
                </span>
              </div>

              {/* Yosep Yusnandar */}
              <div className="chem-card card-pemeliharaan w-100" style={{ maxWidth: '100%' }}>
                <span className="chem-badge badge-pemeliharaan">Pompa Elektrik</span>
                <h6 className="fw-bold mb-1 text-dark">Yosep Yusnandar, S.T.</h6>
                <p className="small text-muted mb-1">
                  Supervisor Pemeliharaan Pompa Elektrik Tarum Timur
                </p>
                <span className="team-badge">
                  <strong>Tim:</strong> Akbar Jejef Maulana, Ade Irfan
                </span>
              </div>

              {/* Ahmad Hotib */}
              <div className="chem-card card-pemeliharaan w-100" style={{ maxWidth: '100%' }}>
                <span className="chem-badge badge-pemeliharaan">SUTT &amp; SUTM</span>
                <h6 className="fw-bold mb-1 text-dark">Ahmad Hotib</h6>
                <p className="small text-muted mb-1">
                  Supervisor Pemeliharaan SUTT &amp; SUTM Curug
                </p>
                <span className="team-badge">
                  <strong>Tim:</strong> Staf terkait SUTT &amp; SUTM
                </span>
              </div>

              {/* Yusron */}
              <div className="chem-card card-pemeliharaan w-100" style={{ maxWidth: '100%' }}>
                <span className="chem-badge badge-pemeliharaan">SUTR</span>
                <h6 className="fw-bold mb-1 text-dark">Yusron</h6>
                <p className="small text-muted mb-1">Supervisor Pemeliharaan SUTR Curug</p>
                <span className="team-badge">
                  <strong>Tim:</strong> Nurwanto
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
