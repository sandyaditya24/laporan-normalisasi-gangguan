import React from 'react';
import { LaporanBaru, ChecklistArchive } from '../types';
import { generateLaporanBaruPdf, generateChecklistPdf } from '../utils/pdfGenerator';

interface HistoryGangguanProps {
  laporanList: LaporanBaru[];
  checklistList: ChecklistArchive[];
  onClose: () => void;
}

export const HistoryGangguan: React.FC<HistoryGangguanProps> = ({
  laporanList,
  checklistList,
  onClose,
}) => {
  return (
    <div className="card content-card mb-4" id="container-history-gangguan">
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
          <i className="fa-solid fa-clock-rotate-left me-2"></i> HYSTORY GANGGUAN
        </h3>
        <p className="mb-0 text-white-50 small mt-1">
          Daftar riwayat laporan gangguan baru dan checklist normalisasi yang tersimpan
        </p>
      </div>

      <div className="card-body p-4 p-md-5">
        {/* Table 1: Riwayat Laporan Gangguan Baru */}
        <h5 className="fw-bold text-dark mb-3">
          <i className="fa-solid fa-list-check me-2 text-primary"></i> Riwayat Laporan Gangguan Baru
        </h5>
        <div className="table-responsive mb-5">
          <table className="table table-bordered table-hover align-middle bg-white shadow-sm mb-0">
            <thead className="table-dark text-center">
              <tr>
                <th style={{ width: '5%' }}>No</th>
                <th style={{ width: '22%' }}>Jenis Gangguan</th>
                <th style={{ width: '18%' }}>Waktu &amp; Tanggal</th>
                <th style={{ width: '40%' }}>Kronologi</th>
                <th style={{ width: '15%' }}>Aksi</th>
              </tr>
            </thead>
            <tbody>
              {laporanList.length > 0 ? (
                laporanList.map((item, idx) => (
                  <tr key={item.id}>
                    <td className="text-center fw-bold">{idx + 1}</td>
                    <td className="fw-semibold text-danger">{item.jenis}</td>
                    <td className="text-center small">
                      {item.tanggal}
                      <br />
                      <span className="badge bg-light text-dark border mt-1">{item.waktu} WIB</span>
                    </td>
                    <td className="small" style={{ whiteSpace: 'pre-line' }}>
                      {item.kronologi}
                    </td>
                    <td className="text-center">
                      <button
                        type="button"
                        onClick={() => generateLaporanBaruPdf(item)}
                        className="btn btn-sm btn-primary px-3 shadow-sm"
                        title="Unduh PDF Berkas Resmi"
                      >
                        <i className="fa-solid fa-download me-1"></i> PDF
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="text-center text-muted py-4">
                    Belum ada riwayat Laporan Gangguan Baru.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Table 2: Riwayat Checklist & Laporan PDF Tergenerate */}
        <h5 className="fw-bold text-dark mb-3">
          <i className="fa-solid fa-file-pdf me-2 text-danger"></i> Riwayat Checklist &amp; Laporan PDF Tergenerate
        </h5>
        <div className="table-responsive">
          <table className="table table-bordered table-hover align-middle bg-white shadow-sm mb-0">
            <thead className="table-dark text-center">
              <tr>
                <th style={{ width: '8%' }}>No</th>
                <th style={{ width: '52%' }}>Nama File Arsip PDF</th>
                <th style={{ width: '25%' }}>Waktu Pembuatan / Pelaksanaan</th>
                <th style={{ width: '15%' }}>Aksi</th>
              </tr>
            </thead>
            <tbody>
              {checklistList.length > 0 ? (
                checklistList.map((file, idx) => (
                  <tr key={file.id}>
                    <td className="text-center fw-bold">{idx + 1}</td>
                    <td>
                      <i className="fa-solid fa-file-pdf text-danger me-2"></i>
                      <span className="fw-medium">{file.name}</span>
                      <div className="small text-muted mt-1">
                        {file.kategori} &bull; Petugas: {file.namaPetugas || '-'}
                      </div>
                    </td>
                    <td className="text-center text-muted small">{file.date}</td>
                    <td className="text-center">
                      <button
                        type="button"
                        onClick={() => generateChecklistPdf(file)}
                        className="btn btn-sm btn-primary px-3 shadow-sm"
                        title="Unduh Berkas PDF"
                      >
                        <i className="fa-solid fa-download me-1"></i> Unduh
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={4} className="text-center text-muted py-4">
                    Belum ada file PDF checklist tersimpan.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
