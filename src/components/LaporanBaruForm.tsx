import React, { useState } from 'react';
import { LaporanBaru } from '../types';
import { generateLaporanBaruPdf } from '../utils/pdfGenerator';

interface LaporanBaruFormProps {
  onSaveLaporan: (laporan: LaporanBaru) => void;
  onClose: () => void;
}

export const LaporanBaruForm: React.FC<LaporanBaruFormProps> = ({
  onSaveLaporan,
  onClose,
}) => {
  const [jenis, setJenis] = useState('');
  const [waktu, setWaktu] = useState('');
  const [tanggal, setTanggal] = useState('');
  const [kronologi, setKronologi] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!jenis.trim() || !waktu.trim() || !tanggal.trim() || !kronologi.trim()) {
      return;
    }

    const now = new Date();
    const pad = (n: number) => n.toString().padStart(2, '0');
    const timestampStr = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(
      now.getDate()
    )}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
    const pdfName = `Laporan_Gangguan_Baru_${timestampStr}.pdf`;

    const newLaporan: LaporanBaru = {
      id: 'lap-' + Date.now(),
      jenis: jenis.trim(),
      tanggal: tanggal.trim(),
      waktu: waktu.trim(),
      kronologi: kronologi.trim(),
      pdf_name: pdfName,
      createdAt: now.toLocaleString('id-ID'),
    };

    onSaveLaporan(newLaporan);
    generateLaporanBaruPdf(newLaporan);

    // Reset form
    setJenis('');
    setWaktu('');
    setTanggal('');
    setKronologi('');
  };

  return (
    <div className="card content-card mb-4" id="container-buat-laporan-baru">
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
          <i className="fa-solid fa-file-circle-plus me-2"></i> BUAT LAPORAN GANGGUAN BARU
        </h3>
        <p className="mb-0 text-white-50 small mt-1">
          Formulir pencatatan kronologi dan detail gangguan operasional
        </p>
      </div>
      <div className="card-body p-4 p-md-5">
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="baru_jenis_gangguan"
              className="form-label fw-bold text-secondary"
            >
              Jenis Gangguan:
            </label>
            <input
              type="text"
              className="form-control"
              id="baru_jenis_gangguan"
              value={jenis}
              onChange={(e) => setJenis(e.target.value)}
              placeholder="Contoh: Gangguan Trafo Utama / Trip PMT 70 kV"
              required
            />
          </div>

          <div className="row g-3 mb-4">
            <div className="col-md-4">
              <label htmlFor="baru_waktu" className="form-label fw-bold text-secondary">
                Waktu Gangguan (Jam):
              </label>
              <input
                type="time"
                className="form-control"
                id="baru_waktu"
                value={waktu}
                onChange={(e) => setWaktu(e.target.value)}
                required
              />
            </div>
            <div className="col-md-8">
              <label
                htmlFor="baru_tanggal_lengkap"
                className="form-label fw-bold text-secondary"
              >
                Tanggal, Bulan, dan Tahun Gangguan:
              </label>
              <input
                type="date"
                className="form-control"
                id="baru_tanggal_lengkap"
                value={tanggal}
                onChange={(e) => setTanggal(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-4">
            <label
              htmlFor="baru_kronologi"
              className="form-label fw-bold text-secondary"
            >
              Kronologi Gangguan:
            </label>
            <textarea
              className="form-control"
              id="baru_kronologi"
              rows={5}
              value={kronologi}
              onChange={(e) => setKronologi(e.target.value)}
              placeholder="Jelaskan kronologi kejadian secara detail..."
              required
            ></textarea>
          </div>

          <button
            type="submit"
            className="btn btn-primary w-100 py-3 shadow-sm fs-5 btn-custom"
          >
            <i className="fa-solid fa-paper-plane me-2"></i> Simpan &amp; Catat Laporan Gangguan
          </button>
        </form>
      </div>
    </div>
  );
};
