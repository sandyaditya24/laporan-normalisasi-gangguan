from flask import Blueprint, request, redirect, url_for, render_template
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

normalisasi_bp = Blueprint('normalisasi', __name__)

PDF_FOLDER = "static"

@normalisasi_bp.route("/generate", methods=["POST"])
def generate_normalisasi():
    kategori = request.form.get("kategori")
    mode_pencatatan = request.form.get("mode_pencatatan")
    waktu = request.form.get("waktu")
    nama_group = request.form.get("nama_group")
    nama_petugas = request.form.get("nama_petugas")
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_name = f"Checklist_Normalisasi_{timestamp_str}.pdf"
    pdf_path = os.path.join(PDF_FOLDER, pdf_name)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#0f172a')
    )
    
    story.append(Paragraph("<b>PERUM JASA TIRTA II</b>", title_style))
    story.append(Paragraph(f"<b>LAPORAN NORMALISASI & CHECKLIST: {kategori}</b>", title_style))
    story.append(Spacer(1, 10))
    
    # Informasi Ringkas
    data_info = [
        [Paragraph("<b>Kategori / Lokasi:</b>", styles['Normal']), Paragraph(str(kategori), styles['Normal'])],
        [Paragraph("<b>Mode Pencatatan:</b>", styles['Normal']), Paragraph(str(mode_pencatatan), styles['Normal'])],
        [Paragraph("<b>Waktu Kejadian:</b>", styles['Normal']), Paragraph(str(waktu), styles['Normal'])],
        [Paragraph("<b>Tim / Petugas:</b>", styles['Normal']), Paragraph(f"{nama_group} - {nama_petugas}", styles['Normal'])],
    ]
    t_info = Table(data_info, colWidths=[120, 420])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 15))
    
    # Jika mode manual, ambil data dynamic rows
    if mode_pencatatan == 'manual':
        penanganan = request.form.getlist("penanganan[]")
        jam_item = request.form.getlist("jam_item[]")
        status_item = request.form.getlist("status_item[]")
        
        story.append(Paragraph("<b>Detail Penanganan (Mode Manual):</b>", styles['Heading3']))
        story.append(Spacer(1, 5))
        
        table_data = [["No", "Jenis Penanganan", "Jam", "Status"]]
        for i in range(len(penanganan)):
            table_data.append([str(i+1), penanganan[i], jam_item[i] if i < len(jam_item) else "", status_item[i] if i < len(status_item) else ""])
            
        t_manual = Table(table_data, colWidths=[30, 270, 100, 120])
        t_manual.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_manual)
    else:
        jenis_otomatis = request.form.get("jenis_gangguan_otomatis", "Checklist Otomatis")
        story.append(Paragraph(f"<b>Jenis Checklist Otomatis:</b> {jenis_otomatis}", styles['Normal']))
        story.append(Spacer(1, 10))
        story.append(Paragraph("<i>Dokumen checklist otomatis telah diproses sesuai parameter sistem gardu induk / unit terkait.</i>", styles['Normal']))

    doc.build(story)
    return redirect(url_for('index'))
