export interface LaporanBaru {
  id: string;
  jenis: string;
  tanggal: string;
  waktu: string;
  kronologi: string;
  pdf_name: string;
  createdAt: string;
}

export interface OtomatisItem {
  no: number;
  uraian: string;
  posisi?: string;
  jam?: string;
  paraf?: string;
}

export interface OtomatisSection {
  title: string;
  items: OtomatisItem[];
}

export interface OtomatisData {
  sections: OtomatisSection[];
}

export interface ChecklistArchive {
  id: string;
  name: string;
  date: string;
  kategori: string;
  jenisGangguan: string;
  mode: 'manual' | 'otomatis';
  namaGroup: string;
  namaPetugas: string;
  manualRows?: { no: number; penanganan: string; jam: string; status: string }[];
  otomatisData?: OtomatisData;
}

export interface ManualRow {
  id: string;
  penanganan: string;
  jam: string;
  status: string;
}

export interface FaqItem {
  id: string;
  kategori: 'profil' | 'plta' | 'bendungan' | 'wilayah' | 'bisnis' | string;
  question: string;
  answer: string;
  badge?: string;
  highlights?: string[];
  sourceUrl?: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
}
