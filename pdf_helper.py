import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_laporan(jenis, waktu, tanggal, kronologi, pdf_folder):
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_name = f"Laporan_Gangguan_Baru_{timestamp_str}.pdf"
    pdf_path = os.path.join(pdf_folder, pdf_name)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=14,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#0f172a')
    )
    
    story.append(Paragraph("<b>PERUM JASA TIRTA II</b>", title_style))
    story.append(Paragraph("<b>LAPORAN GANGGUAN OPERASIONAL & KRONOLOGI</b>", title_style))
    story.append(Spacer(1, 15))
    
    data_info = [
        [Paragraph("<b>Jenis Gangguan:</b>", styles['Normal']), Paragraph(jenis, styles['Normal'])],
        [Paragraph("<b>Tanggal Kejadian:</b>", styles['Normal']), Paragraph(tanggal, styles['Normal'])],
        [Paragraph("<b>Waktu (Jam):</b>", styles['Normal']), Paragraph(waktu, styles['Normal'])],
    ]
    t_info = Table(data_info, colWidths=[120, 420])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Kronologi Kejadian:</b>", styles['Heading3']))
    story.append(Spacer(1, 5))
    story.append(Paragraph(kronologi.replace('\n', '<br/>'), styles['Normal']))
    
    doc.build(story)
    return pdf_name
