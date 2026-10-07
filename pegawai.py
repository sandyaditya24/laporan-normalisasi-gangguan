from flask import Blueprint, render_template_string

# Membuat Blueprint untuk modul Pegawai
pegawai_bp = Blueprint('pegawai', __name__)

# Template HTML khusus untuk bagian Struktural Pegawai (Kiri: Operasional, Kanan: Pemeliharaan, Tema Unsur Kimia/Sains)
PEGAWAI_SECTION_TEMPLATE = """
<style>
    .chemistry-plant-container {
        background: radial-gradient(circle at top right, #0f172a 0%, #1e293b 100%);
        border-radius: 16px;
        padding: 25px;
        position: relative;
        overflow: hidden;
        color: #f8fafc;
    }
    /* Efek latar belakang unsur kimia / molekul abstrak */
    .chemistry-plant-container::before {
        content: "⚗️ ⚛️ 🧪 ⚡";
        position: absolute;
        top: 15px;
        right: 25px;
        font-size: 1.8rem;
        opacity: 0.15;
        letter-spacing: 12px;
    }
    .tree-grid {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        overflow-x: auto;
        padding: 10px 0;
    }
    .chem-card {
        background: #ffffff;
        color: #1e293b;
        border-radius: 14px;
        padding: 15px 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        min-width: 270px;
        max-width: 310px;
        position: relative;
        margin: 12px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .chem-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.25);
    }
    .card-puncak {
        background: linear-gradient(135deg, #38bdf8, #0284c7);
        color: white;
        border: 2px solid #bae6fd;
    }
    .card-manajemen {
        background: linear-gradient(135deg, #e0f2fe, #bae6fd);
        border-color: #0284c7;
    }
    /* Sisi Kiri: Operasional (Nuansa Kimia Air / Cyan - Teal) */
    .card-operasional {
        background: linear-gradient(135deg, #f0fdf4, #ccfbf1);
        border-color: #14b8a6;
    }
    /* Sisi Kanan: Pemeliharaan (Nuansa Energi / Amber - Copper) */
    .card-pemeliharaan {
        background: linear-gradient(135deg, #fefce8, #fef08a);
        border-color: #eab308;
    }
    .chem-level {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 30px;
        width: 100%;
        margin-top: 15px;
    }
    .connector-line {
        width: 3px;
        height: 25px;
        background: #38bdf8;
        margin: 0 auto;
        border-radius: 2px;
    }
    .chem-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .badge-puncak { background: #0f172a; color: #38bdf8; }
    .badge-manajemen { background: #0284c7; color: #ffffff; }
    .badge-operasional { background: #0d9488; color: #ffffff; }
    .badge-pemeliharaan { background: #ca8a04; color: #ffffff; }
    
    .team-badge {
        font-size: 0.75rem;
        background: rgba(0,0,0,0.05);
        padding: 6px 10px;
        border-radius: 8px;
        color: #334155;
        margin-top: 8px;
        display: block;
        text-align: left;
        border-left: 3px solid #0284c7;
    }
    .branch-container {
        display: flex;
        justify-content: space-around;
        width: 100%;
        max-width: 900px;
        gap: 20px;
        margin-top: 10px;
    }
    .branch-column {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 14px;
        padding: 15px;
    }
    .branch-title {
        font-size: 0.85rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        padding: 6px 12px;
        border-radius: 6px;
    }
</style>

<div class="card content-card mb-4" id="container-struktural-pegawai" style="display: none;">
    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
        <i class="fa-solid fa-xmark"></i>
    </button>
    <div class="card-header-custom text-white text-center">
        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-atom me-2 text-info"></i> STRUKTUR LABORATORIUM ENERGI (PLTA CURUG)</h3>
        <p class="mb-0 text-white-50 small mt-1">Reaksi Sinergi Operasional (Kiri) & Pemeliharaan (Kanan) — PJT II</p>
    </div>
    <div class="card-body p-4 p-md-4 chemistry-plant-container">
        <div class="tree-grid">
            
            <!-- LEVEL 1: PIMPINAN PUNCAK -->
            <div class="chem-card card-puncak">
                <span class="chem-badge badge-puncak"><i class="fa-solid fa-flask-vial me-1"></i> Inti Reaktor Utama</span>
                <h5 class="fw-bold mb-1 text-white">BUDIYO, ST</h5>
                <p class="small text-white-50 mb-0">General Manajer PLTA</p>
            </div>

            <div class="connector-line"></div>

            <!-- LEVEL 2: MANAJEMEN OPERASIONAL JARINGAN -->
            <div class="chem-level">
                <div class="chem-card card-manajemen">
                    <span class="chem-badge badge-manajemen"><i class="fa-solid fa-network-wired me-1"></i> Katalisator Sektor</span>
                    <h6 class="fw-bold mb-1 text-dark">CARTONO, ST</h6>
                    <p class="small text-primary fw-semibold mb-0">Manajer Operasional Jaringan</p>
                </div>
            </div>

            <div class="connector-line"></div>

            <!-- LEVEL 3: ASISTEN MANAJER (KIRI: OPERASIONAL, KANAN: PEMELIHARAAN) -->
            <div class="chem-level" style="gap: 40px;">
                <!-- KIRI: ASISTEN MANAJER OPERASI -->
                <div class="chem-card card-operasional">
                    <span class="chem-badge badge-operasional"><i class="fa-solid fa-droplet me-1"></i> Formula Operasi</span>
                    <h6 class="fw-bold mb-1 text-dark">Endang Maryadi</h6>
                    <p class="small text-teal fw-semibold mb-0" style="color: #0d9488;">Asisten Manajer Operasi Jaringan</p>
                </div>

                <!-- KANAN: ASISTEN MANAJER PEMELIHARAAN -->
                <div class="chem-card card-pemeliharaan">
                    <span class="chem-badge badge-pemeliharaan"><i class="fa-solid fa-bolt me-1"></i> Formula Pemeliharaan</span>
                    <h6 class="fw-bold mb-1 text-dark">SUMITRA DJARNUDJI, ST</h6>
                    <p class="small text-warning-emphasis fw-semibold mb-0">Asisten Manajer Pemeliharaan</p>
                    <span class="team-badge" style="border-left-color: #ca8a04;">Gardu Induk Curug, Mini Hydro, dll</span>
                </div>
            </div>

            <div class="connector-line"></div>
            <div class="text-center fw-bold text-info small my-2" style="letter-spacing: 1px;">
                <i class="fa-solid fa-dna me-1"></i> ⚛️ JALUR KANDUNGAN TIM LAPANGAN: OPERASIONAL (KIRI) VS PEMELIHARAAN (KANAN) ⚛️
            </div>

            <!-- LEVEL 4: PEMISAHAN KOLOM (KIRI = OPERASI, KANAN = PEMELIHARAAN) -->
            <div class="branch-container">
                
                <!-- KOLOM KIRI: OPERASIONAL -->
                <div class="branch-column">
                    <div class="branch-title bg-teal text-white" style="background: #0d9488;">
                        <i class="fa-solid fa-arrows-split-up-and-left me-1"></i> Sektor Operasional (Kiri)
                    </div>

                    <!-- Ahlan Sopiana -->
                    <div class="chem-card card-operasional w-100" style="max-width: 100%;">
                        <span class="chem-badge badge-operasional">Kelompok IV</span>
                        <h6 class="fw-bold mb-1 text-dark">Ahlan Sopiana</h6>
                        <p class="small text-muted mb-1">Supervisor Operasi Mini Hydro, GI & PETT</p>
                        <span class="team-badge"><strong>Tim:</strong> Lugi Rama Diansyah, Rizal Kurniawan</span>
                    </div>

                    <!-- Yadi Suwarma -->
                    <div class="chem-card card-operasional w-100" style="max-width: 100%;">
                        <span class="chem-badge badge-operasional">Kelompok II</span>
                        <h6 class="fw-bold mb-1 text-dark">Yadi Suwarma</h6>
                        <p class="small text-muted mb-1">Supervisor Operasi Mini Hydro, GI & PETT</p>
                        <span class="team-badge"><strong>Tim:</strong> Achmad Hidayat, Angga Hermawan</span>
                    </div>

                    <!-- Andriana -->
                    <div class="chem-card card-operasional w-100" style="max-width: 100%;">
                        <span class="chem-badge badge-operasional">Kelompok III</span>
                        <h6 class="fw-bold mb-1 text-dark">Andriana, ST</h6>
                        <p class="small text-muted mb-1">Supervisor Operasi Mini Hydro, GI & PETT</p>
                        <span class="team-badge"><strong>Tim:</strong> Ejan Suryadi, Yanuar Utomo</span>
                    </div>

                    <!-- Saepudin -->
                    <div class="chem-card card-operasional w-100" style="max-width: 100%;">
                        <span class="chem-badge badge-operasional">Kelompok I</span>
                        <h6 class="fw-bold mb-1 text-dark">Saepudin</h6>
                        <p class="small text-muted mb-1">Supervisor Operasi Mini Hydro, GI & PETT</p>
                        <span class="team-badge"><strong>Tim:</strong> Ibnu Aulia, Willy Wiriawan</span>
                    </div>
                </div>

                <!-- KOLOM KANAN: PEMELIHARAAN -->
                <div class="branch-column">
                    <div class="branch-title bg-warning text-dark" style="background: #eab308;">
                        <i class="fa-solid fa-gears me-1"></i> Sektor Pemeliharaan (Kanan)
                    </div>

                    <!-- Mulyadi -->
                    <div class="chem-card card-pemeliharaan w-100" style="max-width: 100%;">
                        <span class="chem-badge badge-pemeliharaan">Mini Hydro & GI</span>
                        <h6 class="fw-bold mb-1 text-dark">Mulyadi</h6>
                        <p class="small text-muted mb-1">Supervisor Pemeliharaan Mini Hydro & GI Curug</p>
                        <span class="team-badge"><strong>Tim:</strong> Kholidin Tri Sandy, Sandy Aditya</span>
                    </div>

                    <!-- Yosep Yusnandar -->
                    <div class="chem-card card-pemeliharaan w-100" style="max-width: 100%;">
                        <span class="chem-badge badge-pemeliharaan">Pompa Elektrik</span>
                        <h6 class="fw-bold mb-1 text-dark">Yosep Yusnandar, S.T.</h6>
                        <p class="small text-muted mb-1">Supervisor Pemeliharaan Pompa Elektrik Tarum Timur</p>
                        <span class="team-badge"><strong>Tim:</strong> Akbar Jejef Maulana, Ade Irfan</span>
                    </div>

                    <!-- Ahmad Hotib -->
                    <div class="chem-card card-pemeliharaan w-100" style="max-width: 100%;">
                        <span class="chem-badge badge-pemeliharaan">SUTT & SUTM</span>
                        <h6 class="fw-bold mb-1 text-dark">Ahmad Hotib</h6>
                        <p class="small text-muted mb-1">Supervisor Pemeliharaan SUTT & SUTM Curug</p>
                        <span class="team-badge"><strong>Tim:</strong> Staf terkait SUTT & SUTM</span>
                    </div>

                    <!-- Yusron -->
                    <div class="chem-card card-pemeliharaan w-100" style="max-width: 100%;">
                        <span class="chem-badge badge-pemeliharaan">SUTR</span>
                        <h6 class="fw-bold mb-1 text-dark">Yusron</h6>
                        <p class="small text-muted mb-1">Supervisor Pemeliharaan SUTR Curug</p>
                        <span class="team-badge"><strong>Tim:</strong> Nurwanto</span>
                    </div>
                </div>

            </div>

        </div>
    </div>
</div>
"""

@pegawai_bp.route('/get-struktural-pegawai')
def get_struktural_pegawai():
    return PEGAWAI_SECTION_TEMPLATE
