import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';
import { LaporanBaru, ChecklistArchive } from '../types';

export function generateLaporanBaruPdf(laporan: LaporanBaru): void {
  const doc = new jsPDF({
    unit: 'pt',
    format: 'letter',
  });

  const pageWidth = doc.internal.pageSize.getWidth();

  // Header Title
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(14);
  doc.setTextColor(15, 23, 42); // #0f172a
  doc.text('PERUM JASA TIRTA II', pageWidth / 2, 50, { align: 'center' });
  doc.text('LAPORAN GANGGUAN OPERASIONAL & KRONOLOGI', pageWidth / 2, 70, { align: 'center' });

  // Metadata Table
  autoTable(doc, {
    startY: 95,
    margin: { left: 40, right: 40 },
    theme: 'grid',
    styles: {
      fontSize: 10,
      textColor: [30, 41, 59],
      cellPadding: 6,
      lineColor: [203, 213, 225],
      lineWidth: 0.5,
    },
    columnStyles: {
      0: { cellWidth: 140, fontStyle: 'bold', fillColor: [248, 250, 252] },
      1: { fillColor: [255, 255, 255] },
    },
    body: [
      ['Jenis Gangguan:', laporan.jenis],
      ['Tanggal Kejadian:', laporan.tanggal],
      ['Waktu (Jam):', laporan.waktu],
    ],
  });

  // Kronologi Section
  const lastY = (doc as any).lastAutoTable ? (doc as any).lastAutoTable.finalY : 180;
  
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(12);
  doc.setTextColor(15, 23, 42);
  doc.text('Kronologi Kejadian:', 40, lastY + 25);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(10);
  doc.setTextColor(51, 65, 85);
  
  const splitKronologi = doc.splitTextToSize(laporan.kronologi, pageWidth - 80);
  doc.text(splitKronologi, 40, lastY + 45);

  // Sign-off / footer section
  const endY = lastY + 45 + (splitKronologi.length * 14) + 40;
  const signatureY = Math.min(Math.max(endY, 620), 680);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.text('Mengetahui,', 80, signatureY);
  doc.text('Supervisor Terkait', 80, signatureY + 14);
  doc.text('Yang Melaporkan / Petugas,', pageWidth - 180, signatureY);

  doc.text('( ........................................ )', 80, signatureY + 65);
  doc.text(`( ${laporan.jenis.slice(0, 25)} )`, pageWidth - 180, signatureY + 65);

  doc.save(laporan.pdf_name);
}

export function generateChecklistPdf(data: ChecklistArchive): void {
  const doc = new jsPDF({
    unit: 'pt',
    format: 'letter',
  });

  const pageWidth = doc.internal.pageSize.getWidth();

  // Header Title
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(12);
  doc.setTextColor(15, 23, 42);
  doc.text('PERUM JASA TIRTA II', pageWidth / 2, 40, { align: 'center' });
  
  doc.setFontSize(10);
  const titleText = data.jenisGangguan ? data.jenisGangguan.toUpperCase() : 'CHECK LIST OPERASIONAL';
  const splitTitle = doc.splitTextToSize(titleText, pageWidth - 80);
  doc.text(splitTitle, pageWidth / 2, 56, { align: 'center' });

  const metaStartY = 56 + (splitTitle.length * 13) + 6;

  // Metadata Table
  autoTable(doc, {
    startY: metaStartY,
    margin: { left: 40, right: 40 },
    theme: 'grid',
    styles: {
      fontSize: 9,
      textColor: [30, 41, 59],
      cellPadding: 4,
      lineColor: [203, 213, 225],
      lineWidth: 0.5,
    },
    columnStyles: {
      0: { cellWidth: 140, fontStyle: 'bold', fillColor: [248, 250, 252] },
      1: { fillColor: [255, 255, 255] },
    },
    body: [
      ['Kategori / Lokasi:', data.kategori],
      ['Waktu Kejadian:', data.date],
      ['Group / Tim:', data.namaGroup || '-'],
      ['Petugas Pelaksana:', data.namaPetugas || '-'],
    ],
  });

  const tableStartY = (doc as any).lastAutoTable ? (doc as any).lastAutoTable.finalY + 12 : metaStartY + 80;

  if (data.mode === 'manual' && data.manualRows) {
    const tableBody = data.manualRows.map((row) => [
      row.no.toString(),
      row.penanganan,
      row.jam,
      row.status,
    ]);

    autoTable(doc, {
      startY: tableStartY,
      margin: { left: 40, right: 40 },
      theme: 'grid',
      head: [['No', 'Jenis Penanganan / Uraian', 'Jam / Pukul', 'Keadaan / Status']],
      headStyles: {
        fillColor: [15, 23, 42],
        textColor: [255, 255, 255],
        fontStyle: 'bold',
        fontSize: 9,
        halign: 'center',
      },
      styles: {
        fontSize: 8.5,
        textColor: [30, 41, 59],
        cellPadding: 5,
        lineColor: [203, 213, 225],
        lineWidth: 0.5,
      },
      columnStyles: {
        0: { cellWidth: 35, halign: 'center' },
        1: { cellWidth: 260 },
        2: { cellWidth: 100, halign: 'center' },
        3: { halign: 'center' },
      },
      body: tableBody.length > 0 ? tableBody : [['1', 'Pemeriksaan rutin gangguan', '-', 'Selesai']],
    });
  } else if (data.otomatisData && data.otomatisData.sections) {
    // Parse table sections stored in otomatisData
    const rows = data.otomatisData.sections;
    const formattedBody: any[] = [];

    rows.forEach((sec) => {
      // Header for section
      formattedBody.push([
        {
          content: sec.title,
          colSpan: 4,
          styles: { fontStyle: 'bold', fillColor: [241, 245, 249], textColor: [15, 23, 42] },
        },
      ]);
      sec.items.forEach((item: any) => {
        formattedBody.push([
          item.no.toString(),
          item.uraian,
          item.posisi || '-',
          item.jam || item.paraf || '-',
        ]);
      });
    });

    autoTable(doc, {
      startY: tableStartY,
      margin: { left: 40, right: 40 },
      theme: 'grid',
      head: [['No', 'Uraian Manuver / Pengecekan', 'Keadaan / Posisi', 'Pukul / Status']],
      headStyles: {
        fillColor: [15, 23, 42],
        textColor: [255, 255, 255],
        fontStyle: 'bold',
        fontSize: 9,
        halign: 'center',
      },
      styles: {
        fontSize: 8,
        textColor: [30, 41, 59],
        cellPadding: 4,
        lineColor: [203, 213, 225],
        lineWidth: 0.5,
      },
      columnStyles: {
        0: { cellWidth: 30, halign: 'center' },
        1: { cellWidth: 280 },
        2: { cellWidth: 120, halign: 'center' },
        3: { halign: 'center' },
      },
      body: formattedBody,
    });
  }

  const itemsEndY = (doc as any).lastAutoTable ? (doc as any).lastAutoTable.finalY : 500;

  // Final SOP instruction
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);
  doc.setTextColor(71, 85, 105);
  doc.text('IV. Melaporkan hasil pelaksanaan manuver (pindah line) ke kontrol Building.', 40, itemsEndY + 18);

  // Signatures table
  const sigY = Math.min(itemsEndY + 36, 680);
  autoTable(doc, {
    startY: sigY,
    margin: { left: 40, right: 40 },
    theme: 'plain',
    styles: {
      fontSize: 8,
      cellPadding: 2,
      halign: 'center',
      textColor: [30, 41, 59],
    },
    columnStyles: {
      0: { cellWidth: 180 },
      1: { cellWidth: 180 },
      2: { cellWidth: 170 },
    },
    body: [
      [
        'Mengetahui,\nKa. Seksi O & P GI Curug, Mini Hydro & PETT',
        'Kaur. Operasi GI Curug,\nMini Hydro & PETT',
        `Curug, ${data.date.split(' ')[0] || '...............'}\nYang melaksanakan`,
      ],
      ['\n\n\n', '\n\n\n', '\n\n\n'],
      ['( NIK. .................... )', '( NIK. .................... )', `( ${data.namaPetugas || 'NIK. ....................'} )`],
    ],
  });

  doc.save(data.name);
}
