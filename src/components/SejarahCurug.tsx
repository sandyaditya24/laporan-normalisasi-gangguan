import React, { useState } from 'react';

interface SejarahCurugProps {
  onClose: () => void;
}

export const SejarahCurug: React.FC<SejarahCurugProps> = ({ onClose }) => {
  const [imageVisible, setImageVisible] = useState(true);

  return (
    <div className="card content-card mb-4" id="container-sejarah">
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
          <i className="fa-solid fa-landmark me-2"></i> SEJARAH BENDUNG CURUG &amp; PENGEMBANGANNYA
        </h3>
        <p className="mb-0 text-white-50 small mt-1">
          Perum Jasa Tirta II - Perjalanan Infrastruktur Pengairan &amp; Kelistrikan di Jawa Barat
        </p>
      </div>

      <div className="card-body p-4 p-md-5">
        <div className="row align-items-center mb-4 g-4">
          <div className={imageVisible ? 'col-md-7' : 'col-md-12'}>
            <h4 className="fw-bold text-dark mb-3">Awal Mula Pembangunan</h4>
            <p className="text-muted" style={{ textAlign: 'justify', lineHeight: 1.8 }}>
              Bendung Curug memiliki peranan yang sangat vital dalam sejarah pengelolaan sumber daya air dan kelistrikan di Indonesia, khususnya di Jawa Barat. Pembangunan kompleks pengairan di kawasan Curug (Kecamatan Klari / Ciampel, Karawang) tidak dapat dilepaskan dari sejarah besar proyek irigasi Jatiluhur (Waduk Ir. H. Djuanda). Bendung Curug berfungsi sebagai pengatur pembagian air utama yang mengalirkan air dari Sungai Citarum ke Saluran Induk Tarum Barat dan Tarum Timur.
            </p>
            <p className="text-muted" style={{ textAlign: 'justify', lineHeight: 1.8 }}>
              Saluran Induk Tarum Barat membawa pasokan air baku vital menuju DKI Jakarta dan kawasan industri Bekasi-Karawang, sedangkan Saluran Induk Tarum Timur dan Pompa Elektrik Tarum Timur (PETT) mengairi ratusan ribu hektar sawah lumbung padi nasional di Kabupaten Karawang, Subang, dan Indramayu.
            </p>
            <p className="text-muted" style={{ textAlign: 'justify', lineHeight: 1.8 }}>
              Seiring modernisasi energi bersih dan terbarukan, kompleks Bendung Curug dilengkapi dengan pembangkit tenaga air (PLTA Mini Hydro Unit Turbin 2x3400 kW) dan Gardu Induk 70 / 6,3 kV yang menyalurkan energi andal ke sistem kelistrikan terhubung Jatiluhur dan Kosambi.
            </p>
            {!imageVisible && (
              <button
                type="button"
                className="btn btn-outline-primary btn-sm mt-2 rounded-pill"
                onClick={() => setImageVisible(true)}
              >
                <i className="fa-solid fa-image me-1"></i> Tampilkan Foto Dokumentasi Historis
              </button>
            )}
          </div>

          {imageVisible && (
            <div className="col-md-5 text-center">
              <div
                id="imageWrapper"
                className="closable-image-wrapper border shadow-sm rounded-4 position-relative d-inline-block"
              >
                <button
                  type="button"
                  className="btn-close-img"
                  onClick={() => setImageVisible(false)}
                  title="Sembunyikan Gambar"
                >
                  <i className="fa-solid fa-xmark"></i>
                </button>
                <img
                  src="/static/CURUGTEMPODULU.jpg"
                  alt="Bendung Curug Tempo Dulu"
                  className="img-fluid rounded-4 shadow-sm"
                  id="targetImage"
                  style={{ maxHeight: '280px', objectFit: 'cover' }}
                  onError={(e) => {
                    // Fallback to Unsplash vintage dam photo if local file is missing
                    (e.target as HTMLImageElement).src =
                      'https://images.unsplash.com/photo-1574958269340-fa927503f3dd?auto=format&fit=crop&w=800&q=80';
                  }}
                />
              </div>
              <small className="d-block text-muted mt-2 fst-italic" id="imageCaption">
                Dokumentasi historis kawasan Bendung Curug.
              </small>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
