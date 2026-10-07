from flask import Blueprint, render_template_string

# Membuat Blueprint untuk modul Pegawai
pegawai_bp = Blueprint('pegawai', __name__)

# Template HTML khusus untuk bagian Struktural Pegawai dengan gaya Diagram Pohon
PEGAWAI_SECTION_TEMPLATE = """
<style>
    .tree-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        overflow-x: auto;
        padding: 20px 0;
    }
    .tree-node {
        background: #ffffff;
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        min-width: 260px;
        max-width: 320px;
        position: relative;
        margin: 10px;
        transition: transform 0.2s;
    }
    .tree-node:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.2);
    }
    .tree-node.puncak {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        color: white;
        border-color: #0f172a;
    }
    .tree-node.manajemen {
        background: #eff6ff;
        border-color: #2563eb;
    }
    .tree-node.supervisor {
        background: #f8fafc;
        border-color: #cbd5e1;
    }
    .tree-level {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 20px;
        width: 100%;
        position: relative;
        margin-top: 15px;
    }
    .tree-connector-vertical {
        width: 2px;
        height: 25px;
        background: #cbd5e1;
        margin: 0 auto;
    }
    .badge-jabatan {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #2563eb;
        margin-bottom: 4px;
        display: block;
    }
    .tree-node.puncak .badge-jabatan {
        color: #93c5fd;
    }
    .team-list {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 6px;
        border-top: 1px dashed #e2e8f0;
        padding-top: 6px;
        text-align: left;
    }
</style>

<div class="card content-card mb-4" id="container-struktural-pegawai" style="display: none;">
    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
        <i class="fa-solid fa-xmark"></i>
    </button>
    <div class="card-header-custom text-white text-center">
        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-sitemap me-2"></i> DIAGRAM STRUKTURAL PEGAWAI & ORGANISASI</h3>
        <p class="mb-0 text-white-50 small mt-1">Bagan susunan hirarki dan penanggung jawab operasional PLTA Curug - PJT II</p>
    </div>
    <div class="card-body p-4 p-md-4">
        <div class="tree-container">
            
            <!-- LEVEL 1: PIMPINAN PUNCAK -->
            <span class="badge-jabatan text-dark mb-1">Pimpinan Puncak</span>
            <div class="tree-node puncak">
                <span class="badge-jabatan">General Manajer PLTA</span>
                <h6 class="fw-bold mb-0 text-white">BUDIYO, ST</h6>
            </div>

            <div class="tree-connector-vertical"></div>

            <!-- LEVEL 2: MANAJEMEN JARINGAN -->
            <div class="tree-level">
                <div class="tree-node manajemen">
                    <span class="badge-jabatan">Manajemen Jaringan</span>
                    <h6 class="fw-bold mb-0 text-dark">CARTONO, ST</h6>
                </div>
                <div class="tree-node manajemen">
                    <span class="badge-jabatan">Asisten Manajer Pemeliharaan</span>
                    <h6 class="fw-bold mb-0 text-dark">SUMITRA DJARNUDJI, ST</h6>
                    <div class="team-list">Unit: Gardu Induk Curug, Mini Hydro, dll</div>
                </div>
            </div>

            <div class="tree-connector-vertical"></div>
            <div class="text-center fw-bold text-muted small mb-2">— SUPERVISOR & TIM OPERASI / PEMELIHARAAN —</div>

            <!-- LEVEL 3: SUPERVISOR & TIM -->
            <div class="tree-level">
                
                <!-- 1. Mulyadi -->
                <div class="tree-node supervisor">
                    <span class="badge-jabatan">Supervisor Pemeliharaan</span>
                    <h6 class="fw-bold mb-1 text-dark">Mulyadi</h6>
                    <div class="team-list"><strong>Tim:</strong> Kholidin Tri Sandy Nasution, Sandy Aditya, dll</div>
                </div>

                <!-- 2. Ahlan Sopiana -->
                <div class="tree-node supervisor">
                    <span class="badge-jabatan">Supervisor Operasi (Kel. IV)</span>
                    <h6 class="fw-bold mb-1 text-dark">Ahlan Sopiana</h6>
                    <div class="team-list"><strong>Tim:</strong> Lugi Rama Diansyah, Rizal Kurniawan, dll</div>
                </div>

                <!-- 3. Yadi Suwarma -->
                <div class="tree-node supervisor">
                    <span class="badge-jabatan">Supervisor Operasi (Kel. II)</span>
                    <h6 class="fw-bold mb-1 text-dark">Yadi Suwarma</h6>
                    <div class="team-list"><strong>Tim:</strong> Achmad Hidayat, Angga Hermawan, dll</div>
                </div>

                <!-- 4. Andriana -->
                <div class="tree-node supervisor">
                    <span class="badge-jabatan">Supervisor Operasi (Kel. III)</span>
                    <h6 class="fw-bold mb-1 text-dark">Andriana, ST</h6>
                    <div class="team-list"><strong>Tim:</strong> Ejan Suryadi, Yanuar Utomo Mandala Putra, dll</div>
                </div>

                <!-- 5. Saepudin -->
                <div class="tree-node supervisor">
                    <span class="badge-jabatan">Supervisor Operasi (Kel. I)</span>
                    <h6 class="fw-bold mb-1 text-dark">Saepudin</h6>
                    <div class="team-list"><strong>Tim:</strong> Ibnu Aulia, Willy Wiriawan Hasan Mulyadi, S.T., dll</div>
                </div>

                <!-- 6. Ahmad Hotib -->
                <div class="tree-node supervisor">
                    <span class="badge-jabatan">Supervisor Pemeliharaan SUTT & SUTM</span>
                    <h6 class="fw-bold mb-1 text-dark">Ahmad Hotib</h6>
                    <div class="team-list"><strong>Tim:</strong> Staf terkait pemeliharaan SUTT & SUTM</div>
                </div>

                <!-- 7. Yosep Yusnandar -->
                <div class="tree-node supervisor">
                    <span class="badge-jabatan">Supervisor Pemeliharaan Pompa</span>
                    <h6 class="fw-bold mb-1 text-dark">Yosep Yusnandar, S.T.</h6>
                    <div class="team-list"><strong>Tim:</strong> Akbar Jejef Maulana, S.T., Ade Irfan Sopian, dll</div>
                </div>

                <!-- 8. Yusron -->
                <div class="tree-node supervisor">
                    <span class="badge-jabatan">Supervisor Pemeliharaan SUTR</span>
                    <h6 class="fw-bold mb-1 text-dark">Yusron</h6>
                    <div class="team-list"><strong>Tim:</strong> Nurwanto</div>
                </div>

            </div>

        </div>
    </div>
</div>
"""

@pegawai_bp.route('/get-struktural-png') # (atau route aslinya)
@pegawai_bp.route('/get-struktural-pegawai')
def get_struktural_pegawai():
    return PEGAWAI_SECTION_TEMPLATE
