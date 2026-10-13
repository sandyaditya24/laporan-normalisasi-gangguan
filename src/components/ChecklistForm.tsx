import React, { useState, useEffect } from 'react';
import { ChecklistArchive, ManualRow } from '../types';
import { generateChecklistPdf } from '../utils/pdfGenerator';

interface ChecklistFormProps {
  onSaveChecklist: (archive: ChecklistArchive) => void;
  onClose: () => void;
  initialSopValue?: string;
  onSopChange?: (sopValue: string) => void;
}

const UNITS = [
  {
    id: 'Gardu Induk Curug',
    title: 'Gardu Induk Curug',
    desc: 'Tegangan Tinggi 70 / 6,3 kV & Distribusi',
    icon: 'fa-solid fa-tower-broadcast',
    color: 'text-primary',
  },
  {
    id: 'Mini Hydro',
    title: 'PLTA Mini Hydro Unit Turbin 2x3400 kW',
    desc: 'Pembangkit Listrik Tenaga Air (Turbin 2x3400 kW)',
    icon: 'fa-solid fa-water',
    color: 'text-info',
  },
  {
    id: 'Pompa Elektrik Tarum Timur',
    title: 'Pompa Elektrik (PETT)',
    desc: 'Pompa Suplesi Irigasi Tarum Timur',
    icon: 'fa-solid fa-gears',
    color: 'text-warning',
  },
];

export const SOP_LIST = [
  {
    id: 'gi-curug',
    code: 'F-20/GI-CRG/01',
    title: 'Checklist Pengamanan Gangguan / Trip GI Curug 70 / 6,3 kV',
    shortTitle: 'Trip GI Curug (70 / 6,3 kV)',
    desc: 'Prosedur pengamanan gangguan relai trip PMT 70 kV, trafo tenaga 500 kVA / 5 MVA, panel 20 kV, 6,3 kV & distribusi 380 V.',
    icon: 'fa-solid fa-bolt-lightning text-warning',
    value: 'CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)',
  },
  {
    id: 'pindah-line-jtl-ksb',
    code: 'F-20/DPL/IK.12-01',
    title: 'Checklist Pindah Line 70 kV: Jatiluhur ke Kosambi (PLN)',
    shortTitle: 'Pindah Line: Jatiluhur ➔ Kosambi',
    desc: 'Manuver pengalihan beban transmisi 70 kV dari Penghantar Jatiluhur ke Penghantar Kosambi (PLN).',
    icon: 'fa-solid fa-arrow-right-arrow-left text-primary',
    value: 'CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV JATILUHUR KE PENGHANTAR 70 KV KOSAMBI (PLN)',
  },
  {
    id: 'pindah-line-ksb-jtl',
    code: 'F-20/DPL/IK.12-02',
    title: 'Checklist Pindah Line 70 kV: Kosambi ke Jatiluhur (PLN)',
    shortTitle: 'Pindah Line: Kosambi ➔ Jatiluhur',
    desc: 'Manuver pengalihan beban transmisi 70 kV dari Penghantar Kosambi ke Penghantar Jatiluhur (PLN). Dilengkapi Bay Kosambi & Bay Jatiluhur.',
    icon: 'fa-solid fa-repeat text-success',
    value: 'CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV KOSAMBI KE PENGHANTAR 70 KV JATILUHUR (PLN)',
    badgeLabel: 'SOP AKTIF IK.12-02',
  },
  {
    id: 'mini-hydro',
    code: 'F-20/DPL/IK.10-01',
    title: 'Checklist Pengoperasian PLTA Mini Hydro Unit Turbin 2x3400 kW Curug',
    shortTitle: 'PLTA Mini Hydro Unit Turbin 2x3400 kW',
    desc: 'Standar pengoperasian unit turbin air 2x3400 kW, pengecekan debit/TMA, tekanan 60/120 bar, control room, & sinkronisasi LGB001JD.',
    icon: 'fa-solid fa-water text-info',
    value: 'CHECK LIST OPERASI PLTA MINI HYDRO CURUG',
  },
  {
    id: 'custom',
    code: 'F-20/CUSTOM',
    title: 'Kustom Jenis Gangguan / Pengoperasian Khusus',
    shortTitle: '+ Tambah / Kustom Gangguan',
    desc: 'Template terbuka untuk pencatatan manuver non-standar, perbaikan darurat, atau pemeliharaan berkala.',
    icon: 'fa-solid fa-sliders text-secondary',
    value: 'custom',
  },
];

export const ChecklistForm: React.FC<ChecklistFormProps> = ({
  onSaveChecklist,
  onClose,
  initialSopValue,
  onSopChange,
}) => {
  const [kategori, setKategori] = useState('Gardu Induk Curug');
  const [mode, setMode] = useState<'manual' | 'otomatis'>('otomatis');
  const [jenisGangguanManual, setJenisGangguanManual] = useState('');
  const [jenisGangguanOtomatis, setJenisGangguanOtomatis] = useState(
    initialSopValue || 'CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)'
  );
  const [customJenisOtomatis, setCustomJenisOtomatis] = useState('');
  const [waktu, setWaktu] = useState(() => {
    const now = new Date();
    const pad = (n: number) => n.toString().padStart(2, '0');
    return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(
      now.getHours()
    )}:${pad(now.getMinutes())}`;
  });
  const [namaGroup, setNamaGroup] = useState('Regu 1 (Piket Siaga)');
  const [namaPetugas, setNamaPetugas] = useState('Saepudin, Ibnu Aulia');

  // Sync if parent updates initialSopValue
  useEffect(() => {
    if (initialSopValue) {
      setJenisGangguanOtomatis(initialSopValue);
      setMode('otomatis');
    }
  }, [initialSopValue]);

  // Manual rows
  const [manualRows, setManualRows] = useState<ManualRow[]>([
    { id: '1', penanganan: 'Pengecekan Relai OCR/GFR & Panel Annunciator', jam: '10:00', status: 'Clear / Tidak ada anomali' },
    { id: '2', penanganan: 'Pelepasan PMT 70 kV dan Pengisolasian Jalur', jam: '10:05', status: 'Posisi Dikeluarkan' },
    { id: '3', penanganan: 'Koordinasi Beban dengan Kontrol Building Jatiluhur', jam: '10:15', status: 'Siap Re-energize' },
  ]);

  // Otomatis items state
  const [otState, setOtState] = useState<Record<string, string>>({
    // GI Curug Defaults
    pos_a1: 'Dikeluarkan',
    pos_a2: 'Dikeluarkan',
    pos_a3: 'Dikeluarkan',
    pos_b1: 'Dikeluarkan',
    pos_b2: 'Dikeluarkan',
    pos_b3: 'Dikeluarkan',
    pos_b4: 'Dikeluarkan',
    pos_b5: 'Clear',
    pos_b6: 'Siap Dimasukan',
    pos_b7: 'Dimasukan',
    pos_b8: 'Dimasukan',
    pos_b9: 'Dimasukan',
    tc_b10: '1',
    pos_b10: 'Dimasukan',
    tc_b11: '1',
    pos_b11: 'Dimasukan',
    pos_b12: 'Clear',
    pos_c1: 'Clear',
    pos_c2: 'Dimasukan',
    pos_c3: 'Dimasukan',
    pos_c4: 'Dimasukan',
    pos_c5: 'Dimasukan',
    pos_c6: 'Dimasukan',
    pos_c7: 'Clear',
    pos_d1: 'Dimasukan',

    // Pindah Line JTL -> KSB
    pos_pl_a1: 'Dikeluarkan',
    pos_pl_a2: 'Dikeluarkan',
    pos_pl_a3: 'Dikeluarkan',
    pos_pl_a4: 'Dikeluarkan',
    pos_pl_a5: 'Dikeluarkan',
    pos_pl_b1: 'Dikeluarkan',
    pos_pl_b2: 'Dikeluarkan',
    pos_pl_b3: 'Dikeluarkan',
    pos_pl_b4: 'Dikeluarkan',
    pos_pl_c1: 'Dikeluarkan',
    pos_pl_c2: 'Tdk. dikeluarkan',
    pos_pl_c3: 'Keluar',
    pos_pl_c4: 'Dikeluarkan',
    pos_pl_c5: 'Keluar',
    pos_pl_d1: 'Keluar',
    pos_pl_d2: 'Masuk',
    pos_pl_d3: 'Keluar',
    pos_pl_d4: 'Dimasukan',
    pos_pl_d5: 'Dimasukan',
    pos_pl_e1: 'Dimasukan',
    pos_pl_e2: 'Dimasukan',
    tc_pl_e3: '1',
    pos_pl_e3: 'Dimasukan',
    tc_pl_e4: '1',
    pos_pl_e4: 'Dimasukan',
    pos_pl_f1: 'Dimasukan',
    pos_pl_f2: 'Dimasukan',
    pos_pl_f3: 'Dimasukan',
    pos_pl_f4: 'Dimasukan',
    pos_pl_f5: 'Dimasukan',

    // Pindah Line KSB -> JTL
    pos_ksb_a1: 'Dikeluarkan',
    pos_ksb_a2: 'Dikeluarkan',
    pos_ksb_a3: 'Dikeluarkan',
    pos_ksb_a4: 'Dikeluarkan',
    pos_ksb_a5: 'Dikeluarkan',
    pos_ksb_b1: 'Dikeluarkan',
    pos_ksb_b2: 'Dikeluarkan',
    pos_ksb_b3: 'Dikeluarkan',
    pos_ksb_b4: 'Dikeluarkan',
    pos_ksb_c1: 'Dikeluarkan',
    pos_ksb_c2: 'Tdk. dikeluarkan',
    pos_ksb_c3: 'Keluar',
    pos_ksb_c4: 'Dikeluarkan',
    pos_ksb_c5: 'Keluar',
    pos_ksb_d1: 'Keluar',
    pos_ksb_d2: 'Masuk',
    pos_ksb_d3: 'Keluar',
    pos_ksb_d4: 'Dimasukan',
    pos_ksb_d5: 'Dimasukan',
    pos_ksb_e1: 'Dimasukan',
    pos_ksb_e2: 'Dimasukan',
    tc_ksb_e3: '1',
    pos_ksb_e3: 'Dimasukan',
    tc_ksb_e4: '1',
    pos_ksb_e4: 'Dimasukan',
    pos_ksb_f1: 'Dimasukan',
    pos_ksb_f2: 'Dimasukan',
    pos_ksb_f3: 'Dimasukan',
    pos_ksb_f4: 'Dimasukan',
    pos_ksb_f5: 'Dimasukan',

    // Mini Hydro
    pos_mh_i1: 'Sudah',
    pos_mh_i2: 'Sudah',
    pos_mh_p1: 'Normal',
    pos_mh_p2: '>= 3 bar',
    pos_mh_p3: '60 bar',
    pos_mh_p4: '120 bar',
    pos_mh_a1: 'Clear / Aman',
    pos_mh_udik: '10.5 m',
    pos_mh_hilir: '2.1 m',
    pos_mh_sampah: 'Bersih',
    pos_mh_a2: 'Normal',
    pos_mh_a3: 'Stabil',
    pos_mh_a4: 'Tutup',
    pos_mh_a5: 'GTA 030 JD',
    pos_mh_a6: 'GTA 031 JS',
    pos_mh_a7: 'LGB 001 JD',
    pos_mh_a8: 'LGB 031 JS',
    pos_mh_a9: 'Ready / Siap',
    pos_mh_b1: 'Normal',
    pos_mh_b2: 'Manual / Auto',
    pos_mh_b3: 'Terkoneksi',
    pos_mh_b4: 'Terkontrol',
    pos_mh_b5: 'Executed',
    ket_mh_b5: 'Tunggu s/d tdk berkedip',
    pos_mh_b6: 'Paralel ON',
    pos_mh_c1: 'Stabil',
  });

  const handleOtChange = (field: string, val: string) => {
    setOtState((prev) => ({ ...prev, [field]: val }));
  };

  const handleSelectSop = (val: string) => {
    setJenisGangguanOtomatis(val);
    setMode('otomatis');
    if (onSopChange) {
      onSopChange(val);
    }
  };

  const handleFillCurrentTime = (prefix: string) => {
    const now = new Date();
    const pad = (n: number) => n.toString().padStart(2, '0');
    const timeNow = `${pad(now.getHours())}:${pad(now.getMinutes())}`;
    setOtState((prev) => {
      const updated = { ...prev };
      Object.keys(prev).forEach((key) => {
        if (key.startsWith(prefix) && key.includes('jam')) {
          updated[key] = timeNow;
        }
      });
      return updated;
    });
  };

  // One-click state cycle helper for fast touch operation
  const cycleState = (key: string, options: string[]) => {
    const current = otState[key] || options[0];
    const currentIndex = options.indexOf(current);
    const nextIndex = (currentIndex + 1) % options.length;
    handleOtChange(key, options[nextIndex]);
  };

  const handleAddManualRow = () => {
    const now = new Date();
    const pad = (n: number) => n.toString().padStart(2, '0');
    const timeNow = `${pad(now.getHours())}:${pad(now.getMinutes())}`;
    setManualRows((prev) => [
      ...prev,
      { id: Date.now().toString(), penanganan: '', jam: timeNow, status: 'Selesai' },
    ]);
  };

  const handleRemoveManualRow = (id: string) => {
    if (manualRows.length > 1) {
      setManualRows((prev) => prev.filter((r) => r.id !== id));
    }
  };

  const handleUpdateManualRow = (
    id: string,
    field: 'penanganan' | 'jam' | 'status',
    val: string
  ) => {
    setManualRows((prev) =>
      prev.map((r) => (r.id === id ? { ...r, [field]: val } : r))
    );
  };

  // Bulletproof detection of Kosambi ke Jatiluhur vs Jatiluhur ke Kosambi
  const isKsbJtl =
    jenisGangguanOtomatis.includes('KOSAMBI KE JATILUHUR') ||
    jenisGangguanOtomatis.includes('KOSAMBI KE PENGHANTAR 70 KV JATILUHUR') ||
    (jenisGangguanOtomatis.includes('KOSAMBI') &&
      jenisGangguanOtomatis.includes('JATILUHUR') &&
      jenisGangguanOtomatis.indexOf('KOSAMBI') < jenisGangguanOtomatis.indexOf('JATILUHUR'));

  const isJtlKsb =
    !isKsbJtl &&
    (jenisGangguanOtomatis.includes('JATILUHUR KE KOSAMBI') ||
      jenisGangguanOtomatis.includes('JATILUHUR KE PENGHANTAR 70 KV KOSAMBI') ||
      (jenisGangguanOtomatis.includes('JATILUHUR') &&
        jenisGangguanOtomatis.includes('KOSAMBI')));

  const isMiniHydro = jenisGangguanOtomatis.includes('MINI HYDRO');
  const isCustom = jenisGangguanOtomatis === 'custom';
  const isGiCurug = !isKsbJtl && !isJtlKsb && !isMiniHydro;

  const buildStructuredOtomatisData = () => {
    if (isJtlKsb || isKsbJtl) {
      const p = isKsbJtl ? 'ksb' : 'pl';
      const cTitle = isKsbJtl ? 'C. PMT KOSAMBI BAY' : 'C. PMT JATILUHUR BAY';
      const dTitle = isKsbJtl ? 'D. PMT JATILUHUR BAY' : 'D. PMT KOSAMBI BAY';

      return {
        sections: [
          {
            title: 'A. RUANG PANEL 6 KV',
            items: [
              { no: 1, uraian: 'PMT/CB panel Trafo 500 KVA / Trafo I', posisi: otState[`pos_${p}_a1`], jam: otState[`jam_${p}_a1`] },
              { no: 2, uraian: 'PMT/CB panel Trafo 500 KVA / Trafo II', posisi: otState[`pos_${p}_a2`], jam: otState[`jam_${p}_a2`] },
              { no: 3, uraian: 'PMT/CB panel keluaran 6 MB2', posisi: otState[`pos_${p}_a3`], jam: otState[`jam_${p}_a3`] },
              { no: 4, uraian: 'PMT/CB panel masukan dari Trafo II', posisi: otState[`pos_${p}_a4`], jam: otState[`jam_${p}_a4`] },
              { no: 5, uraian: 'PMT/CB panel masukan dari Trafo III', posisi: otState[`pos_${p}_a5`], jam: otState[`jam_${p}_a5`] },
            ],
          },
          {
            title: 'B. RUANG PANEL 20 KV BUILDING',
            items: [
              { no: 1, uraian: 'PMT/CB Masukan dari trafo I', posisi: otState[`pos_${p}_b1`], jam: otState[`jam_${p}_b1`] },
              { no: 2, uraian: 'PMT/CB Trafo I 20 / 70 KV 10 MVA', posisi: otState[`pos_${p}_b2`], jam: otState[`jam_${p}_b2`] },
              { no: 3, uraian: 'PMT/CB Trafo II 70 / 6,3 KV 5 MVA', posisi: otState[`pos_${p}_b3`], jam: otState[`jam_${p}_b3`] },
              { no: 4, uraian: 'PMT/CB Trafo III 70 / 6,3 KV 5 MVA', posisi: otState[`pos_${p}_b4`], jam: otState[`jam_${p}_b4`] },
            ],
          },
          {
            title: cTitle,
            items: [
              { no: 1, uraian: 'PMT / CB 70 KV Bay', posisi: otState[`pos_${p}_c1`], jam: otState[`jam_${p}_c1`] },
              { no: 2, uraian: 'PMS / DS Line 70 KV Bay', posisi: otState[`pos_${p}_c2`], jam: otState[`jam_${p}_c2`] },
              { no: 3, uraian: 'PMS / DS Arde Line 70 KV Bay', posisi: otState[`pos_${p}_c3`], jam: otState[`jam_${p}_c3`] },
              { no: 4, uraian: 'PMS / DS Rel 70 KV Bay', posisi: otState[`pos_${p}_c4`], jam: otState[`jam_${p}_c4`] },
              { no: 5, uraian: 'PMS / DS Arde Rel 70 KV Bay', posisi: otState[`pos_${p}_c5`], jam: otState[`jam_${p}_c5`] },
            ],
          },
          {
            title: dTitle,
            items: [
              { no: 1, uraian: 'PMS / DS Arde Line 70 KV Bay', posisi: otState[`pos_${p}_d1`], jam: otState[`jam_${p}_d1`] },
              { no: 2, uraian: 'PMS / DS Line 70 KV Bay', posisi: otState[`pos_${p}_d2`], jam: otState[`jam_${p}_d2`] },
              { no: 3, uraian: 'PMS / DS Arde Rel 70 KV Bay', posisi: otState[`pos_${p}_d3`], jam: otState[`jam_${p}_d3`] },
              { no: 4, uraian: 'PMS / DS Rel 70 KV Bay', posisi: otState[`pos_${p}_d4`], jam: otState[`jam_${p}_d4`] },
              { no: 5, uraian: 'PMT / CB 70 KV Bay', posisi: otState[`pos_${p}_d5`], jam: otState[`jam_${p}_d5`] },
            ],
          },
          {
            title: 'E. RUANG PANEL 20 KV BUILDING (NORMALISASI)',
            items: [
              { no: 1, uraian: 'PMT/CB Trafo I 20 / 70 KV 10 MVA', posisi: otState[`pos_${p}_e1`], jam: otState[`jam_${p}_e1`] },
              { no: 2, uraian: 'PMT/CB Masukan dari trafo I', posisi: otState[`pos_${p}_e2`], jam: otState[`jam_${p}_e2`] },
              { no: 3, uraian: `PMT/CB Trafo II Posisi TC ${otState[`tc_${p}_e3`] || '1'}`, posisi: otState[`pos_${p}_e3`], jam: otState[`jam_${p}_e3`] },
              { no: 4, uraian: `PMT/CB Trafo III Posisi TC ${otState[`tc_${p}_e4`] || '1'}`, posisi: otState[`pos_${p}_e4`], jam: otState[`jam_${p}_e4`] },
            ],
          },
          {
            title: 'F. RUANG PANEL 6 KV (NORMALISASI)',
            items: [
              { no: 1, uraian: 'PMT/CB panel masukan dari Trafo II', posisi: otState[`pos_${p}_f1`], jam: otState[`jam_${p}_f1`] },
              { no: 2, uraian: 'PMT/CB panel masukan dari Trafo III', posisi: otState[`pos_${p}_f2`], jam: otState[`jam_${p}_f2`] },
              { no: 3, uraian: 'PMT/CB panel Trafo 500 KVA / Trafo I', posisi: otState[`pos_${p}_f3`], jam: otState[`jam_${p}_f3`] },
              { no: 4, uraian: 'PMT/CB panel Trafo 500 KVA / Trafo II', posisi: otState[`pos_${p}_f4`], jam: otState[`jam_${p}_f4`] },
              { no: 5, uraian: 'PMT/CB panel keluaran 6 MB2', posisi: otState[`pos_${p}_f5`], jam: otState[`jam_${p}_f5`] },
            ],
          },
        ],
      };
    }

    if (isMiniHydro) {
      return {
        sections: [
          {
            title: 'I. PERSIAPAN',
            items: [
              { no: 1, uraian: 'Koordinasi debit air / TMA dg Operator Bendung Curug Div II', posisi: otState.pos_mh_i1, paraf: otState.paraf_mh_i1 },
              { no: 2, uraian: 'Koordinasi dg Operator Control Building Jatiluhur', posisi: otState.pos_mh_i2, paraf: otState.paraf_mh_i2 },
            ],
          },
          {
            title: 'II & III. PENGECEKAN TEKANAN OPERASIONAL',
            items: [
              { no: 1, uraian: 'Pelaksanaan Pengoperasian Unit Mini Hydro', posisi: otState.pos_mh_p1, paraf: otState.paraf_mh_p1 },
              { no: 2, uraian: 'Pengecekan Air Baku I & II (Tekanan >= 3 bar)', posisi: otState.pos_mh_p2, paraf: otState.paraf_mh_p2 },
              { no: 3, uraian: 'Pengecekan Sudu - Sudu (Tekanan 60 bar)', posisi: otState.pos_mh_p3, paraf: otState.paraf_mh_p3 },
              { no: 4, uraian: 'Pengecekan Down Stream (Tekanan 120 bar)', posisi: otState.pos_mh_p4, paraf: otState.paraf_mh_p4 },
            ],
          },
          {
            title: 'A. RUANG PANEL CONTROL ROOM',
            items: [
              { no: 1, uraian: 'Jendela alarm clear (tidak ada trip)', posisi: otState.pos_mh_a1, jam: otState.jam_mh_a1 },
              { no: 2, uraian: `TMA: Udik ${otState.pos_mh_udik || '-'}, Hilir ${otState.pos_mh_hilir || '-'}, Sampah ${otState.pos_mh_sampah || '-'}`, posisi: otState.pos_mh_a2, jam: otState.jam_mh_a2 },
              { no: 3, uraian: 'Kriteria berhenti stabil / tombol stop', posisi: otState.pos_mh_a3, jam: otState.jam_mh_a3 },
              { no: 4, uraian: 'Posisi Pintu Pembuangan', posisi: otState.pos_mh_a4, jam: otState.jam_mh_a4 },
              { no: 5, uraian: 'Indikasi DS Phase Cubicle', posisi: otState.pos_mh_a5, jam: otState.jam_mh_a5 },
              { no: 6, uraian: 'Indikasi Earthing Switch', posisi: otState.pos_mh_a6, jam: otState.jam_mh_a6 },
              { no: 7, uraian: 'Indikasi CB 20 KV', posisi: otState.pos_mh_a7, jam: otState.jam_mh_a7 },
              { no: 8, uraian: 'Indikasi Earthing Switch LGB 031 JS', posisi: otState.pos_mh_a8, jam: otState.jam_mh_a8 },
              { no: 9, uraian: 'Indikasi Unit Siap Jalan', posisi: otState.pos_mh_a9, jam: otState.jam_mh_a9 },
            ],
          },
          {
            title: 'B. PENGOPERASIAN & SINKRONISASI',
            items: [
              { no: 1, uraian: 'Sistim Pengatur Unit', posisi: otState.pos_mh_b1, paraf: otState.ket_mh_b1 },
              { no: 2, uraian: 'Sistim Komando Unit', posisi: otState.pos_mh_b2, paraf: otState.ket_mh_b2 },
              { no: 3, uraian: 'Sinkronisasi (Portable tool jika manual)', posisi: otState.pos_mh_b3, paraf: otState.ket_mh_b3 },
              { no: 4, uraian: 'Duga Muka Air / Kontrol Water Level', posisi: otState.pos_mh_b4, paraf: otState.ket_mh_b4 },
              { no: 5, uraian: 'Putaran Tanpa Beban -> Eksitasi -> Generator', posisi: otState.pos_mh_b5, paraf: otState.ket_mh_b5 },
              { no: 6, uraian: 'Sinkronisasi Paralel ON (CB LGB001JD ke ON)', posisi: otState.pos_mh_b6, paraf: otState.ket_mh_b6 },
            ],
          },
          {
            title: 'C. PENGATURAN BEBAN',
            items: [
              { no: 1, uraian: 'Pengatur Beban / Frekuensi naik/turun stabil', posisi: otState.pos_mh_c1, paraf: otState.ket_mh_c1 },
            ],
          },
        ],
      };
    }

    // Default: GI Curug 70/6.3 kV
    return {
      sections: [
        {
          title: 'A. RUANG PANEL 6,3 KV',
          items: [
            { no: 1, uraian: 'PMT / CB Panel Trafo 500 KVA / Trafo I', posisi: otState.pos_a1, jam: otState.jam_a1 },
            { no: 2, uraian: 'PMT / CB Panel Trafo 500 KVA / Trafo II', posisi: otState.pos_a2, jam: otState.jam_a2 },
            { no: 3, uraian: 'PMT / CB Panel Keluaran 6 MB2', posisi: otState.pos_a3, jam: otState.jam_a3 },
          ],
        },
        {
          title: 'B. RUANG PANEL 20 KV BUILDING',
          items: [
            { no: 1, uraian: 'PMT / CB Masukan dari Trafo I', posisi: otState.pos_b1, jam: otState.jam_b1 },
            { no: 2, uraian: 'PMT / CB Trafo I 20 / 70 KV 10 MVA', posisi: otState.pos_b2, jam: otState.jam_b2 },
            { no: 3, uraian: 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA', posisi: otState.pos_b3, jam: otState.jam_b3 },
            { no: 4, uraian: 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA', posisi: otState.pos_b4, jam: otState.jam_b4 },
            { no: 5, uraian: 'Riset Semua Gangguan', posisi: otState.pos_b5, jam: otState.jam_b5 },
            { no: 6, uraian: 'Koordinasi dengan Kontrol Building', posisi: otState.pos_b6, jam: otState.jam_b6 },
            { no: 7, uraian: 'PMT / CB Jatiluhur / Kosambi', posisi: otState.pos_b7, jam: otState.jam_b7 },
            { no: 8, uraian: 'PMT / CB Trafo I 20 / 70 KV 10 MVA', posisi: otState.pos_b8, jam: otState.jam_b8 },
            { no: 9, uraian: 'PMT / CB Masukan dari Trafo I', posisi: otState.pos_b9, jam: otState.jam_b9 },
            { no: 10, uraian: `PMT / CB Trafo II 5 MVA Posisi TC ${otState.tc_b10 || '1'}`, posisi: otState.pos_b10, jam: otState.jam_b10 },
            { no: 11, uraian: `PMT / CB Trafo III 5 MVA Posisi TC ${otState.tc_b11 || '1'}`, posisi: otState.pos_b11, jam: otState.jam_b11 },
            { no: 12, uraian: 'Riset Semua Gangguan', posisi: otState.pos_b12, jam: otState.jam_b12 },
          ],
        },
        {
          title: 'C. RUANG PANEL 6 KV',
          items: [
            { no: 1, uraian: 'Riset Semua Gangguan', posisi: otState.pos_c1, jam: otState.jam_c1 },
            { no: 2, uraian: 'PMT / CB Panel Masukan dari Trafo II', posisi: otState.pos_c2, jam: otState.jam_c2 },
            { no: 3, uraian: 'PMT / CB Panel Masukan dari Trafo III', posisi: otState.pos_c3, jam: otState.jam_c3 },
            { no: 4, uraian: 'PMT / CB Panel Trafo 500 KVA / Trafo I', posisi: otState.pos_c4, jam: otState.jam_c4 },
            { no: 5, uraian: 'PMT / CB Panel Trafo 500 KVA / Trafo II', posisi: otState.pos_c5, jam: otState.jam_c5 },
            { no: 6, uraian: 'PMT / CB Panel Keluaran 6 MB2', posisi: otState.pos_c6, jam: otState.jam_c6 },
            { no: 7, uraian: 'Riset Semua Gangguan', posisi: otState.pos_c7, jam: otState.jam_c7 },
          ],
        },
        {
          title: 'D. CB PANEL DISTRIBUSI 380 V AC TARUM BARAT',
          items: [
            { no: 1, uraian: 'PMT / CB Panel Distribusi 380 V AC Tarum Barat', posisi: otState.pos_d1, jam: otState.jam_d1 },
          ],
        },
      ],
    };
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!kategori || !waktu) {
      return;
    }

    const now = new Date();
    const pad = (n: number) => n.toString().padStart(2, '0');
    const timestampStr = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(
      now.getDate()
    )}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
    const pdfName = `Checklist_Normalisasi_${timestampStr}.pdf`;

    const finalJenisGangguan =
      mode === 'manual'
        ? jenisGangguanManual || 'NORMALISASI GANGGUAN'
        : jenisGangguanOtomatis === 'custom'
        ? customJenisOtomatis.trim() || 'CHECK LIST OPERASIONAL GANGGUAN'
        : jenisGangguanOtomatis;

    const formattedManualRows = manualRows.map((r, i) => ({
      no: i + 1,
      penanganan: r.penanganan.trim() || `Item Penanganan ${i + 1}`,
      jam: r.jam.trim() || '-',
      status: r.status.trim() || '-',
    }));

    const archive: ChecklistArchive = {
      id: 'chk-' + Date.now(),
      name: pdfName,
      date: waktu.replace('T', ' Pukul ') + ' WIB',
      kategori,
      jenisGangguan: finalJenisGangguan,
      mode,
      namaGroup: namaGroup.trim(),
      namaPetugas: namaPetugas.trim(),
      manualRows: formattedManualRows,
      otomatisData: mode === 'otomatis' ? buildStructuredOtomatisData() : undefined,
    };

    onSaveChecklist(archive);
    generateChecklistPdf(archive);
  };

  const renderPindahLineTables = (p: 'pl' | 'ksb', title: string, sopCode: string) => {
    const isKsb = p === 'ksb';
    const cBayTitle = isKsb ? 'C. PMT KOSAMBI BAY (PELEPASAN / OPEN)' : 'C. PMT JATILUHUR BAY (PELEPASAN / OPEN)';
    const dBayTitle = isKsb ? 'D. PMT JATILUHUR BAY (PENUTUPAN / CLOSE)' : 'D. PMT KOSAMBI BAY (PENUTUPAN / CLOSE)';
    const bay1Name = isKsb ? 'Kosambi Bay' : 'Jatiluhur Bay';
    const bay2Name = isKsb ? 'Jatiluhur Bay' : 'Kosambi Bay';

    return (
      <div>
        {/* World-Class Header & SOP Badge */}
        <div className="d-flex flex-wrap align-items-center justify-content-between alert alert-primary border border-primary-subtle shadow-sm rounded-4 mb-3 p-3 gap-2">
          <div>
            <div className="d-flex align-items-center gap-2">
              <span className="badge bg-primary text-white rounded-pill px-2.5 py-1 small fw-bold">
                {sopCode}
              </span>
              <span className="small text-primary fw-bold text-uppercase" style={{ letterSpacing: '0.05em' }}>
                Standard Operating Procedure (SOP)
              </span>
            </div>
            <h5 className="fw-bold text-dark mb-0 fs-6 mt-1.5">{title}</h5>
          </div>
          <div className="d-flex align-items-center gap-2">
            <button
              type="button"
              className="btn btn-sm btn-outline-primary bg-white rounded-pill px-3 shadow-xs"
              onClick={() => handleFillCurrentTime(p)}
              title="Isi seluruh kolom jam dengan waktu saat ini"
            >
              <i className="fa-regular fa-clock me-1 text-primary"></i> Isi Jam Sekarang
            </button>
          </div>
        </div>

        {/* Single-Line Circuit Bay Diagram Schematics */}
        <div className="bay-diagram-banner">
          <div className="d-flex align-items-center justify-content-between">
            <span className="small text-white-50 text-uppercase fw-semibold" style={{ letterSpacing: '0.06em' }}>
              <i className="fa-solid fa-diagram-project me-1 text-cyan-400"></i> Diagram Alur Manuver Transmisi 70 kV Curug
            </span>
            <span className="badge bg-slate-800 text-cyan-300 border border-slate-700 small">
              {isKsb ? 'Bay Kosambi ➔ Bay Jatiluhur' : 'Bay Jatiluhur ➔ Bay Kosambi'}
            </span>
          </div>

          <div className="bay-flow">
            <div className="bay-node active-source">
              <div className="bay-node-title">{bay1Name} (Sumber Lama)</div>
              <div className="bay-node-status text-danger">
                <i className="fa-solid fa-lock-open me-1"></i> PMT &amp; PMS Terbuka
              </div>
            </div>

            <div className="bay-arrow">
              <i className="fa-solid fa-right-long"></i>
            </div>

            <div className="bay-node" style={{ borderColor: '#38bdf8', background: 'rgba(56, 189, 248, 0.1)' }}>
              <div className="bay-node-title">Rel Busbar 70 kV</div>
              <div className="bay-node-status text-info">
                <i className="fa-solid fa-bolt me-1"></i> Sinkronisasi Bus
              </div>
            </div>

            <div className="bay-arrow">
              <i className="fa-solid fa-right-long"></i>
            </div>

            <div className="bay-node active-dest">
              <div className="bay-node-title">{bay2Name} (Tujuan Baru)</div>
              <div className="bay-node-status text-success">
                <i className="fa-solid fa-lock me-1"></i> PMT &amp; PMS Dimasukan
              </div>
            </div>
          </div>
        </div>

        {/* A. RUANG PANEL 6 KV */}
        <div className="mb-4">
          <div className="d-flex align-items-center gap-2 mb-2">
            <span className="badge bg-secondary text-white px-2 py-1 rounded">A</span>
            <h6 className="fw-bold text-dark mb-0">RUANG PANEL 6 KV (PELEPASAN / PENYIAPAN)</h6>
          </div>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '45%' }}>Uraian Manuver</th>
                  <th style={{ width: '30%' }}>Keadaan / Posisi</th>
                  <th style={{ width: '20%' }}>Pukul (Jam)</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { no: 1, text: 'PMT/CB panel Trafo 500 KVA / Trafo I', key: `${p}_a1` },
                  { no: 2, text: 'PMT/CB panel Trafo 500 KVA / Trafo II', key: `${p}_a2` },
                  { no: 3, text: 'PMT/CB panel keluaran 6 MB2', key: `${p}_a3` },
                  { no: 4, text: 'PMT/CB panel masukan dari Trafo II', key: `${p}_a4` },
                  { no: 5, text: 'PMT/CB panel masukan dari Trafo III', key: `${p}_a5` },
                ].map((item) => (
                  <tr key={item.key}>
                    <td className="text-center fw-bold">{item.no}</td>
                    <td>{item.text}</td>
                    <td>
                      <div className="d-flex align-items-center gap-1">
                        <input
                          type="text"
                          className="form-control form-control-sm text-center"
                          value={otState[`pos_${item.key}`] || 'Dikeluarkan'}
                          onChange={(e) => handleOtChange(`pos_${item.key}`, e.target.value)}
                        />
                        <button
                          type="button"
                          className="btn btn-xs btn-outline-secondary py-1 px-2 small"
                          title="Ubah posisi cepat"
                          onClick={() => cycleState(`pos_${item.key}`, ['Dikeluarkan', 'Dimasukan', 'Clear'])}
                        >
                          <i className="fa-solid fa-rotate fs-7"></i>
                        </button>
                      </div>
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center tabular-nums"
                        placeholder="WIB"
                        value={otState[`jam_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`jam_${item.key}`, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* B. RUANG PANEL 20 KV BUILDING */}
        <div className="mb-4">
          <div className="d-flex align-items-center gap-2 mb-2">
            <span className="badge bg-secondary text-white px-2 py-1 rounded">B</span>
            <h6 className="fw-bold text-dark mb-0">RUANG PANEL 20 KV BUILDING</h6>
          </div>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '45%' }}>Uraian Manuver</th>
                  <th style={{ width: '30%' }}>Keadaan / Posisi</th>
                  <th style={{ width: '20%' }}>Pukul (Jam)</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { no: 1, text: 'PMT/CB Masukan dari trafo I', key: `${p}_b1` },
                  { no: 2, text: 'PMT/CB Trafo I 20 / 70 KV 10 MVA', key: `${p}_b2` },
                  { no: 3, text: 'PMT/CB Trafo II 70 / 6,3 KV 5 MVA', key: `${p}_b3` },
                  { no: 4, text: 'PMT/CB Trafo III 70 / 6,3 KV 5 MVA', key: `${p}_b4` },
                ].map((item) => (
                  <tr key={item.key}>
                    <td className="text-center fw-bold">{item.no}</td>
                    <td>{item.text}</td>
                    <td>
                      <div className="d-flex align-items-center gap-1">
                        <input
                          type="text"
                          className="form-control form-control-sm text-center"
                          value={otState[`pos_${item.key}`] || 'Dikeluarkan'}
                          onChange={(e) => handleOtChange(`pos_${item.key}`, e.target.value)}
                        />
                        <button
                          type="button"
                          className="btn btn-xs btn-outline-secondary py-1 px-2 small"
                          title="Ubah posisi cepat"
                          onClick={() => cycleState(`pos_${item.key}`, ['Dikeluarkan', 'Dimasukan', 'Clear'])}
                        >
                          <i className="fa-solid fa-rotate fs-7"></i>
                        </button>
                      </div>
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center tabular-nums"
                        placeholder="WIB"
                        value={otState[`jam_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`jam_${item.key}`, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* C. BAY 1 (PELEPASAN) */}
        <div className="mb-4">
          <div className="d-flex align-items-center gap-2 mb-2">
            <span className="badge bg-danger text-white px-2 py-1 rounded">C</span>
            <h6 className="fw-bold text-dark mb-0">{cBayTitle}</h6>
          </div>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '45%' }}>Uraian Saklar / Pemutus</th>
                  <th style={{ width: '30%' }}>Keadaan / Posisi</th>
                  <th style={{ width: '20%' }}>Pukul (Jam)</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { no: 1, text: `PMT / CB 70 KV ${bay1Name}`, key: `${p}_c1`, def: 'Dikeluarkan', opts: ['Dikeluarkan', 'Dimasukan'] },
                  { no: 2, text: `PMS / DS Line 70 KV ${bay1Name}`, key: `${p}_c2`, def: 'Tdk. dikeluarkan', opts: ['Tdk. dikeluarkan', 'Dikeluarkan', 'Dimasukan'] },
                  { no: 3, text: `PMS / DS Arde Line 70 KV ${bay1Name}`, key: `${p}_c3`, def: 'Keluar', opts: ['Keluar', 'Masuk'] },
                  { no: 4, text: `PMS / DS Rel 70 KV ${bay1Name}`, key: `${p}_c4`, def: 'Dikeluarkan', opts: ['Dikeluarkan', 'Dimasukan'] },
                  { no: 5, text: `PMS / DS Arde Rel 70 KV ${bay1Name}`, key: `${p}_c5`, def: 'Keluar', opts: ['Keluar', 'Masuk'] },
                ].map((item) => (
                  <tr key={item.key}>
                    <td className="text-center fw-bold">{item.no}</td>
                    <td>{item.text}</td>
                    <td>
                      <div className="d-flex align-items-center gap-1">
                        <input
                          type="text"
                          className="form-control form-control-sm text-center"
                          value={otState[`pos_${item.key}`] || item.def}
                          onChange={(e) => handleOtChange(`pos_${item.key}`, e.target.value)}
                        />
                        <button
                          type="button"
                          className="btn btn-xs btn-outline-secondary py-1 px-2 small"
                          title="Ubah posisi cepat"
                          onClick={() => cycleState(`pos_${item.key}`, item.opts)}
                        >
                          <i className="fa-solid fa-rotate fs-7"></i>
                        </button>
                      </div>
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center tabular-nums"
                        placeholder="WIB"
                        value={otState[`jam_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`jam_${item.key}`, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* D. BAY 2 (PENUTUPAN) */}
        <div className="mb-4">
          <div className="d-flex align-items-center gap-2 mb-2">
            <span className="badge bg-success text-white px-2 py-1 rounded">D</span>
            <h6 className="fw-bold text-dark mb-0">{dBayTitle}</h6>
          </div>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '45%' }}>Uraian Saklar / Pemutus</th>
                  <th style={{ width: '30%' }}>Keadaan / Posisi</th>
                  <th style={{ width: '20%' }}>Pukul (Jam)</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { no: 1, text: `PMS / DS Arde Line 70 KV ${bay2Name}`, key: `${p}_d1`, def: 'Keluar', opts: ['Keluar', 'Masuk'] },
                  { no: 2, text: `PMS / DS Line 70 KV ${bay2Name}`, key: `${p}_d2`, def: 'Masuk', opts: ['Masuk', 'Keluar'] },
                  { no: 3, text: `PMS / DS Arde Rel 70 KV ${bay2Name}`, key: `${p}_d3`, def: 'Keluar', opts: ['Keluar', 'Masuk'] },
                  { no: 4, text: `PMS / DS Rel 70 KV ${bay2Name}`, key: `${p}_d4`, def: 'Dimasukan', opts: ['Dimasukan', 'Dikeluarkan'] },
                  { no: 5, text: `PMT / CB 70 KV ${bay2Name}`, key: `${p}_d5`, def: 'Dimasukan', opts: ['Dimasukan', 'Dikeluarkan'] },
                ].map((item) => (
                  <tr key={item.key}>
                    <td className="text-center fw-bold">{item.no}</td>
                    <td>{item.text}</td>
                    <td>
                      <div className="d-flex align-items-center gap-1">
                        <input
                          type="text"
                          className="form-control form-control-sm text-center"
                          value={otState[`pos_${item.key}`] || item.def}
                          onChange={(e) => handleOtChange(`pos_${item.key}`, e.target.value)}
                        />
                        <button
                          type="button"
                          className="btn btn-xs btn-outline-secondary py-1 px-2 small"
                          title="Ubah posisi cepat"
                          onClick={() => cycleState(`pos_${item.key}`, item.opts)}
                        >
                          <i className="fa-solid fa-rotate fs-7"></i>
                        </button>
                      </div>
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center tabular-nums"
                        placeholder="WIB"
                        value={otState[`jam_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`jam_${item.key}`, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* E. RUANG PANEL 20 KV BUILDING (NORMALISASI) */}
        <div className="mb-4">
          <div className="d-flex align-items-center gap-2 mb-2">
            <span className="badge bg-primary text-white px-2 py-1 rounded">E</span>
            <h6 className="fw-bold text-dark mb-0">RUANG PANEL 20 KV BUILDING (NORMALISASI)</h6>
          </div>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '45%' }}>Uraian Manuver</th>
                  <th style={{ width: '30%' }}>Keadaan / Posisi</th>
                  <th style={{ width: '20%' }}>Pukul (Jam)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="text-center fw-bold">1</td>
                  <td>PMT/CB Trafo I 20 / 70 KV 10 MVA</td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState[`pos_${p}_e1`] || 'Dimasukan'}
                      onChange={(e) => handleOtChange(`pos_${p}_e1`, e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center tabular-nums"
                      placeholder="WIB"
                      value={otState[`jam_${p}_e1`] || ''}
                      onChange={(e) => handleOtChange(`jam_${p}_e1`, e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <td className="text-center fw-bold">2</td>
                  <td>PMT/CB Masukan dari trafo I</td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState[`pos_${p}_e2`] || 'Dimasukan'}
                      onChange={(e) => handleOtChange(`pos_${p}_e2`, e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center tabular-nums"
                      placeholder="WIB"
                      value={otState[`jam_${p}_e2`] || ''}
                      onChange={(e) => handleOtChange(`jam_${p}_e2`, e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <td className="text-center fw-bold">3</td>
                  <td>
                    PMT/CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC.{' '}
                    <select
                      className="form-select form-select-sm d-inline-block w-auto ms-2"
                      value={otState[`tc_${p}_e3`] || '1'}
                      onChange={(e) => handleOtChange(`tc_${p}_e3`, e.target.value)}
                    >
                      {Array.from({ length: 20 }, (_, i) => i + 1).map((val) => (
                        <option key={val} value={val}>
                          TC {val}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState[`pos_${p}_e3`] || 'Dimasukan'}
                      onChange={(e) => handleOtChange(`pos_${p}_e3`, e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center tabular-nums"
                      placeholder="WIB"
                      value={otState[`jam_${p}_e3`] || ''}
                      onChange={(e) => handleOtChange(`jam_${p}_e3`, e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <td className="text-center fw-bold">4</td>
                  <td>
                    PMT/CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC.{' '}
                    <select
                      className="form-select form-select-sm d-inline-block w-auto ms-2"
                      value={otState[`tc_${p}_e4`] || '1'}
                      onChange={(e) => handleOtChange(`tc_${p}_e4`, e.target.value)}
                    >
                      {Array.from({ length: 20 }, (_, i) => i + 1).map((val) => (
                        <option key={val} value={val}>
                          TC {val}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState[`pos_${p}_e4`] || 'Dimasukan'}
                      onChange={(e) => handleOtChange(`pos_${p}_e4`, e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center tabular-nums"
                      placeholder="WIB"
                      value={otState[`jam_${p}_e4`] || ''}
                      onChange={(e) => handleOtChange(`jam_${p}_e4`, e.target.value)}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* F. RUANG PANEL 6 KV */}
        <div className="mb-4">
          <div className="d-flex align-items-center gap-2 mb-2">
            <span className="badge bg-primary text-white px-2 py-1 rounded">F</span>
            <h6 className="fw-bold text-dark mb-0">RUANG PANEL 6 KV (NORMALISASI)</h6>
          </div>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '45%' }}>Uraian Manuver</th>
                  <th style={{ width: '30%' }}>Keadaan / Posisi</th>
                  <th style={{ width: '20%' }}>Pukul (Jam)</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { no: 1, text: 'PMT/CB panel masukan dari Trafo II', key: `${p}_f1` },
                  { no: 2, text: 'PMT/CB panel masukan dari Trafo III', key: `${p}_f2` },
                  { no: 3, text: 'PMT/CB panel Trafo 500 KVA / Trafo I', key: `${p}_f3` },
                  { no: 4, text: 'PMT/CB panel Trafo 500 KVA / Trafo II', key: `${p}_f4` },
                  { no: 5, text: 'PMT/CB panel keluaran 6 MB2', key: `${p}_f5` },
                ].map((item) => (
                  <tr key={item.key}>
                    <td className="text-center fw-bold">{item.no}</td>
                    <td>{item.text}</td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center"
                        value={otState[`pos_${item.key}`] || 'Dimasukan'}
                        onChange={(e) => handleOtChange(`pos_${item.key}`, e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center tabular-nums"
                        placeholder="WIB"
                        value={otState[`jam_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`jam_${item.key}`, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="p-3 bg-light border rounded-3 mt-3">
          <div className="d-flex align-items-center gap-2">
            <i className="fa-solid fa-circle-info text-primary"></i>
            <span className="fw-bold text-dark small">Instruksi Akhir SOP:</span>
          </div>
          <p className="text-secondary small mb-0 mt-1">
            IV. Melaporkan hasil pelaksanaan manuver (pindah line) ke Kontrol Building Jatiluhur untuk verifikasi sinkronisasi daya transmisi.
          </p>
        </div>
      </div>
    );
  };

  const renderMiniHydroTables = () => {
    return (
      <div>
        <div className="alert alert-info border border-info-subtle shadow-sm rounded-4 text-center mb-4 p-3">
          <div className="small text-info fw-bold text-uppercase" style={{ letterSpacing: '0.05em' }}>
            Standar Pengoperasian Turbin Air 2x3400 kW
          </div>
          <h6 className="fw-bold text-dark mb-0 fs-6 mt-1">
            CHECK LIST OPERASI PLTA MINI HYDRO UNIT TURBIN 2x3400 kW CURUG (F-20/DPL/IK.10-01)
          </h6>
        </div>

        {/* I. PERSIAPAN */}
        <div className="mb-4">
          <h6 className="fw-bold text-dark mb-2">I. PERSIAPAN OPERASIONAL</h6>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '50%' }}>Uraian Kegiatan Persiapan</th>
                  <th style={{ width: '25%' }}>Status / Keterangan</th>
                  <th style={{ width: '20%' }}>Paraf Petugas</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="text-center fw-bold">1</td>
                  <td>Koordinasi debit air / Tinggi Muka air dengan Operator Bendung Curug Divisi II</td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState.pos_mh_i1 || 'Sudah'}
                      onChange={(e) => handleOtChange('pos_mh_i1', e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      placeholder="Paraf"
                      value={otState.paraf_mh_i1 || ''}
                      onChange={(e) => handleOtChange('paraf_mh_i1', e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <td className="text-center fw-bold">2</td>
                  <td>Koordinasi dengan Operator Control Building di Jatiluhur</td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState.pos_mh_i2 || 'Sudah'}
                      onChange={(e) => handleOtChange('pos_mh_i2', e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      placeholder="Paraf"
                      value={otState.paraf_mh_i2 || ''}
                      onChange={(e) => handleOtChange('paraf_mh_i2', e.target.value)}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* II, III, IV, V. PELAKSANAAN & PENGECEKAN TEKANAN */}
        <div className="mb-4">
          <h6 className="fw-bold text-dark mb-2">II, III, IV, V. PENGECEKAN TEKANAN OPERASIONAL</h6>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '50%' }}>Uraian Pengecekan</th>
                  <th style={{ width: '25%' }}>Nilai / Target</th>
                  <th style={{ width: '20%' }}>Paraf Petugas</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { no: 1, text: 'Pelaksanaan Pengoperasian Unit Mini Hydro', key: 'p1', def: 'Normal' },
                  { no: 2, text: 'Pengecekan Air Baku I & II (Tekanan 3 bar / lebih)', key: 'p2', def: '>= 3 bar' },
                  { no: 3, text: 'Pengecekan Sudu - Sudu (Tekanan 60 bar)', key: 'p3', def: '60 bar' },
                  { no: 4, text: 'Pengecekan Down Stream (Tekanan 120 bar)', key: 'p4', def: '120 bar' },
                ].map((item) => (
                  <tr key={item.key}>
                    <td className="text-center fw-bold">{item.no}</td>
                    <td>{item.text}</td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center"
                        value={otState[`pos_mh_${item.key}`] || item.def}
                        onChange={(e) => handleOtChange(`pos_mh_${item.key}`, e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center"
                        placeholder="Paraf"
                        value={otState[`paraf_mh_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`paraf_mh_${item.key}`, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* A. CONTROL ROOM */}
        <div className="mb-4">
          <h6 className="fw-bold text-dark mb-2">A. RUANG PANEL CONTROL ROOM</h6>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '45%' }}>Uraian Indikator</th>
                  <th style={{ width: '25%' }}>Posisi / Isian</th>
                  <th style={{ width: '13%' }}>Paraf</th>
                  <th style={{ width: '12%' }}>Jam</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="text-center fw-bold">1</td>
                  <td>Pada jendela alarm tidak ada indikasi gangguan</td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState.pos_mh_a1 || 'Clear / Aman'}
                      onChange={(e) => handleOtChange('pos_mh_a1', e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      placeholder="Paraf"
                      value={otState.paraf_mh_a1 || ''}
                      onChange={(e) => handleOtChange('paraf_mh_a1', e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center tabular-nums"
                      placeholder="WIB"
                      value={otState.jam_mh_a1 || ''}
                      onChange={(e) => handleOtChange('jam_mh_a1', e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <td className="text-center fw-bold">2</td>
                  <td>
                    Tinggi Muka Air:<br />
                    - Tinggi Udik:{' '}
                    <input
                      type="text"
                      className="form-control form-control-sm d-inline-block mt-1"
                      placeholder="Tinggi Udik"
                      value={otState.pos_mh_udik || ''}
                      onChange={(e) => handleOtChange('pos_mh_udik', e.target.value)}
                    />
                    <br />
                    - Tinggi Hilir:{' '}
                    <input
                      type="text"
                      className="form-control form-control-sm d-inline-block mt-1"
                      placeholder="Tinggi Hilir"
                      value={otState.pos_mh_hilir || ''}
                      onChange={(e) => handleOtChange('pos_mh_hilir', e.target.value)}
                    />
                    <br />
                    - Saring Sampah:{' '}
                    <input
                      type="text"
                      className="form-control form-control-sm d-inline-block mt-1"
                      placeholder="Kondisi Sampah"
                      value={otState.pos_mh_sampah || ''}
                      onChange={(e) => handleOtChange('pos_mh_sampah', e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState.pos_mh_a2 || 'Normal'}
                      onChange={(e) => handleOtChange('pos_mh_a2', e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      placeholder="Paraf"
                      value={otState.paraf_mh_a2 || ''}
                      onChange={(e) => handleOtChange('paraf_mh_a2', e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center tabular-nums"
                      placeholder="WIB"
                      value={otState.jam_mh_a2 || ''}
                      onChange={(e) => handleOtChange('jam_mh_a2', e.target.value)}
                    />
                  </td>
                </tr>
                {[
                  { no: 3, text: 'Kriteria berhenti posisi stabil / tombol stop', key: 'a3', def: 'Stabil' },
                  { no: 4, text: 'Posisi Pintu Pembuangan', key: 'a4', def: 'Tutup' },
                  { no: 5, text: 'Indikasi DS Phase Cubicle', key: 'a5', def: 'GTA 030 JD' },
                  { no: 6, text: 'Indikasi Earthing Switch', key: 'a6', def: 'GTA 031 JS' },
                  { no: 7, text: 'Indikasi CB 20 KV', key: 'a7', def: 'LGB 001 JD' },
                  { no: 8, text: 'Indikasi Earthing Switch LGB 031 JS', key: 'a8', def: 'LGB 031 JS' },
                  { no: 9, text: 'Indikasi Unit Siap Jalan', key: 'a9', def: 'Ready / Siap' },
                ].map((item) => (
                  <tr key={item.key}>
                    <td className="text-center fw-bold">{item.no}</td>
                    <td>{item.text}</td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center"
                        value={otState[`pos_mh_${item.key}`] || item.def}
                        onChange={(e) => handleOtChange(`pos_mh_${item.key}`, e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center"
                        placeholder="Paraf"
                        value={otState[`paraf_mh_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`paraf_mh_${item.key}`, e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center tabular-nums"
                        placeholder="WIB"
                        value={otState[`jam_mh_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`jam_mh_${item.key}`, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* B. CARA PENGOPERASIAN */}
        <div className="mb-4">
          <h6 className="fw-bold text-dark mb-2">B. CARA PENGOPERASIAN &amp; SINKRONISASI</h6>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '50%' }}>Tahapan Pengoperasian / Sinkronisasi</th>
                  <th style={{ width: '25%' }}>Posisi / Status</th>
                  <th style={{ width: '20%' }}>Keterangan / Jam</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { no: 1, text: 'Sistim Pengatur Unit', key: 'b1', def: 'Normal' },
                  { no: 2, text: 'Sistim Komando Unit', key: 'b2', def: 'Manual / Auto' },
                  { no: 3, text: 'Sinkronisasi (Jika manual, hubungkan alat portabel)', key: 'b3', def: 'Terkoneksi' },
                  { no: 4, text: 'Duga Muka Air / Kontrol Water Level', key: 'b4', def: 'Terkontrol' },
                  { no: 5, text: 'Pengoperasian: Putaran Tanpa Beban -> Eksitasi -> Generator', key: 'b5', def: 'Executed', ket: 'Tunggu s/d tdk berkedip' },
                  { no: 6, text: 'Sinkronisasi (Auto/Manual & CB LGB001JD posisi ON)', key: 'b6', def: 'Paralel ON', ket: 'Pukul ... WIB' },
                ].map((item) => (
                  <tr key={item.key}>
                    <td className="text-center fw-bold">{item.no}</td>
                    <td>{item.text}</td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center"
                        value={otState[`pos_mh_${item.key}`] || item.def}
                        onChange={(e) => handleOtChange(`pos_mh_${item.key}`, e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control form-control-sm text-center"
                        placeholder={item.ket || 'Keterangan'}
                        value={otState[`ket_mh_${item.key}`] || ''}
                        onChange={(e) => handleOtChange(`ket_mh_${item.key}`, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* C. PENGATURAN BEBAN */}
        <div className="mb-4">
          <h6 className="fw-bold text-dark mb-2">C. PENGATURAN BEBAN &amp; D. CATATAN RUTIN</h6>
          <div className="table-responsive">
            <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
              <thead className="table-light text-center">
                <tr>
                  <th style={{ width: '5%' }}>No</th>
                  <th style={{ width: '50%' }}>Uraian Pengaturan</th>
                  <th style={{ width: '25%' }}>Target / Posisi</th>
                  <th style={{ width: '20%' }}>Keterangan</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="text-center fw-bold">1</td>
                  <td>Tekan Tombol Pengatur Beban / Frekuensi (naik/turun) hingga stabil</td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      value={otState.pos_mh_c1 || 'Stabil'}
                      onChange={(e) => handleOtChange('pos_mh_c1', e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="form-control form-control-sm text-center"
                      placeholder="Keterangan"
                      value={otState.ket_mh_c1 || ''}
                      onChange={(e) => handleOtChange('ket_mh_c1', e.target.value)}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="card content-card mb-4" id="container-form-laporan">
      <button
        type="button"
        className="btn-close-red-container"
        onClick={onClose}
        title="Tutup Formulir"
      >
        <i className="fa-solid fa-xmark"></i>
      </button>

      <div className="card-header-custom text-white">
        <div className="d-flex align-items-center justify-content-between">
          <div>
            <div className="d-flex align-items-center gap-2 mb-1">
              <span className="badge bg-primary text-white px-2.5 py-0.5 rounded-pill small">SOP PJT II RESMI</span>
              <span className="text-white-50 small">Standardisasi Manuver Gardu Induk &amp; Pembangkit</span>
            </div>
            <h3 className="mb-0 fw-bold fs-4">
              FORM LAPORAN NORMALISASI &amp; CHECKLIST
            </h3>
          </div>
        </div>
      </div>

      <div className="card-body p-4 p-md-5">
        <form onSubmit={handleSubmit}>
          {/* 1. Pilih Kategori / Lokasi Visual Unit Cards */}
          <div className="mb-4">
            <label className="form-label fw-bold text-secondary mb-2">
              1. Pilih Unit / Fasilitas Pembangkit &amp; Gardu:
            </label>
            <div className="row g-3">
              {UNITS.map((u) => {
                const isSelected = kategori === u.id;
                return (
                  <div className="col-md-4" key={u.id}>
                    <div
                      className={`unit-card ${isSelected ? 'active' : ''}`}
                      onClick={() => setKategori(u.id)}
                    >
                      <i className={`${u.icon} ${u.color} fs-3`}></i>
                      <div>
                        <div className="fw-bold text-dark small">{u.title}</div>
                        <div className="text-muted" style={{ fontSize: '0.74rem' }}>{u.desc}</div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 2. Mode Pencatatan Penanganan */}
          <div className="mb-4 p-3 bg-light border rounded-4">
            <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-2">
              <label className="form-label fw-bold text-primary mb-0">
                2. Pilih Mode Pencatatan:
              </label>
              <small className="text-muted">
                {mode === 'otomatis' ? 'Memuat standar prosedur SOP resmi' : 'Pencatatan bebas langkah demi langkah'}
              </small>
            </div>
            <div className="btn-group w-100 shadow-xs rounded-3" role="group">
              <input
                type="radio"
                className="btn-check"
                name="mode_pencatatan"
                id="modeOtomatis"
                checked={mode === 'otomatis'}
                onChange={() => setMode('otomatis')}
              />
              <label className="btn btn-outline-primary btn-custom py-2" htmlFor="modeOtomatis">
                <i className="fa-solid fa-list-check me-2"></i> Mode Otomatis (Standar SOP)
              </label>

              <input
                type="radio"
                className="btn-check"
                name="mode_pencatatan"
                id="modeManual"
                checked={mode === 'manual'}
                onChange={() => setMode('manual')}
              />
              <label className="btn btn-outline-secondary btn-custom py-2" htmlFor="modeManual">
                <i className="fa-solid fa-pen-to-square me-2"></i> Mode Manual (Kustom)
              </label>
            </div>
          </div>

          {/* 3. Input Jenis Gangguan / Pengoperasian (PROMINENT WORLD-CLASS SELECTOR) */}
          {mode === 'manual' ? (
            <div className="mb-4" id="wrapper-jenis-manual">
              <label htmlFor="jenis_gangguan_manual" className="form-label fw-bold text-secondary">
                3. Jenis Gangguan (Manual):
              </label>
              <input
                type="text"
                className="form-control"
                id="jenis_gangguan_manual"
                placeholder="Contoh: Gangguan Trafo / Trip PMT 70 kV Jatiluhur"
                value={jenisGangguanManual}
                onChange={(e) => setJenisGangguanManual(e.target.value)}
              />
            </div>
          ) : (
            <div className="sop-section-container" id="wrapper-jenis-otomatis">
              <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
                <div>
                  <h6 className="fw-bold text-dark mb-0 fs-6">
                    <i className="fa-solid fa-sliders text-primary me-2"></i>
                    3. JENIS GANGGUAN / PENGOPERASIAN (MODE OTOMATIS)
                  </h6>
                  <small className="text-muted">
                    Pilih SOP operasional di bawah ini untuk menampilkan formulir checklist resmi:
                  </small>
                </div>
                <span className="badge bg-primary text-white px-2.5 py-1 rounded-pill small">
                  Wajib Dipilih
                </span>
              </div>

              {/* SOP Interactive Cards Grid */}
              <div className="sop-card-grid mb-3">
                {SOP_LIST.map((sop) => {
                  const isSelected = jenisGangguanOtomatis === sop.value;
                  return (
                    <div
                      key={sop.id}
                      className={`sop-card ${isSelected ? 'active' : ''}`}
                      onClick={() => handleSelectSop(sop.value)}
                    >
                      <div className="sop-card-header">
                        <span className="sop-doc-code">{sop.code}</span>
                        {sop.badgeLabel ? (
                          <span className="badge bg-success text-white small px-2 py-0.5" style={{ fontSize: '0.68rem' }}>
                            {sop.badgeLabel}
                          </span>
                        ) : isSelected ? (
                          <span className="badge bg-primary text-white small px-2 py-0.5" style={{ fontSize: '0.68rem' }}>
                            Terpilih
                          </span>
                        ) : null}
                      </div>
                      <div className="d-flex align-items-start gap-2 mb-1">
                        <i className={`${sop.icon} mt-1 fs-6`}></i>
                        <div className="sop-card-title">{sop.shortTitle}</div>
                      </div>
                      <div className="sop-card-desc">{sop.desc}</div>
                    </div>
                  );
                })}
              </div>

              {/* Secondary Select Dropdown (Synchronized fallback) */}
              <div className="mt-2 pt-2 border-top">
                <div className="d-flex align-items-center justify-content-between mb-1">
                  <label htmlFor="jenis_gangguan_otomatis" className="form-label text-muted small fw-semibold mb-0">
                    Opsi Dropdown Alternatif:
                  </label>
                  <span className="text-muted small" style={{ fontSize: '0.74rem' }}>
                    SOP Aktif: <strong>{isKsbJtl ? 'Pindah Line Kosambi ➔ Jatiluhur' : isJtlKsb ? 'Pindah Line Jatiluhur ➔ Kosambi' : isMiniHydro ? 'PLTA Mini Hydro Unit Turbin 2x3400 kW' : 'GI Curug Trip'}</strong>
                  </span>
                </div>
                <select
                  className="form-select form-select-sm"
                  id="jenis_gangguan_otomatis"
                  name="jenis_gangguan_otomatis"
                  value={jenisGangguanOtomatis}
                  onChange={(e) => handleSelectSop(e.target.value)}
                  required
                >
                  <option value="CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG)">
                    1. CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG) [F-20/GI-CRG/01]
                  </option>
                  <option value="CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV JATILUHUR KE PENGHANTAR 70 KV KOSAMBI (PLN)">
                    2. CHECK LIST PINDAH LINE (JATILUHUR ➔ KOSAMBI) [F-20/DPL/IK.12-01]
                  </option>
                  <option value="CHECK LIST PINDAH LINE / PENGHANTAR 70 KV DARI PENGHANTAR 70 KV KOSAMBI KE PENGHANTAR 70 KV JATILUHUR (PLN)">
                    3. CHECK LIST PINDAH LINE (KOSAMBI ➔ JATILUHUR) [F-20/DPL/IK.12-02] ★ MUNCUL
                  </option>
                  <option value="CHECK LIST OPERASI PLTA MINI HYDRO CURUG">
                    4. CHECK LIST OPERASI PLTA MINI HYDRO CURUG [F-20/DPL/IK.10-01]
                  </option>
                  <option value="custom">
                    5. + Tambah / Kustom Jenis Gangguan/Pengoperasian Lainnya...
                  </option>
                </select>
              </div>

              {isCustom && (
                <div className="mt-3 p-3 bg-white border border-primary-subtle rounded-3">
                  <label htmlFor="custom_jenis_otomatis" className="form-label fw-bold text-primary">
                    Tuliskan Nama Jenis Gangguan / Pengoperasian Baru:
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="custom_jenis_otomatis"
                    placeholder="Contoh: CHECK LIST PEMELIHARAAN TRAFO 20/70 KV & BAY TRANSMISI"
                    value={customJenisOtomatis}
                    onChange={(e) => setCustomJenisOtomatis(e.target.value)}
                    required
                  />
                </div>
              )}
            </div>
          )}

          {/* 4. Waktu */}
          <div className="mb-4">
            <label htmlFor="waktu" className="form-label fw-bold text-secondary">
              4. Tanggal &amp; Jam Kejadian / Pelaksanaan:
            </label>
            <input
              type="datetime-local"
              className="form-control tabular-nums"
              id="waktu"
              value={waktu}
              onChange={(e) => setWaktu(e.target.value)}
              required
            />
          </div>

          <hr className="my-4" />

          {/* SECTION MANUAL */}
          {mode === 'manual' && (
            <div className="mb-4" id="section-manual">
              <div className="d-flex align-items-center justify-content-between mb-2">
                <label className="form-label fw-bold text-primary mb-0">
                  Daftar Penanganan Gangguan, Jam &amp; Status (Manual):
                </label>
                <button
                  type="button"
                  className="btn btn-outline-primary btn-sm rounded-pill px-3"
                  onClick={handleAddManualRow}
                >
                  <i className="fa-solid fa-plus me-1"></i> Tambah Baris
                </button>
              </div>

              <div id="penanganan-container">
                {manualRows.map((row, idx) => (
                  <div className="row g-2 mb-2 align-items-center penanganan-row" key={row.id}>
                    <div className="col-md-1">
                      <input
                        type="text"
                        className="form-control text-center bg-light fw-bold"
                        value={idx + 1}
                        readOnly
                      />
                    </div>
                    <div className="col-md-5">
                      <input
                        type="text"
                        className="form-control"
                        placeholder="Jenis Penanganan"
                        value={row.penanganan}
                        onChange={(e) =>
                          handleUpdateManualRow(row.id, 'penanganan', e.target.value)
                        }
                      />
                    </div>
                    <div className="col-md-2">
                      <input
                        type="text"
                        className="form-control text-center tabular-nums"
                        placeholder="Jam (10:00)"
                        value={row.jam}
                        onChange={(e) =>
                          handleUpdateManualRow(row.id, 'jam', e.target.value)
                        }
                      />
                    </div>
                    <div className="col-md-3">
                      <input
                        type="text"
                        className="form-control text-center"
                        placeholder="Status Tindakan"
                        value={row.status}
                        onChange={(e) =>
                          handleUpdateManualRow(row.id, 'status', e.target.value)
                        }
                      />
                    </div>
                    <div className="col-md-1">
                      <button
                        type="button"
                        className="btn btn-outline-danger w-100"
                        onClick={() => handleRemoveManualRow(row.id)}
                        disabled={manualRows.length === 1}
                        title="Hapus baris"
                      >
                        <i className="fa-solid fa-trash"></i>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* SECTION OTOMATIS */}
          {mode === 'otomatis' && (
            <div className="mb-4" id="section-otomatis">
              {/* 1. GI Curug Trip / Custom */}
              {isGiCurug && (
                <div>
                  <div className="alert alert-warning border border-warning-subtle shadow-sm rounded-4 text-center mb-4 p-3">
                    <div className="small text-warning-emphasis fw-bold text-uppercase">
                      Prosedur Standar Gardu Induk Curug
                    </div>
                    <h6 className="fw-bold text-dark mb-0 fs-6 mt-1">
                      {isCustom
                        ? customJenisOtomatis || 'CHECK LIST OPERASIONAL GANGGUAN'
                        : 'CHECK LIST PENGAMANAN GANGGUAN / TRIP (GARDU INDUK 70 / 6,3 KV CURUG) [F-20/GI-CRG/01]'}
                    </h6>
                  </div>

                  {/* A. RUANG PANEL 6,3 KV */}
                  <div className="mb-4">
                    <h6 className="fw-bold text-dark mb-2">A. RUANG PANEL 6,3 KV</h6>
                    <div className="table-responsive">
                      <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
                        <thead className="table-light text-center">
                          <tr>
                            <th style={{ width: '5%' }}>No</th>
                            <th style={{ width: '48%' }}>Uraian</th>
                            <th style={{ width: '27%' }}>Keadaan / Posisi</th>
                            <th style={{ width: '20%' }}>Pukul (Jam)</th>
                          </tr>
                        </thead>
                        <tbody>
                          {[
                            { no: 1, text: 'PMT / CB Panel Trafo 500 KVA / Trafo I', key: 'a1' },
                            { no: 2, text: 'PMT / CB Panel Trafo 500 KVA / Trafo II', key: 'a2' },
                            { no: 3, text: 'PMT / CB Panel Keluaran 6 MB2', key: 'a3' },
                          ].map((item) => (
                            <tr key={item.key}>
                              <td className="text-center fw-bold">{item.no}</td>
                              <td>{item.text}</td>
                              <td>
                                <input
                                  type="text"
                                  className="form-control form-control-sm text-center"
                                  value={otState[`pos_${item.key}`] || 'Dikeluarkan'}
                                  onChange={(e) => handleOtChange(`pos_${item.key}`, e.target.value)}
                                />
                              </td>
                              <td>
                                <input
                                  type="text"
                                  className="form-control form-control-sm text-center tabular-nums"
                                  placeholder="WIB"
                                  value={otState[`jam_${item.key}`] || ''}
                                  onChange={(e) => handleOtChange(`jam_${item.key}`, e.target.value)}
                                />
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* B. RUANG PANEL 20 KV BUILDING */}
                  <div className="mb-4">
                    <h6 className="fw-bold text-dark mb-2">B. RUANG PANEL 20 KV BUILDING</h6>
                    <div className="table-responsive">
                      <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
                        <thead className="table-light text-center">
                          <tr>
                            <th style={{ width: '5%' }}>No</th>
                            <th style={{ width: '48%' }}>Uraian</th>
                            <th style={{ width: '27%' }}>Keadaan / Posisi</th>
                            <th style={{ width: '20%' }}>Pukul (Jam)</th>
                          </tr>
                        </thead>
                        <tbody>
                          {[
                            { no: 1, text: 'PMT / CB Masukan dari Trafo I', key: 'b1' },
                            { no: 2, text: 'PMT / CB Trafo I 20 / 70 KV 10 MVA', key: 'b2' },
                            { no: 3, text: 'PMT / CB Trafo II 70 / 6,3 KV 5 MVA', key: 'b3' },
                            { no: 4, text: 'PMT / CB Trafo III 70 / 6,3 KV 5 MVA', key: 'b4' },
                            { no: 5, text: 'Riset Semua Gangguan', key: 'b5' },
                            { no: 6, text: 'Koordinasi dengan Kontrol Building', key: 'b6' },
                            { no: 7, text: 'PMT / CB Jatiluhur / Kosambi', key: 'b7' },
                            { no: 8, text: 'PMT / CB Trafo I 20 / 70 KV 10 MVA', key: 'b8' },
                            { no: 9, text: 'PMT / CB Masukan dari Trafo I', key: 'b9' },
                          ].map((item) => (
                            <tr key={item.key}>
                              <td className="text-center fw-bold">{item.no}</td>
                              <td>{item.text}</td>
                              <td>
                                <input
                                  type="text"
                                  className="form-control form-control-sm text-center"
                                  value={otState[`pos_${item.key}`] || 'Dimasukan'}
                                  onChange={(e) => handleOtChange(`pos_${item.key}`, e.target.value)}
                                />
                              </td>
                              <td>
                                <input
                                  type="text"
                                  className="form-control form-control-sm text-center tabular-nums"
                                  placeholder="WIB"
                                  value={otState[`jam_${item.key}`] || ''}
                                  onChange={(e) => handleOtChange(`jam_${item.key}`, e.target.value)}
                                />
                              </td>
                            </tr>
                          ))}
                          <tr>
                            <td className="text-center fw-bold">10</td>
                            <td>
                              PMT / CB Trafo II 70 / 6,3 KV 5 MVA Posisi TC.{' '}
                              <select
                                className="form-select form-select-sm d-inline-block w-auto ms-2"
                                value={otState.tc_b10 || '1'}
                                onChange={(e) => handleOtChange('tc_b10', e.target.value)}
                              >
                                {Array.from({ length: 20 }, (_, i) => i + 1).map((val) => (
                                  <option key={val} value={val}>
                                    TC {val}
                                  </option>
                                ))}
                              </select>
                            </td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm text-center"
                                value={otState.pos_b10 || 'Dimasukan'}
                                onChange={(e) => handleOtChange('pos_b10', e.target.value)}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm text-center tabular-nums"
                                value={otState.jam_b10 || ''}
                                onChange={(e) => handleOtChange('jam_b10', e.target.value)}
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="text-center fw-bold">11</td>
                            <td>
                              PMT / CB Trafo III 70 / 6,3 KV 5 MVA Posisi TC.{' '}
                              <select
                                className="form-select form-select-sm d-inline-block w-auto ms-2"
                                value={otState.tc_b11 || '1'}
                                onChange={(e) => handleOtChange('tc_b11', e.target.value)}
                              >
                                {Array.from({ length: 20 }, (_, i) => i + 1).map((val) => (
                                  <option key={val} value={val}>
                                    TC {val}
                                  </option>
                                ))}
                              </select>
                            </td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm text-center"
                                value={otState.pos_b11 || 'Dimasukan'}
                                onChange={(e) => handleOtChange('pos_b11', e.target.value)}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm text-center tabular-nums"
                                value={otState.jam_b11 || ''}
                                onChange={(e) => handleOtChange('jam_b11', e.target.value)}
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="text-center fw-bold">12</td>
                            <td>Riset Semua Gangguan</td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm text-center"
                                value={otState.pos_b12 || 'Clear'}
                                onChange={(e) => handleOtChange('pos_b12', e.target.value)}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm text-center tabular-nums"
                                value={otState.jam_b12 || ''}
                                onChange={(e) => handleOtChange('jam_b12', e.target.value)}
                              />
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* C. RUANG PANEL 6 KV */}
                  <div className="mb-4">
                    <h6 className="fw-bold text-dark mb-2">C. RUANG PANEL 6 KV</h6>
                    <div className="table-responsive">
                      <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
                        <thead className="table-light text-center">
                          <tr>
                            <th style={{ width: '5%' }}>No</th>
                            <th style={{ width: '48%' }}>Uraian</th>
                            <th style={{ width: '27%' }}>Keadaan / Posisi</th>
                            <th style={{ width: '20%' }}>Pukul (Jam)</th>
                          </tr>
                        </thead>
                        <tbody>
                          {[
                            { no: 1, text: 'Riset Semua Gangguan', key: 'c1' },
                            { no: 2, text: 'PMT / CB Panel Masukan dari Trafo II', key: 'c2' },
                            { no: 3, text: 'PMT / CB Panel Masukan dari Trafo III', key: 'c3' },
                            { no: 4, text: 'PMT / CB Panel Trafo 500 KVA / Trafo I', key: 'c4' },
                            { no: 5, text: 'PMT / CB Panel Trafo 500 KVA / Trafo II', key: 'c5' },
                            { no: 6, text: 'PMT / CB Panel Keluaran 6 MB2', key: 'c6' },
                            { no: 7, text: 'Riset Semua Gangguan', key: 'c7' },
                          ].map((item) => (
                            <tr key={item.key}>
                              <td className="text-center fw-bold">{item.no}</td>
                              <td>{item.text}</td>
                              <td>
                                <input
                                  type="text"
                                  className="form-control form-control-sm text-center"
                                  value={otState[`pos_${item.key}`] || 'Dimasukan'}
                                  onChange={(e) => handleOtChange(`pos_${item.key}`, e.target.value)}
                                />
                              </td>
                              <td>
                                <input
                                  type="text"
                                  className="form-control form-control-sm text-center tabular-nums"
                                  placeholder="WIB"
                                  value={otState[`jam_${item.key}`] || ''}
                                  onChange={(e) => handleOtChange(`jam_${item.key}`, e.target.value)}
                                />
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* D. CB PANEL DISTRIBUSI */}
                  <div className="mb-4">
                    <h6 className="fw-bold text-dark mb-2">D. CB PANEL DISTRIBUSI 380 V AC TARUM BARAT</h6>
                    <div className="table-responsive">
                      <table className="table table-bordered table-sm bg-white align-middle shadow-xs mb-0 table-hover">
                        <thead className="table-light text-center">
                          <tr>
                            <th style={{ width: '5%' }}>No</th>
                            <th style={{ width: '48%' }}>Uraian</th>
                            <th style={{ width: '27%' }}>Keadaan / Posisi</th>
                            <th style={{ width: '20%' }}>Pukul (Jam)</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td className="text-center fw-bold">1</td>
                            <td>PMT / CB Panel Distribusi 380 V AC Tarum Barat</td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm text-center"
                                value={otState.pos_d1 || 'Dimasukan'}
                                onChange={(e) => handleOtChange('pos_d1', e.target.value)}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm text-center tabular-nums"
                                placeholder="WIB"
                                value={otState.jam_d1 || ''}
                                onChange={(e) => handleOtChange('jam_d1', e.target.value)}
                              />
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}

              {/* 2. Pindah Line Jatiluhur -> Kosambi */}
              {isJtlKsb &&
                renderPindahLineTables(
                  'pl',
                  'CHECK LIST PINDAH LINE 70 KV DARI JATILUHUR KE KOSAMBI (PLN)',
                  'SOP F-20/DPL/IK.12-01'
                )}

              {/* 3. Pindah Line Kosambi -> Jatiluhur (Specifically requested!) */}
              {isKsbJtl &&
                renderPindahLineTables(
                  'ksb',
                  'CHECK LIST PINDAH LINE 70 KV DARI KOSAMBI KE JATILUHUR (PLN)',
                  'SOP F-20/DPL/IK.12-02'
                )}

              {/* 4. Mini Hydro */}
              {isMiniHydro && renderMiniHydroTables()}
            </div>
          )}

          <hr className="my-4" />

          {/* Form Informasi Pembuat Laporan & Pengesahan */}
          <div className="card p-4 mb-4 bg-light border-0 shadow-xs rounded-4">
            <h6 className="fw-bold text-dark mb-3">
              <i className="fa-solid fa-user-check me-2 text-primary"></i> Pengesahan Regu &amp; Petugas Pelaksana
            </h6>
            <div className="row g-3">
              <div className="col-md-4">
                <label htmlFor="nama_group" className="form-label fw-bold text-secondary small">
                  Group / Regu Piket:
                </label>
                <input
                  type="text"
                  className="form-control bg-white"
                  id="nama_group"
                  placeholder="Contoh: Regu 1 / Piket Siaga"
                  value={namaGroup}
                  onChange={(e) => setNamaGroup(e.target.value)}
                  required
                />
              </div>
              <div className="col-md-8">
                <label htmlFor="nama_petugas" className="form-label fw-bold text-secondary small">
                  Nama Petugas Yang Melaksanakan:
                </label>
                <input
                  type="text"
                  className="form-control bg-white"
                  id="nama_petugas"
                  placeholder="Contoh: Saepudin, Ibnu Aulia, Willy Wiriawan"
                  value={namaPetugas}
                  onChange={(e) => setNamaPetugas(e.target.value)}
                  required
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary w-100 py-3 shadow-sm fs-5 btn-custom"
          >
            <i className="fa-solid fa-file-pdf me-2"></i> Buat Laporan PDF Checklist Sekarang
          </button>
        </form>
      </div>
    </div>
  );
};
