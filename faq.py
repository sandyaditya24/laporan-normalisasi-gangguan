from flask import Blueprint, render_template_string

# Membuat Blueprint untuk modul FAQ / Tanya Jawab PJT II
faq_bp = Blueprint('faq', __name__)

# Template HTML khusus untuk Fitur Tanya Jawab Interaktif Perum Jasa Tirta II
FAQ_SECTION_TEMPLATE = """
<style>
    .faq-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 25px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .faq-container::before {
        content: "💧 ⚡ 🌍";
        position: absolute;
        top: 15px;
        right: 25px;
        font-size: 1.5rem;
        opacity: 0.15;
        letter-spacing: 10px;
    }
    .faq-search-box {
        border-radius: 50px 0 0 50px !important;
        border: 2px solid #cbd5e1;
        padding-left: 20px;
    }
    .faq-search-btn {
        border-radius: 0 50px 50px 0 !important;
        background-color: #0284c7;
        color: white;
        border: 2px solid #0284c7;
        padding: 0 20px;
    }
    .faq-search-btn:hover {
        background-color: #0369a1;
        color: white;
    }
    .accordion-item {
        border: none;
        border-radius: 12px !important;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        overflow: hidden;
    }
    .accordion-button {
        background-color: #ffffff;
        font-weight: 600;
        color: #1e293b;
        padding: 15px 20px;
        box-shadow: none !important;
    }
    .accordion-button:not(.collapsed) {
        background-color: #e0f2fe;
        color: #0369a1;
    }
    .accordion-body {
        background-color: #ffffff;
        color: #475569;
        font-size: 0.9rem;
        line-height: 1.6;
        padding: 20px;
    }
    .category-btn {
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 6px 16px;
        transition: all 0.2s ease;
    }
</style>

<div class="card content-card mb-4" id="container-faq-pjt2">
    <button type="button" class="btn-close-red-container" onclick="kosongkanKanan()" title="Tutup">
        <i class="fa-solid fa-xmark"></i>
    </button>
    <div class="card-header-custom text-white text-center py-3" style="background: linear-gradient(135deg, #1e293b, #0f172a);">
        <h4 class="mb-0 fw-bold fs-5"><i class="fa-solid fa-water me-2 text-info"></i> PUSAT INFORMASI & PENGETAHUAN PERUM JASA TIRTA II</h4>
        <p class="mb-0 text-white-50 small mt-1">Kenali lebih dekat profil, bendungan, PLTA, dan wilayah kerja PJT II</p>
    </div>
    <div class="card-body p-4 faq-container">
        
        <!-- Search Bar Interaktif -->
        <div class="input-group mb-4 shadow-sm">
            <input type="text" id="faqSearchInput" class="form-control faq-search-box" placeholder="Cari topik seputar Jasa Tirta II (misal: Jatiluhur, PLTA Curug, Irigasi)..." onkeyup="filterFAQ()">
            <button class="btn faq-search-btn" type="button"><i class="fa-solid fa-magnifying-glass"></i></button>
        </div>

        <!-- Tombol Kategori Cepat -->
        <div class="d-flex flex-wrap gap-2 mb-4 justify-content-center">
            <button class="btn btn-sm btn-outline-primary category-btn active" onclick="filterKategori('all', event)"><i class="fa-solid fa-globe me-1"></i> Semua</button>
            <button class="btn btn-sm btn-outline-primary category-btn" onclick="filterKategori('profil', event)"><i class="fa-solid fa-building me-1"></i> Profil PJT II</button>
            <button class="btn btn-sm btn-outline-primary category-btn" onclick="filterKategori('plta', event)"><i class="fa-solid fa-bolt me-1"></i> PLTA & Energi</button>
            <button class="btn btn-sm btn-outline-primary category-btn" onclick="filterKategori('bendungan', event)"><i class="fa-solid fa-water me-1"></i> Bendungan & Air</button>
        </div>

        <!-- Daftar Accordion Tanya Jawab -->
        <div class="accordion" id="accordionPJT2">
            
            <!-- Item 1 -->
            <div class="accordion-item faq-item" data-kategori="profil">
                <h2 class="accordion-header" id="headingOne">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                        <i class="fa-solid fa-circle-question text-primary me-2"></i> Apa itu Perum Jasa Tirta II (PJT II)?
                    </button>
                </h2>
                <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionPJT2">
                    <div class="accordion-body">
                        Perum Jasa Tirta II adalah Badan Usaha Milik Negara (BUMN) yang bertugas mengelola sumber daya air di wilayah sungai Citarum dan beberapa wilayah sungai lainnya di Jawa Barat. PJT II berperan penting dalam penyediaan air baku untuk industri, perkotaan, irigasi pertanian, serta pembangkit tenaga listrik (PLTA).
                    </div>
                </div>
            </div>

            <!-- Item 2 -->
            <div class="accordion-item faq-item" data-kategori="plta">
                <h2 class="accordion-header" id="headingTwo">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                        <i class="fa-solid fa-circle-question text-primary me-2"></i> Apa peran PLTA Curug dalam sistem Jasa Tirta II?
                    </button>
                </h2>
                <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionPJT2">
                    <div class="accordion-body">
                        PLTA Curug memanfaatkan aliran air dari saluran irigasi Tarum Timur untuk memutar turbin dan menghasilkan energi listrik terbarukan (pembangkit listrik tenaga air mini/mikro serta gardu induk) yang mendukung keandalan pasokan listrik serta sistem kelistrikan di bawah koordinasi Perum Jasa Tirta II Sektor Curug.
                    </div>
                </div>
            </div>

            <!-- Item 3 -->
            <div class="accordion-item faq-item" data-kategori="bendungan">
                <h2 class="accordion-header" id="headingThree">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                        <i class="fa-solid fa-circle-question text-primary me-2"></i> Di mana lokasi utama waduk dan kantor pusat PJT II?
                    </button>
                </h2>
                <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionPJT2">
                    <div class="accordion-body">
                        Kantor pusat dan waduk utama yang dikelola oleh Perum Jasa Tirta II berpusat di <strong>Waduk Ir. H. Djuanda (Jatiluhur)</strong>, Kabupaten Purwakarta, Jawa Barat, yang menjadi waduk serbaguna terbesar di Indonesia.
                    </div>
                </div>
            </div>

            <!-- Item 4 -->
            <div class="accordion-item faq-item" data-kategori="profil">
                <h2 class="accordion-header" id="headingFour">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                        <i class="fa-solid fa-circle-question text-primary me-2"></i> Apa saja fungsi utama pengelolaan air oleh PJT II?
                    </button>
                </h2>
                <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour" data-bs-parent="#accordionPJT2">
                    <div class="accordion-body">
                        Fungsi utama meliputi: penyediaan air irigasi untuk ratusan ribu hektar lahan pertanian (lumbung padi nasional di Jawa Barat), penyediaan air baku Perusahaan Daerah Air Minum (PDAM) & industri, PLTA (Pembangkit Listrik Tenaga Air), pengendalian banjir, serta pariwisata perairan.
                    </div>
                </div>
            </div>

        </div>
    </div>
</div>

<!-- Script Filter & Pencarian FAQ -->
<script>
function filterFAQ() {
    let input = document.getElementById('faqSearchInput').value.toLowerCase();
    let items = document.querySelectorAll('.faq-item');
    
    items.forEach(item => {
        let text = item.innerText.toLowerCase();
        if(text.includes(input)) {
            item.style.display = "";
        } else {
            item.style.display = "none";
        }
    });
}

function filterKategori(kategori, event) {
    // Ubah status tombol aktif
    document.querySelectorAll('.category-btn').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');

    let items = document.querySelectorAll('.faq-item');
    items.items?.forEach ? items.forEach(item => {
        if(kategori === 'all' || item.getAttribute('data-kategori') === kategori) {
            item.style.display = "";
        } else {
            item.style.display = "none";
        }
    }) : null;
}
</script>
"""

@faq_bp.route('/get-faq-pjt2')
def get_faq_pjt2():
    return FAQ_SECTION_TEMPLATE
