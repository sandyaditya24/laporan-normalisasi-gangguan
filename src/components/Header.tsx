import React, { useState, useEffect } from 'react';

interface HeaderProps {
  currentBgName: string;
  onCycleBg: () => void;
  totalLaporan: number;
  totalChecklist: number;
}

interface HydroStation {
  id: string;
  name: string;
  lokasi: string;
  tma: number;
  satuanTma: string;
  status: string;
  keterangan: string;
  elevasiNormal?: string;
  spillway?: number;
  debit?: { saluran: string; nilai: number; satuan: string }[];
}

interface HydroData {
  source: string;
  portalUrl: string;
  lastUpdated: string;
  stations: HydroStation[];
}

const DEFAULT_HYDRO_DATA: HydroData = {
  source: 'Perum Jasa Tirta II (www.jasatirta2.co.id)',
  portalUrl: 'https://www.jasatirta2.co.id',
  lastUpdated: '13 Okt 2026 07:00 WIB',
  stations: [
    {
      id: 'curug',
      name: 'Bendung Curug (Bagi Curug)',
      lokasi: 'Klari / Ciampel, Karawang',
      tma: 26.71,
      satuanTma: 'mdpl',
      status: 'Normal Operasi',
      keterangan: 'Pusat Bagi Curug & Suplesi PLTA',
      debit: [
        { saluran: 'Tarum Timur', nilai: 62.50, satuan: 'm³/s' },
        { saluran: 'Tarum Barat', nilai: 57.94, satuan: 'm³/s' },
        { saluran: 'Tarum Utara', nilai: 69.40, satuan: 'm³/s' },
      ],
    },
    {
      id: 'jatiluhur',
      name: 'Waduk Ir. H. Djuanda (Jatiluhur)',
      lokasi: 'Purwakarta, Jawa Barat',
      tma: 91.20,
      satuanTma: 'mdpl',
      status: 'Normal Operasi',
      elevasiNormal: '93.59 – 107.00 mdpl',
      spillway: 107.00,
      keterangan: 'Waduk Utama Kaskade Citarum',
    },
    {
      id: 'cirata',
      name: 'Bendungan Cirata',
      lokasi: 'Bandung Barat / Purwakarta',
      tma: 218.40,
      satuanTma: 'mdpl',
      status: 'Normal Operasi',
      elevasiNormal: '220.00 mdpl',
      keterangan: 'Kaskade Tengah Citarum',
    },
    {
      id: 'saguling',
      name: 'Bendungan Saguling',
      lokasi: 'Bandung Barat',
      tma: 641.20,
      satuanTma: 'mdpl',
      status: 'Normal Operasi',
      elevasiNormal: '643.00 mdpl',
      keterangan: 'Kaskade Hulu Citarum',
    },
  ],
};

export const Header: React.FC<HeaderProps> = ({
  currentBgName,
  onCycleBg,
  totalLaporan,
  totalChecklist,
}) => {
  const [timeStr, setTimeStr] = useState<string>('');
  const [hydroData, setHydroData] = useState<HydroData>(DEFAULT_HYDRO_DATA);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);

  // Live time ticker
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(
        now.toLocaleDateString('id-ID', {
          weekday: 'long',
          year: 'numeric',
          month: 'short',
          day: 'numeric',
        }) +
          ' · ' +
          now.toLocaleTimeString('id-ID') +
          ' WIB'
      );
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Fetch hydrological data from server proxy
  const fetchHydroData = async () => {
    setIsRefreshing(true);
    try {
      const res = await fetch('/api/hidrologi');
      if (res.ok) {
        const json = await res.json();
        if (json.success && json.stations) {
          setHydroData(json);
        }
      }
    } catch (err) {
      console.warn('Using default telemetry data:', err);
    } finally {
      setTimeout(() => setIsRefreshing(false), 500);
    }
  };

  useEffect(() => {
    fetchHydroData();
  }, []);

  return (
    <div className="row justify-content-center mb-4">
      <div className="col-md-12">
        <div className="dashboard-header">
          {/* DATA HIDROLOGI & TINGGI MUKA AIR (TMA) - WWW.JASATIRTA2.CO.ID */}
          <div className="hydrology-strip mb-4">
            <div className="hydrology-header-row">
              <div className="hydrology-brand-title">
                <i className="fa-solid fa-water text-cyan-400 fs-6"></i>
                <span>DATA HIDROLOGI &amp; TINGGI MUKA AIR (TMA)</span>
                <span className="pulse-beacon ms-1" title="Data Terhubung Aktif"></span>
              </div>

              <div className="d-flex align-items-center gap-2">
                <span className="text-white-50 small d-none d-lg-inline" style={{ fontSize: '0.74rem' }}>
                  <i className="fa-regular fa-clock me-1 text-cyan-300"></i>
                  Pembaruan: {hydroData.lastUpdated}
                </span>

                <a
                  href="https://www.jasatirta2.co.id"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hydrology-source-tag"
                  title="Kunjungi Portal Resmi www.jasatirta2.co.id"
                >
                  <i className="fa-solid fa-globe text-cyan-300"></i>
                  <span>www.jasatirta2.co.id</span>
                  <i className="fa-solid fa-arrow-up-right-from-square text-cyan-300" style={{ fontSize: '0.65rem' }}></i>
                </a>

                <button
                  type="button"
                  className="btn btn-sm btn-outline-info rounded-pill px-2.5 py-0.5 text-white"
                  style={{ fontSize: '0.72rem', borderColor: 'rgba(56, 189, 248, 0.4)' }}
                  onClick={fetchHydroData}
                  disabled={isRefreshing}
                  title="Sinkronkan data hidrologi terkini dari web perusahaan"
                >
                  <i className={`fa-solid fa-arrows-rotate me-1 ${isRefreshing ? 'fa-spin text-warning' : 'text-cyan-300'}`}></i>
                  {isRefreshing ? 'Memuat...' : 'Sinkronkan'}
                </button>
              </div>
            </div>

            {/* Grid 4 Pos Pemantauan Hidrologi Kaskade Citarum */}
            <div className="hydrology-grid">
              {hydroData.stations.map((st) => (
                <div className="hydrology-card" key={st.id}>
                  <div className="hydrology-card-station">
                    <span className="text-truncate">{st.name}</span>
                    <span className="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-1.5 py-0.5" style={{ fontSize: '0.65rem' }}>
                      {st.status}
                    </span>
                  </div>

                  <div className="hydrology-card-tma">
                    <span className="text-white-50 small me-1" style={{ fontSize: '0.72rem' }}>TMA:</span>
                    <span className="hydrology-card-val tabular-nums">{st.tma.toFixed(2)}</span>
                    <span className="hydrology-card-unit">{st.satuanTma}</span>
                  </div>

                  {st.debit && st.debit.length > 0 ? (
                    <div className="hydrology-card-extra text-cyan-200">
                      <div className="d-flex justify-content-between">
                        <span>Q T.Timur: <strong>{st.debit[0]?.nilai} m³/s</strong></span>
                        <span>Q T.Barat: <strong>{st.debit[1]?.nilai} m³/s</strong></span>
                      </div>
                      <div className="text-white-50" style={{ fontSize: '0.68rem' }}>
                        Q T.Utara: <strong>{st.debit[2]?.nilai} m³/s</strong>
                      </div>
                    </div>
                  ) : st.elevasiNormal ? (
                    <div className="hydrology-card-extra text-white-50">
                      Normal: <span className="text-info">{st.elevasiNormal}</span>
                      {st.spillway && (
                        <span> · Spillway: <strong className="text-warning">{st.spillway} m</strong></span>
                      )}
                    </div>
                  ) : (
                    <div className="hydrology-card-extra text-white-50">
                      {st.keterangan}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Brand Info & Main Controls */}
          <div className="row align-items-center g-3">
            {/* Brand Title & Info */}
            <div className="col-lg-7">
              <div className="d-flex align-items-center gap-2 mb-2">
                <span className="badge bg-primary-subtle text-primary border border-primary-subtle px-2.5 py-1 rounded-pill small fw-semibold">
                  <i className="fa-solid fa-water me-1"></i> Pengelolaan Sumber Daya Air &amp; PLTA
                </span>
                <span className="badge bg-slate-100 text-slate-700 border px-2.5 py-1 rounded-pill small fw-medium">
                  ISO 9001:2015 Terverifikasi
                </span>
              </div>
              <h1 className="fw-bold text-dark mb-1 fs-3 tracking-tight">
                SISTEM MANAJEMEN PLTA CURUG
              </h1>
              <div className="d-flex align-items-center gap-2 mb-2">
                <h6 className="fw-bold text-primary mb-0">PERUM JASA TIRTA II</h6>
                <span className="text-muted" style={{ fontSize: '0.8rem' }}>&bull;</span>
                <span className="text-muted small">Wilayah Sungai Citarum, Jawa Barat</span>
              </div>
              <p className="text-secondary small mb-0" style={{ maxWidth: '640px', lineHeight: 1.5 }}>
                Platform pelaporan operasional terintegrasi, standardisasi checklist manuver pindah line 70 kV, dan mitigasi gangguan teknis gardu induk.
              </p>
            </div>

            {/* Quick Metrics & Wallpaper Switcher */}
            <div className="col-lg-5 text-lg-end">
              <div className="d-flex flex-wrap justify-content-lg-end gap-2 mb-2">
                <div className="header-stat-box text-start">
                  <div className="small text-muted" style={{ fontSize: '0.72rem' }}>GANGGUAN TERCATAT</div>
                  <div className="fw-bold text-dark fs-6 tabular-nums">{totalLaporan ?? 0} Kejadian</div>
                </div>
                <div className="header-stat-box text-start">
                  <div className="small text-muted" style={{ fontSize: '0.72rem' }}>DOKUMEN CHECKLIST</div>
                  <div className="fw-bold text-primary fs-6 tabular-nums">{totalChecklist ?? 0} Berkas</div>
                </div>
              </div>

              <div className="d-flex align-items-center justify-content-lg-end gap-2 mt-2">
                <span className="text-muted small tabular-nums" style={{ fontSize: '0.82rem' }}>
                  <i className="fa-regular fa-clock me-1 text-primary"></i>
                  {timeStr}
                </span>

                <button
                  type="button"
                  onClick={onCycleBg}
                  className="btn btn-sm btn-dark rounded-pill px-3 py-1 shadow-sm d-inline-flex align-items-center gap-2"
                  style={{ fontSize: '0.8rem', background: '#0f172a' }}
                  title="Ganti gambar latar belakang kawasan PJT II"
                >
                  <i className="fa-solid fa-image text-info"></i>
                  <span>Latar: <strong>{currentBgName}</strong></span>
                  <i className="fa-solid fa-arrows-rotate ms-1 text-white-50"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
