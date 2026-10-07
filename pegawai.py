from flask import Blueprint, render_template_string

# Membuat Blueprint untuk modul Pegawai
pegawai_bp = Blueprint('pegawai', __name__)

# Template HTML khusus untuk bagian Struktural Pegawai
PEGAWAI_SECTION_TEMPLATE = """
<div class="card content-card mb-4" id="container-struktural-pegawai" style="display: none;">
    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
        <i class="fa-solid fa-xmark"></i>
    </button>
    <div class="card-header-custom text-white text-center">
        <h3 class="mb-0 fw-bold fs-4"><i class="fa-solid fa-sitemap me-2"></i> STRUKTURAL PEGAWAI & ORGANISASI</h3>
        <p class="mb-0 text-white-50 small mt-1">Daftar susunan organisasi dan penanggung jawab operasional PLTA Curug - PJT II</p>
    </div>
    <div class="card-body p-4 p-md-5">
        <h5 class="fw-bold text-dark mb-3"><i class="fa-solid fa-users-gear me-2 text-primary"></i> Susunan Tim Manajemen & Operasional</h5>
        <div class="table-responsive">
            <table class="table table-bordered table-hover align-middle bg-white shadow-sm">
                <thead class="table-dark text-center">
                    <tr>
                        <th width="6%">No</th>
                        <th width="28%">Jabatan / Posisi</th>
                        <th width="32%">Nama Pegawai / Pimpinan</th>
                        <th width="34%">Anggota Tim / Staf Terkait</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="text-center fw-bold">1</td>
                        <td class="fw-semibold">General Manajer PLTA</td>
                        <td>BUDIYO, ST[cite: 15]</td>
                        <td class="text-muted small">-</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">2</td>
                        <td class="fw-semibold">Manajer Operasional Jaringan</td>
                        <td>CARTONO, ST[cite: 14]</td>
                        <td class="text-muted small">-</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">3</td>
                        <td class="fw-semibold">Asisten Manajer Pemeliharaan</td>
                        <td>SUMITRA DJARNUDJI, ST[cite: 13]</td>
                        <td class="text-muted small">Gardu Induk Curug, Mini Hydro, dll[cite: 13]</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">4</td>
                        <td class="fw-semibold">Supervisor Pemeliharaan Mini Hydro & GI Curug</td>
                        <td>Mulyadi[cite: 12]</td>
                        <td class="text-muted small">Kholidin Tri Sandy Nasution, Sandy Aditya, dll[cite: 12]</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">5</td>
                        <td class="fw-semibold">Supervisor Operasi Mini Hydro (Kel. IV)</td>
                        <td>Ahlan Sopiana[cite: 6]</td>
                        <td class="text-muted small">Lugi Rama Diansyah, Rizal Kurniawan, dll[cite: 6]</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">6</td>
                        <td class="fw-semibold">Supervisor Operasi Mini Hydro (Kel. II)</td>
                        <td>Yadi Suwarma[cite: 7]</td>
                        <td class="text-muted small">Achmad Hidayat, Angga Hermawan, dll[cite: 7]</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">7</td>
                        <td class="fw-semibold">Supervisor Operasi Mini Hydro (Kel. III)</td>
                        <td>Andriana, ST[cite: 8]</td>
                        <td class="text-muted small">Ejan Suryadi, Yanuar Utomo Mandala Putra, dll[cite: 8]</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">8</td>
                        <td class="fw-semibold">Supervisor Operasi Mini Hydro (Kel. I)</td>
                        <td>Saepudin[cite: 9]</td>
                        <td class="text-muted small">Ibnu Aulia, Willy Wiriawan Hasan Mulyadi, S.T., dll[cite: 9]</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">9</td>
                        <td class="fw-semibold">Supervisor Pemeliharaan SUTT & SUTM Curug</td>
                        <td>Ahmad Hotib[cite: 10]</td>
                        <td class="text-muted small">Staf terkait pemeliharaan SUTT & SUTM[cite: 10]</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">10</td>
                        <td class="fw-semibold">Supervisor Pemeliharaan Pompa Elektrik</td>
                        <td>Yosep Yusnandar, S.T.[cite: 11]</td>
                        <td class="text-muted small">Akbar Jejef Maulana, S.T., Ade Irfan Sopian, dll[cite: 11]</td>
                    </tr>
                    <tr>
                        <td class="text-center fw-bold">11</td>
                        <td class="fw-semibold">Supervisor Pemeliharaan SUTR Curug</td>
                        <td>Yusron</td>
                        <td class="text-muted small">Nurwanto</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
"""

@pegawai_bp.route('/get-struktural-pegawai')
def get_struktural_pegawai():
    return PEGAWAI_SECTION_TEMPLATE
