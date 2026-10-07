from flask import Blueprint, render_template_string

# Membuat Blueprint untuk modul Pegawai
pegawai_bp = Blueprint('pegawai', __name__)

# Template HTML khusus untuk bagian Struktural Pegawai (Pemisahan Operasional & Pemeliharaan)
PEGAWAI_SECTION_TEMPLATE = """
<style>
    .power-plant-container {
        background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%);
        border-radius: 16px;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }
    .power-plant-container::before {
        content: "⚡ 💧 ⚡";
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 1.5rem;
        opacity: 0.2;
        letter-spacing: 10px;
    }
    .tree-grid {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        overflow-x: auto;
        padding: 10px 0;
    }
    .plant-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 15px 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
        min-width: 280px;
        max-width: 320px;
        position: relative;
        margin: 12px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .plant-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.15);
    }
    .card-puncak {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        color: white;
        border: 2px solid #38bdf8;
    }
    .card-manajemen {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border-color: #3b82f6;
    }
    .card-operasional {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border-color: #22c55e;
    }
    .card-pemeliharaan {
        background: linear-gradient(135deg, #fefce8, #fef9c3);
        border-color: #eab308;
    }
    .plant-level {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 25px;
        width: 100%;
        margin-top: 15px;
    }
    .connector-line {
        width: 3px;
        height: 25px;
        background: #cbd5e1;
        margin: 0 auto;
        border-radius: 2px;
    }
    .badge-icon {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .badge-puncak { background: #38bdf8; color: #0f172a; }
    .badge-manajemen { background: #2563eb; color: #ffffff; }
    .badge-operasional { background: #16a34a; color: #ffffff; }
    .badge-pemeliharaan { background: #ca8a04; color: #ffffff; }
    
    .team-badge {
        font-size: 0.75rem;
        background: rgba(0,0,0,0.04);
        padding: 6px 10px;
        border-radius: 8px;
        color: #334155;
        margin-top: 8px;
        display: block;
        text-align: left;
        border-left: 3px solid #3b82f6;
    }
    .section-title-tag {
        font-size: 1rem;
        font-weight: 800;
        padding: 8px 16px;
        border-radius: 8px;
        margin: 20px 0 10px 0;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
</style>

<div class="card content-card mb-4" id="container-struktural-pegawai" style="display: none;">
    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
        <i class="fa-solid fa-xmark"></i>
    </button>
    <div class="card-header-custom text-white text-center">
        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-bolt me-2 text-warning"></i> STRUKTURAL PEMBANGKIT & GARDU INDUK PLTA CURUG</h3>
        <p class="mb-0 text-white-50 small mt-1">Pemisahan Jalur Operasional & Pemeliharaan — Perum Jasa Tirta II</p>
    </div>
    <div class="card-body p-4 p-md-4 power-plant-container">
        <div class="tree-grid">
            
            <!-- LEVEL 1: PIMPINAN PUNCAK -->
            <div class="plant-card card-puncak">
                <span class="badge-icon badge-puncak"><i class="fa-solid fa-crown me-1"></i> Pusat Kendali Utama</span>
                <h5 class="fw-bold mb-1 text-white">BUDIYO, ST</h5>
                <p class="small text-white-50 mb-0">General Manajer PLTA</p>
            </div>

            <div class="connector-line"></div>

            <!-- LEVEL 2: MANAJEMEN OPERASIONAL JARINGAN -->
            <div class="plant-level">
                <div class="plant-card card-manajemen">
                    <span class="badge-icon badge-manajemen"><i class="fa-solid fa-network-wired me-1"></i> Pimpinan Sektor</span>
                    <h6 class="fw-bold mb-1 text-dark">CARTONO, ST</h6>
                    <p class="small text-primary fw-semibold mb-0">Manajer Operasional Jaringan</p>
                </div>
            </div>

            <div class="connector-line"></div>

            <!-- LEVEL 3: CABANG ASISTEN MANAJER (OPERASIONAL VS PEMELIHARAAN) -->
            <div class="plant-level">
                <!-- Jalur Operasional -->
                <div class="plant-card card-operasional">
                    <span class="badge-icon badge-operasional"><i class="fa-solid fa-water me-1"></i> Bidang Operasional</span>
                    <h6 class="fw-bold mb-1 text-dark">Endang Maryadi</h6>
                    <p class="small text-success fw-semibold mb-0">Asisten Manajer Operasi Jaringan</p>
                </div>

                <!-- Jalur Pemeliharaan -->
                <div class="plant-card card-pemeliharaan">
                    <span class="badge-icon badge-pemeliharaan"><i class="fa-solid fa-bolt me-1"></i> Bidang Pemeliharaan</span>
                    <h6 class="fw-bold mb-1 text-dark">SUMITRA DJARNUDJI, ST</h6>
                    <p class="small text-warning-emphasis fw-semibold mb-0">Asisten Manajer Pemeliharaan</p>
                    <span class="team-badge">Gardu Induk Curug, Mini Hydro, dll</span>
                </div>
            </div>

            <!-- ================= SUB-BAGIAN OPERASIONAL ================= -->
            <div class="section-title-tag bg-success text-white mt-4">
                <i class="fa-solid fa-gauge-high me-1"></i> SUPERVISOR & TIM OPERASIONAL (GI, Mini Hydro & PETT)
            </div>
            
            <div class="plant-level">
                <!-- 1. Ahlan Sopiana -->
                <div class="plant-card card-operasional">
                    <span class="badge-icon badge-operasional">Kelompok IV</span>
                    <h6 class="fw-bold mb-1 text-dark">Ahlan Sopiana</h6>
                    <p class="small text-muted mb-1">Supervisor Operasi Mini Hydro, GI & PETT</p>
                    <span class="team-badge"><strong>Tim:</strong> Lugi Rama Diansyah, Rizal Kurniawan</span>
                </div>

                <!-- 2. Yadi Suwarma -->
                <div class="plant-card card-operasional">
                    <span class="badge-icon badge-operasional">Kelompok II</span>
                    <h6 class="fw-bold mb-1 text-dark">Yadi Suwarma</h6>
                    <p class="small text-muted mb-1">Supervisor Operasi Mini Hydro, GI & PETT</p>
                    <span class="team-badge"><strong>Tim:</strong> Achmad Hidayat, Angga Hermawan</span>
                </div>

                <!-- 3. Andriana -->
                <div class="plant-card card-operasional">
                    <span class="badge-icon badge-operasional">Kelompok III</span>
                    <h6 class="fw-bold mb-1 text-dark">Andriana, ST</h6>
                    <p class="small text-muted mb-1">Supervisor Operasi Mini Hydro, GI & PETT</p>
                    <span class="team-badge"><strong>Tim:</strong> Ejan Suryadi, Yanuar Utomo</span>
                </div>

                <!-- 4. Saepudin -->
                <div class="plant-card card-operasional">
                    <span class="badge-icon badge-operasional">Kelompok I</span>
                    <h6 class="fw-bold mb-1 text-dark">Saepudin</h6>
                    <p class="small text-muted mb-1">Supervisor Operasi Mini Hydro, GI & PETT</p>
                    <span class="team-badge"><strong>Tim:</strong> Ibnu Aulia, Willy Wiriawan Hasan</span>
                </div>
            </div>


            <!-- ================= SUB-BAGIAN PEMELIHARAAN ================= -->
            <div class="section-title-tag bg-warning text-dark mt-4">
                <i class="fa-solid fa-screwdriver-wrench me-1"></i> SUPERVISOR & TIM PEMELIHARAAN (GI, Pompa, SUTT & SUTR)
            </div>

            <div class="plant-level">
                <!-- 1. Mulyadi -->
                <div class="plant-card card-pemeliharaan">
                    <span class="badge-icon badge-pemeliharaan">Mini Hydro & GI</span>
                    <h6 class="fw-bold mb-1 text-dark">Mulyadi</h6>
                    <p class="small text-muted mb-1">Supervisor Pemeliharaan Mini Hydro & GI Curug</p>
                    <span class="team-badge"><strong>Tim:</strong> Kholidin Tri Sandy, Sandy Aditya</span>
                </div>

                <!-- 2. Yosep Yusnandar -->
                <div class="plant-card card-pemeliharaan">
                    <span class="badge-icon badge-pemeliharaan">Pompa Elektrik</span>
                    <h6 class="fw-bold mb-1 text-dark">Yosep Yusnandar, S.T.</h6>
                    <p class="small text-muted mb-1">Supervisor Pemeliharaan Pompa Elektrik Tarum Timur</p>
                    <span class="team-badge"><strong>Tim:</strong> Akbar Jejef Maulana, Ade Irfan</span>
                </div>

                <!-- 3. Ahmad Hotib -->
                <div class="plant-card card-pemeliharaan">
                    <span class="badge-icon badge-pemeliharaan">SUTT & SUTM</span>
                    <h6 class="fw-bold mb-1 text-dark">Ahmad Hotib</h6>
                    <p class="small text-muted mb-1">Supervisor Pemeliharaan SUTT & SUTM Curug</p>
                    <span class="team-badge"><strong>Tim:</strong> Staf terkait SUTT & SUTM</span>
                </div>

                <!-- 4. Yusron -->
                <div class="plant-card card-pemeliharaan">
                    <span class="badge-icon badge-pemeliharaan">SUTR</span>
                    <h6 class="fw-bold mb-1 text-dark">Yusron</h6>
                    <p class="small text-muted mb-1">Supervisor Pemeliharaan SUTR Curug</p>
                    <span class="team-badge"><strong>Tim:</strong> Nurwanto</span>
                </div>
            </div>

        </div>
    </div>
</div>
"""

@pegawai_bp.route('/get-struktural-pegawai')
def get_struktural_pegawai():
    return PEGAWAI_SECTION_TEMPLATE
