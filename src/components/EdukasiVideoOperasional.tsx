import React, { useState, useRef, useEffect } from 'react';

interface EdukasiVideoOperasionalProps {
  onClose: () => void;
}

interface VideoTrack {
  id: string;
  title: string;
  category: string;
  categoryBadge: string;
  badgeColor: string;
  duration: string;
  durationSec: number;
  description: string;
  videoUrl: string;
  thumbnail: string;
  chapters: { time: number; label: string; desc: string }[];
  keyPoints: string[];
}

const DEFAULT_VIDEOS: VideoTrack[] = [
  {
    id: 'vid-1',
    title: 'Animasi 3D Prinsip Kerja & Konversi Energi Turbin PLTA Curug (2x3400 kW)',
    category: 'Animasi 3D & Prinsip Fisika',
    categoryBadge: 'Animasi 3D Teknis',
    badgeColor: 'bg-info text-dark',
    duration: '03:45',
    durationSec: 225,
    description:
      'Penjelasan visual 3D prinsip kerja PLTA Curug: bagaimana elevasi TMA hulu (+10.50 m) menghasilkan energi potensial air, dialirkan melalui intake dan penstock bertekanan tinggi menuju turbin Francis 2x3400 kW, memutar generator sinkron untuk menghasilkan listrik 6,3 kV yang dinaikkan ke 70 kV.',
    // Standard high-reliability HTML5 tech demo video stream
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
    thumbnail: 'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80',
    chapters: [
      { time: 0, label: '00:00 - Pengenalan Kompleks Bendung & PLTA Curug', desc: 'Lokasi strategis di Sungai Citarum hilir' },
      { time: 35, label: '00:35 - Aliran Intake & Pipa Pesat (Penstock)', desc: 'Konversi elevasi air hulu +10.5 m ke tekanan hidrolik' },
      { time: 80, label: '01:20 - Spiral Casing & Guide Vane', desc: 'Pengaturan debit air masuk ke sudut sudu turbin' },
      { time: 135, label: '02:15 - Runner Turbin & Poros Generator', desc: 'Putaran turbin 500 RPM memutar rotor elektromagnetik' },
      { time: 180, label: '03:00 - Trafo Step-Up & Transmisi 70 kV Curug', desc: 'Penyaluran listrik ke Switchgear GI Curug' },
    ],
    keyPoints: [
      'Pemanfaatan head potensial air Curug (+10.50 m hulu ke +2.10 m hilir).',
      'Dua unit turbin air bertipe Francis dengan kapasitas masing-masing 3.400 kW (total 6.800 kW).',
      'Efisiensi konversi hidrolik ke mekanik mencapai >91% pada beban optimal.',
    ],
  },
  {
    id: 'vid-2',
    title: 'Panduan SOP Start-Up & Sinkronisasi Cubicle LGB001JD Unit Turbin Curug',
    category: 'SOP Video Operasional',
    categoryBadge: 'Instruksi Kerja F-20',
    badgeColor: 'bg-primary text-white',
    duration: '04:50',
    durationSec: 290,
    description:
      'Panduan langkah demi langkah prosedur start-up unit turbin air sesuai SOP resmi F-20/DPL/IK.10-01. Mulai dari pemeriksaan pra-start (level oli, pendingin, governor 120 bar), pembukaan guide vane bertahap, akselerasi kecepatan hingga sinkronisasi tegangan 6,3 kV dengan frekuensi 50.00 Hz.',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
    thumbnail: 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80',
    chapters: [
      { time: 0, label: '00:00 - Pemeriksaan Awal & Koordinasi Operator Bendung', desc: 'Cek TMA hulu, saringan intake bebas sampah' },
      { time: 45, label: '00:45 - Sistem Hidrolik & Pelumasan Bearing', desc: 'Tekanan oli governor normal 60/120 bar' },
      { time: 110, label: '01:50 - Pembukaan Katup Masuk & Akselerasi RPM', desc: 'Buka guide vane perlahan hingga kecepatan 500 RPM' },
      { time: 190, label: '03:10 - Sinkronisasi Tegangan & Frekuensi (Synchroscope)', desc: 'Pencocokan sudut fase tegangan generator 6,3 kV' },
      { time: 240, label: '04:00 - Penutupan PMT Cubicle LGB001JD & Beban Normal', desc: 'Unit resmi masuk interkoneksi GI Curug' },
    ],
    keyPoints: [
      'Wajib koordinasi radio dengan Operator Control Room Bendung Curug.',
      'Periksa annunciator relai cubicle sebelum memutar tuas start.',
      'Batas deviasi frekuensi maksimum saat sinkronisasi adalah ±0.05 Hz.',
    ],
  },
  {
    id: 'vid-3',
    title: 'Panduan Prosedur Manuver Pemindahan Penghantar 70 kV (Jatiluhur ➔ Kosambi)',
    category: 'Prosedur Manuver Gardu Induk',
    categoryBadge: 'SOP IK.12-01 & IK.12-02',
    badgeColor: 'bg-success text-white',
    duration: '05:15',
    durationSec: 315,
    description:
      'Video panduan pengoperasian interlock PMT (Pemutus Tenaga) dan PMS (Pemisah) saat pengalihan jalur suplai transmisi 70 kV antara Penghantar Jatiluhur dan Penghantar Kosambi PLN di Gardu Induk Curug.',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
    thumbnail: 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=800&q=80',
    chapters: [
      { time: 0, label: '00:00 - Persiapan & Izin Manuver Dispatcher JTL', desc: 'Pencatatan jam warta dan pembagian tugas operator' },
      { time: 55, label: '00:55 - Pengecekan Interlock PMT Bay Jatiluhur & Kosambi', desc: 'Verifikasi kondisi kontak dan tekanan gas SF6' },
      { time: 140, label: '02:20 - Operasi Pemisah PMS Busbar & Line', desc: 'Urutan baku buka/tutup PMS sebelum PMT' },
      { time: 220, label: '03:40 - Pemasukan PMT 70 kV Penghantar Kosambi', desc: 'Indikator lampu merah menyala tanda PMT Closed' },
      { time: 280, label: '04:40 - Pengukuran Tegangan Bus & Arus Beban', desc: 'Tegangan bus stabil pada 70.4 kV, 50.02 Hz' },
    ],
    keyPoints: [
      'Gunakan selalu APD standar: Helm K3, Sarung Tangan Isolasi 70 kV, dan Sepatu Safety.',
      'Dilarang membuka PMS dalam kondisi PMT masih posisi tertutup (berbeban).',
      'Konfirmasi kembali status sakelar ke Operator Control Building Jatiluhur.',
    ],
  },
  {
    id: 'vid-4',
    title: 'Prosedur Tanggap Darurat & Penanganan Trip Gardu Induk Curug 70 / 6,3 kV',
    category: 'Emergency & Troubleshooting',
    categoryBadge: 'SOP Darurat F-20/GI-CRG/01',
    badgeColor: 'bg-danger text-white',
    duration: '04:10',
    durationSec: 250,
    description:
      'Langkah taktis operator saat sirine alarm trip berbunyi: investigasi panel annunciator, pencatatan drop tegangan bus, isolasi peralatan yang terindikasi gangguan, dan prosedur pemulihan (restoration).',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
    thumbnail: 'https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=800&q=80',
    chapters: [
      { time: 0, label: '00:00 - Respon Cepat Alarm & Pengenalan Trip', desc: 'Matikan klakson alarm dan amati bendera relai' },
      { time: 40, label: '00:40 - Identifikasi Kode Relai Proteksi (Overcurrent/Differential)', desc: 'Cek relai 50/51, 87T, atau Buchholz trafo' },
      { time: 115, label: '01:55 - Pemisahan Bay Bermasalah dari Busbar', desc: 'Pencegahan gangguan meluas ke line PLN' },
      { time: 175, label: '02:55 - Pembuatan Laporan Kronologi Kejadian', desc: 'Pengisian form laporan gangguan resmi PJT II' },
    ],
    keyPoints: [
      'Tetap tenang dan utamakan keselamatan personil sebelum peralatan.',
      'Jangan mereset bendera indikator relai sebelum dicatat lengkap.',
      'Laporkan segera ke Asisten Manajer Operasi PLTA Curug.',
    ],
  },
  {
    id: 'vid-5',
    title: 'Animasi Sistem Kaskade 3 Waduk Citarum (Saguling ➔ Cirata ➔ Jatiluhur ➔ Curug)',
    category: 'Hidrologi & Kaskade Citarum',
    categoryBadge: 'Telemetri Hidrologi',
    badgeColor: 'bg-warning text-dark',
    duration: '03:30',
    durationSec: 210,
    description:
      'Visualisasi skematik pergerakan aliran air Sungai Citarum dari hulu Gunung Wayang melintasi Waduk Saguling, Waduk Cirata, Waduk Ir. H. Djuanda (Jatiluhur), hingga diatur pembagiannya di Bendung Curug ke Tarum Barat, Timur, dan Utara.',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
    thumbnail: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
    chapters: [
      { time: 0, label: '00:00 - Daerah Aliran Sungai (DAS) Citarum Hulu', desc: 'Tangkapan air seluas ±12.000 km²' },
      { time: 45, label: '00:45 - Waduk Saguling (643 mdpl) & Cirata (220 mdpl)', desc: 'Pembangkit listrik puncak sistem Jawa-Bali' },
      { time: 105, label: '01:45 - Waduk Ir. H. Djuanda Jatiluhur (107 mdpl)', desc: 'Waduk serbaguna penampung 3 miliar m³ air' },
      { time: 160, label: '02:40 - Bendung Curug (Bagi Curug) & Tarum Timur/Barat', desc: 'Pasokan vital air baku Jakarta & irigasi Pantura' },
    ],
    keyPoints: [
      'Pola operasi menerapkan prinsip "Equal Sharing" kaskade Citarum.',
      'TMA Curug dijaga pada elevasi aman normal +10.50 m.',
      'PETT (Pompa Elektrik Tarum Timur) mendukung suplai irigasi Subang-Indramayu.',
    ],
  },
];

export const EdukasiVideoOperasional: React.FC<EdukasiVideoOperasionalProps> = ({ onClose }) => {
  const [activeTab, setActiveTab] = useState<'video' | 'animasi' | 'komponen'>('video');
  const [selectedVideo, setSelectedVideo] = useState<VideoTrack>(DEFAULT_VIDEOS[0]);
  const [customVideoUrl, setCustomVideoUrl] = useState('');
  const [showCustomModal, setShowCustomModal] = useState(false);

  // Video player controls state
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.85);
  const [isMuted, setIsMuted] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const playerContainerRef = useRef<HTMLDivElement | null>(null);

  // Interactive Physics Simulation Canvas state
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [simRunning, setSimRunning] = useState(true);
  const [waterHead, setWaterHead] = useState(10.5); // meter
  const [waterDischarge, setWaterDischarge] = useState(38); // m3/s
  const [turbineRpm, setTurbineRpm] = useState(500); // RPM
  const [generatorLoadKw, setGeneratorLoadKw] = useState(3400); // kW per unit
  const [valveOpening, setValveOpening] = useState(85); // %

  // Format seconds to mm:ss
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins < 10 ? '0' : ''}${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  // Video element events
  const handlePlayPause = () => {
    if (!videoRef.current) return;
    if (videoRef.current.paused) {
      videoRef.current.play().catch((err) => console.log('Autoplay blocked:', err));
      setIsPlaying(true);
    } else {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  const handleTimeUpdate = () => {
    if (!videoRef.current) return;
    setCurrentTime(videoRef.current.currentTime);
  };

  const handleLoadedMetadata = () => {
    if (!videoRef.current) return;
    setDuration(videoRef.current.duration || selectedVideo.durationSec);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const seekTime = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.currentTime = seekTime;
      setCurrentTime(seekTime);
    }
  };

  const handleJumpToChapter = (timeSec: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = timeSec;
      videoRef.current.play().catch(() => {});
      setIsPlaying(true);
    }
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVol = parseFloat(e.target.value);
    setVolume(newVol);
    if (videoRef.current) {
      videoRef.current.volume = newVol;
      videoRef.current.muted = newVol === 0;
    }
    setIsMuted(newVol === 0);
  };

  const handleToggleMute = () => {
    if (!videoRef.current) return;
    const nextMuted = !isMuted;
    setIsMuted(nextMuted);
    videoRef.current.muted = nextMuted;
  };

  const handleRateChange = (rate: number) => {
    setPlaybackRate(rate);
    if (videoRef.current) {
      videoRef.current.playbackRate = rate;
    }
  };

  const handleToggleFullscreen = () => {
    if (!playerContainerRef.current) return;
    if (!document.fullscreenElement) {
      playerContainerRef.current.requestFullscreen().catch((err) => console.log(err));
      setIsFullscreen(true);
    } else {
      document.exitFullscreen().catch((err) => console.log(err));
      setIsFullscreen(false);
    }
  };

  const handleSelectVideoTrack = (track: VideoTrack) => {
    setSelectedVideo(track);
    setCurrentTime(0);
    setIsPlaying(false);
    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.load();
    }
  };

  const handleApplyCustomUrl = () => {
    if (!customVideoUrl.trim()) return;
    const customTrack: VideoTrack = {
      id: `custom-${Date.now()}`,
      title: 'Video Kustom Pilihan Operator',
      category: 'Video Internal PJT II',
      categoryBadge: 'Video Khusus',
      badgeColor: 'bg-purple-600 text-white',
      duration: 'Custom',
      durationSec: 300,
      description: `Video yang dimuat dari tautan eksternal: ${customVideoUrl}`,
      videoUrl: customVideoUrl,
      thumbnail: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80',
      chapters: [
        { time: 0, label: '00:00 - Mulai Video', desc: 'Pemutaran berkas panduan' },
      ],
      keyPoints: ['Tautan video kustom berhasil dimuat ke dalam pemutar sistem.'],
    };
    setSelectedVideo(customTrack);
    setShowCustomModal(false);
    setCustomVideoUrl('');
    setIsPlaying(false);
  };

  // Interactive 2D/3D Canvas Simulation of Water Turbine
  useEffect(() => {
    if (activeTab !== 'animasi') return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let particleOffset = 0;
    let turbineAngle = 0;
    let sparkTimer = 0;

    // Generate water particles along penstock and turbine
    const particles = Array.from({ length: 65 }, () => ({
      x: Math.random(),
      y: Math.random(),
      speed: 0.004 + Math.random() * 0.005,
      size: 2 + Math.random() * 2.5,
    }));

    const render = () => {
      const width = canvas.width;
      const height = canvas.height;

      // Dark technical blueprint background
      ctx.fillStyle = '#07111e';
      ctx.fillRect(0, 0, width, height);

      // Grid blueprint lines
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.07)';
      ctx.lineWidth = 1;
      for (let x = 0; x < width; x += 30) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += 30) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // 1. Water Reservoir Intake (Curug Head Pond +10.50 m)
      const reservoirWidth = width * 0.22;
      const waterLevelY = height * 0.28;
      
      const gradReservoir = ctx.createLinearGradient(0, waterLevelY, 0, height * 0.65);
      gradReservoir.addColorStop(0, '#38bdf8');
      gradReservoir.addColorStop(1, '#0284c7');
      ctx.fillStyle = gradReservoir;
      ctx.fillRect(20, waterLevelY, reservoirWidth, height * 0.45);

      // Concrete Intake Dam Wall
      ctx.fillStyle = '#334155';
      ctx.fillRect(reservoirWidth + 20, height * 0.18, 30, height * 0.65);

      // Intake Water Surface Waves
      ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
      ctx.beginPath();
      for (let i = 20; i <= reservoirWidth + 20; i += 10) {
        const wave = Math.sin((i + particleOffset * 10) * 0.08) * 3;
        ctx.lineTo(i, waterLevelY + wave);
      }
      ctx.lineTo(reservoirWidth + 20, waterLevelY + 8);
      ctx.lineTo(20, waterLevelY + 8);
      ctx.fill();

      // Text TMA Curug
      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 12px "Plus Jakarta Sans", sans-serif';
      ctx.fillText(`TMA Hulu: +${waterHead.toFixed(2)} m`, 30, waterLevelY - 18);
      ctx.fillStyle = '#38bdf8';
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.fillText('Bendung Curug Reservoir', 30, waterLevelY - 5);

      // 2. Penstock (Pipa Pesat Bertekanan)
      const penstockStartX = reservoirWidth + 50;
      const penstockStartY = height * 0.42;
      const penstockEndX = width * 0.52;
      const penstockEndY = height * 0.58;

      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 42;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(penstockStartX, penstockStartY);
      ctx.lineTo(penstockEndX, penstockEndY);
      ctx.stroke();

      // Penstock Water Flow Inside
      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = 32;
      ctx.beginPath();
      ctx.moveTo(penstockStartX, penstockStartY);
      ctx.lineTo(penstockEndX, penstockEndY);
      ctx.stroke();

      // Guide Vane / Valve Indicator
      const valveX = (penstockStartX + penstockEndX) / 2;
      const valveY = (penstockStartY + penstockEndY) / 2;
      ctx.fillStyle = '#f59e0b';
      ctx.beginPath();
      ctx.arc(valveX, valveY, 14, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#000';
      ctx.font = 'bold 9px sans-serif';
      ctx.fillText(`${valveOpening}%`, valveX - 9, valveY + 3);

      // Animated Water Particles in Penstock
      if (simRunning) {
        ctx.fillStyle = '#e0f2fe';
        particles.forEach((p) => {
          p.x = (p.x + p.speed * (turbineRpm / 350)) % 1;
          const px = penstockStartX + p.x * (penstockEndX - penstockStartX);
          const py = penstockStartY + p.x * (penstockEndY - penstockStartY) + (p.y - 0.5) * 16;
          ctx.beginPath();
          ctx.arc(px, py, p.size, 0, Math.PI * 2);
          ctx.fill();
        });
      }

      // 3. Francis Turbine Spiral Casing (Rumah Keong)
      const turbineCenterX = penstockEndX + 45;
      const turbineCenterY = penstockEndY + 10;
      const casingRadius = 48;

      // Outer Spiral Casing
      ctx.fillStyle = '#1e293b';
      ctx.strokeStyle = '#0ea5e9';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.arc(turbineCenterX, turbineCenterY, casingRadius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Rotating Turbine Runner (Sudu Turbin)
      if (simRunning) {
        turbineAngle += (turbineRpm / 500) * 0.08;
      }

      ctx.save();
      ctx.translate(turbineCenterX, turbineCenterY);
      ctx.rotate(turbineAngle);

      // 8 Blades of Francis Runner
      const numBlades = 8;
      for (let b = 0; b < numBlades; b++) {
        const bAngle = (b * (Math.PI * 2)) / numBlades;
        ctx.fillStyle = b % 2 === 0 ? '#38bdf8' : '#0284c7';
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.arc(0, 0, 36, bAngle, bAngle + 0.45);
        ctx.closePath();
        ctx.fill();
      }

      // Center Hub
      ctx.fillStyle = '#f8fafc';
      ctx.beginPath();
      ctx.arc(0, 0, 10, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // Label Turbin
      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText('Turbin Francis Curug', turbineCenterX - 45, turbineCenterY + 65);
      ctx.fillStyle = '#38bdf8';
      ctx.font = '10px monospace';
      ctx.fillText(`${turbineRpm} RPM`, turbineCenterX - 20, turbineCenterY + 79);

      // 4. Draft Tube (Saluran Buang ke Hilir +2.10 m)
      const tailwaterX = turbineCenterX + 10;
      const tailwaterY = turbineCenterY + 95;
      ctx.fillStyle = '#0369a1';
      ctx.fillRect(tailwaterX - 25, tailwaterY, 55, 30);
      ctx.fillStyle = '#94a3b8';
      ctx.font = '9px monospace';
      ctx.fillText('Tailrace +2.10 m', tailwaterX - 28, tailwaterY + 22);

      // 5. Vertical Shaft to Generator
      const generatorX = turbineCenterX;
      const generatorY = turbineCenterY - 110;

      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 10;
      ctx.beginPath();
      ctx.moveTo(turbineCenterX, turbineCenterY - 35);
      ctx.lineTo(generatorX, generatorY + 35);
      ctx.stroke();

      // 6. Synchronous Generator (Stator & Rotor)
      ctx.fillStyle = '#0f172a';
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.roundRect(generatorX - 45, generatorY - 35, 90, 70, 8);
      ctx.fill();
      ctx.stroke();

      // Magnetic flux lines in generator
      sparkTimer += 0.05;
      const pulseColor = simRunning ? `rgba(34, 197, 94, ${0.4 + Math.sin(sparkTimer * 4) * 0.3})` : 'rgba(100, 116, 139, 0.2)';
      ctx.strokeStyle = pulseColor;
      ctx.lineWidth = 2;
      for (let r = 15; r <= 35; r += 10) {
        ctx.beginPath();
        ctx.arc(generatorX, generatorY, r, 0, Math.PI * 2);
        ctx.stroke();
      }

      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText('Generator Sinkron', generatorX - 42, generatorY - 10);
      ctx.fillStyle = '#4ade80';
      ctx.font = 'bold 12px monospace';
      ctx.fillText(`${generatorLoadKw} kW`, generatorX - 26, generatorY + 8);
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '9px monospace';
      ctx.fillText('6,3 kV / 50 Hz', generatorX - 30, generatorY + 24);

      // 7. Power Cable to Step-Up Transformer (70 kV)
      const trafoX = width * 0.82;
      const trafoY = generatorY;

      ctx.strokeStyle = simRunning ? '#eab308' : '#64748b';
      ctx.lineWidth = 5;
      ctx.setLineDash([6, 4]);
      ctx.lineDashOffset = -particleOffset * 15;
      ctx.beginPath();
      ctx.moveTo(generatorX + 45, generatorY);
      ctx.lineTo(trafoX - 35, trafoY);
      ctx.stroke();
      ctx.setLineDash([]);

      // Transformer Box
      ctx.fillStyle = '#1e293b';
      ctx.strokeStyle = '#eab308';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.roundRect(trafoX - 35, trafoY - 30, 70, 60, 6);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Trafo Step-Up', trafoX - 30, trafoY - 10);
      ctx.fillStyle = '#fbbf24';
      ctx.font = 'bold 11px monospace';
      ctx.fillText('6,3 / 70 kV', trafoX - 28, trafoY + 8);

      // 8. Transmission Pylon Tower & Busbar GI Curug
      const pylonX = width * 0.93;
      const pylonY = height * 0.35;

      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 2;
      // Draw simple electricity tower
      ctx.beginPath();
      ctx.moveTo(pylonX, pylonY - 50);
      ctx.lineTo(pylonX - 20, pylonY + 60);
      ctx.lineTo(pylonX + 20, pylonY + 60);
      ctx.closePath();
      ctx.stroke();
      // Tower crossarms
      ctx.beginPath();
      ctx.moveTo(pylonX - 28, pylonY - 25);
      ctx.lineTo(pylonX + 28, pylonY - 25);
      ctx.moveTo(pylonX - 24, pylonY);
      ctx.lineTo(pylonX + 24, pylonY);
      ctx.stroke();

      // Power Line from Trafo to Tower
      ctx.strokeStyle = simRunning ? '#38bdf8' : '#475569';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(trafoX + 35, trafoY);
      ctx.quadraticCurveTo(width * 0.88, pylonY - 10, pylonX - 25, pylonY - 25);
      ctx.stroke();

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('GI 70 kV', pylonX - 18, pylonY + 75);
      ctx.fillStyle = '#22c55e';
      ctx.font = '9px monospace';
      ctx.fillText('JTL / KSB', pylonX - 20, pylonY + 88);

      particleOffset += 0.05;
      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [activeTab, simRunning, waterHead, waterDischarge, turbineRpm, generatorLoadKw, valveOpening]);

  // Adjust simulation inputs
  const handleGovernorIncrease = () => {
    setValveOpening((prev) => Math.min(100, prev + 5));
    setTurbineRpm((prev) => Math.min(520, prev + 15));
    setGeneratorLoadKw((prev) => Math.min(3400, prev + 150));
    setWaterDischarge((prev) => Math.min(45, prev + 1.5));
  };

  const handleGovernorDecrease = () => {
    setValveOpening((prev) => Math.max(10, prev - 5));
    setTurbineRpm((prev) => Math.max(200, prev - 20));
    setGeneratorLoadKw((prev) => Math.max(500, prev - 250));
    setWaterDischarge((prev) => Math.max(15, prev - 2));
  };

  const handleSimEmergencyTrip = () => {
    setSimRunning(false);
    setTurbineRpm(0);
    setGeneratorLoadKw(0);
    setValveOpening(0);
  };

  const handleSimNormalise = () => {
    setSimRunning(true);
    setTurbineRpm(500);
    setGeneratorLoadKw(3400);
    setValveOpening(85);
  };

  return (
    <div className="card content-card mb-4" id="container-edukasi-video">
      {/* Top Close Button */}
      <button
        type="button"
        className="btn-close-red-container"
        onClick={onClose}
        title="Tutup Menu Edukasi"
      >
        <i className="fa-solid fa-xmark"></i>
      </button>

      {/* HEADER SECTION */}
      <div
        className="card-header-custom text-white text-center py-4 px-3"
        style={{ background: 'linear-gradient(135deg, #09172e 0%, #063456 50%, #031b2e 100%)' }}
      >
        <div className="d-flex align-items-center justify-content-center gap-2 mb-2">
          <span className="badge bg-danger text-white px-3 py-1 rounded-pill small fw-bold shadow-xs">
            <i className="fa-solid fa-circle-play me-1.5 animate-pulse"></i> Pemutar Video &amp; Animasi Interaktif
          </span>
          <span className="badge bg-slate-800 text-cyan-300 border border-slate-700 px-3 py-1 rounded-pill small">
            Turbin 2x3400 kW Curug
          </span>
        </div>
        <h3 className="mb-1 fw-bold fs-4 text-white">
          <i className="fa-solid fa-film me-2 text-cyan-400"></i> EDUKASI ANIMASI &amp; VIDEO PANDUAN OPERASIONAL PLTA CURUG
        </h3>
        <p className="mb-0 text-cyan-100 small mt-1 max-w-xl mx-auto" style={{ lineHeight: 1.6 }}>
          Pusat media instruksional teknis: video panduan operasional SOP F-20, manuver Gardu Induk 70/6,3 kV, serta simulasi interaktif aliran air dan turbin air unit 2x3400 kW.
        </p>

        {/* Navigation Tabs */}
        <div className="mt-3.5 d-flex flex-wrap align-items-center justify-content-center gap-2">
          <button
            type="button"
            className={`btn btn-sm rounded-pill px-3.5 py-1.5 fw-semibold transition-all ${
              activeTab === 'video'
                ? 'btn-info text-dark shadow-sm'
                : 'btn-outline-light text-white'
            }`}
            onClick={() => setActiveTab('video')}
          >
            <i className="fa-solid fa-play me-1.5"></i> 1. Pemutar Video Panduan ({DEFAULT_VIDEOS.length} Video)
          </button>
          <button
            type="button"
            className={`btn btn-sm rounded-pill px-3.5 py-1.5 fw-semibold transition-all ${
              activeTab === 'animasi'
                ? 'btn-info text-dark shadow-sm'
                : 'btn-outline-light text-white'
            }`}
            onClick={() => setActiveTab('animasi')}
          >
            <i className="fa-solid fa-atom me-1.5"></i> 2. Animasi Fisika &amp; Skematik Aliran Air
          </button>
          <button
            type="button"
            className={`btn btn-sm rounded-pill px-3.5 py-1.5 fw-semibold transition-all ${
              activeTab === 'komponen'
                ? 'btn-info text-dark shadow-sm'
                : 'btn-outline-light text-white'
            }`}
            onClick={() => setActiveTab('komponen')}
          >
            <i className="fa-solid fa-gears me-1.5"></i> 3. Diagram Komponen Pembangkit
          </button>
        </div>
      </div>

      <div className="card-body p-3 p-md-4">
        {/* ======================================================== */}
        {/* TAB 1: PEMUTAR VIDEO (VIDEO PLAYER)                      */}
        {/* ======================================================== */}
        {activeTab === 'video' && (
          <div className="video-section">
            <div className="row g-3 g-lg-4">
              {/* LEFT COLUMN: MAIN VIDEO PLAYER */}
              <div className="col-12 col-lg-8">
                {/* VIDEO WRAPPER CONTAINER */}
                <div
                  ref={playerContainerRef}
                  className="position-relative bg-black rounded-4 overflow-hidden shadow-lg border border-slate-700"
                  style={{ minHeight: '340px' }}
                >
                  <video
                    ref={videoRef}
                    src={selectedVideo.videoUrl}
                    poster={selectedVideo.thumbnail}
                    className="w-100 h-100 d-block"
                    style={{ maxHeight: '460px', objectFit: 'cover' }}
                    onTimeUpdate={handleTimeUpdate}
                    onLoadedMetadata={handleLoadedMetadata}
                    onEnded={() => setIsPlaying(false)}
                    onClick={handlePlayPause}
                    playsInline
                  />

                  {/* Top Video Overlay Bar */}
                  <div
                    className="position-absolute top-0 start-0 end-0 p-3 d-flex align-items-center justify-content-between"
                    style={{ background: 'linear-gradient(to bottom, rgba(0,0,0,0.85) 0%, transparent 100%)' }}
                  >
                    <div className="d-flex align-items-center gap-2">
                      <span className={`badge ${selectedVideo.badgeColor} rounded-pill px-2.5 py-1 small fw-bold`}>
                        {selectedVideo.categoryBadge}
                      </span>
                      <span className="text-white fw-bold small text-truncate" style={{ maxWidth: '320px' }}>
                        {selectedVideo.title}
                      </span>
                    </div>

                    <span className="badge bg-dark bg-opacity-75 text-cyan-300 border border-slate-700 small px-2 py-0.5 font-monospace">
                      1080p 60fps HD
                    </span>
                  </div>

                  {/* Play Button Overlay on Pause */}
                  {!isPlaying && (
                    <button
                      type="button"
                      className="position-absolute top-50 start-50 translate-middle btn btn-primary rounded-circle p-3 shadow-lg d-flex align-items-center justify-content-center"
                      style={{ width: '68px', height: '68px', background: 'rgba(2, 132, 199, 0.9)', border: '3px solid rgba(255,255,255,0.8)' }}
                      onClick={handlePlayPause}
                      title="Putar Video"
                    >
                      <i className="fa-solid fa-play fs-4 text-white ms-1"></i>
                    </button>
                  )}

                  {/* CUSTOM BOTTOM CONTROL BAR */}
                  <div
                    className="position-absolute bottom-0 start-0 end-0 p-2.5 p-md-3"
                    style={{ background: 'linear-gradient(to top, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.4) 70%, transparent 100%)' }}
                  >
                    {/* Progress Seek Bar */}
                    <div className="d-flex align-items-center gap-2 mb-2">
                      <input
                        type="range"
                        className="form-range custom-video-seek flex-grow-1"
                        min={0}
                        max={duration || selectedVideo.durationSec}
                        step={0.5}
                        value={currentTime}
                        onChange={handleSeek}
                        style={{ cursor: 'pointer' }}
                      />
                    </div>

                    {/* Button Controls Row */}
                    <div className="d-flex align-items-center justify-content-between text-white">
                      {/* Left: Play/Pause, Skip, Time, Volume */}
                      <div className="d-flex align-items-center gap-2 gap-md-3">
                        <button
                          type="button"
                          className="btn btn-sm text-white p-0"
                          onClick={handlePlayPause}
                          title={isPlaying ? 'Jeda' : 'Putar'}
                        >
                          <i className={`fa-solid ${isPlaying ? 'fa-pause' : 'fa-play'} fs-5 text-cyan-400`}></i>
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm text-white p-0"
                          onClick={() => {
                            if (videoRef.current) {
                              videoRef.current.currentTime = Math.max(0, videoRef.current.currentTime - 10);
                            }
                          }}
                          title="Mundur 10 Detik"
                        >
                          <i className="fa-solid fa-rotate-left fs-6 text-slate-300"></i>
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm text-white p-0"
                          onClick={() => {
                            if (videoRef.current) {
                              videoRef.current.currentTime = Math.min(duration, videoRef.current.currentTime + 10);
                            }
                          }}
                          title="Maju 10 Detik"
                        >
                          <i className="fa-solid fa-rotate-right fs-6 text-slate-300"></i>
                        </button>

                        {/* Current Time / Total Duration */}
                        <div className="font-monospace small text-slate-200" style={{ fontSize: '0.78rem' }}>
                          <span className="text-cyan-300">{formatTime(currentTime)}</span> / {formatTime(duration || selectedVideo.durationSec)}
                        </div>

                        {/* Volume Control */}
                        <div className="d-none d-sm-flex align-items-center gap-1.5 ms-2">
                          <button
                            type="button"
                            className="btn btn-sm text-white p-0"
                            onClick={handleToggleMute}
                          >
                            <i className={`fa-solid ${isMuted ? 'fa-volume-xmark text-danger' : volume < 0.5 ? 'fa-volume-low' : 'fa-volume-high'} text-slate-300`}></i>
                          </button>
                          <input
                            type="range"
                            className="form-range"
                            min={0}
                            max={1}
                            step={0.05}
                            value={isMuted ? 0 : volume}
                            onChange={handleVolumeChange}
                            style={{ width: '60px', height: '4px' }}
                          />
                        </div>
                      </div>

                      {/* Right: Playback Speed, Fullscreen */}
                      <div className="d-flex align-items-center gap-2">
                        {/* Speed dropdown buttons */}
                        <div className="dropdown">
                          <button
                            type="button"
                            className="btn btn-sm btn-dark bg-slate-800 text-cyan-300 border border-slate-700 py-0.5 px-2 rounded-pill small font-monospace"
                            data-bs-toggle="dropdown"
                            style={{ fontSize: '0.75rem' }}
                          >
                            {playbackRate}x
                          </button>
                          <ul className="dropdown-menu dropdown-menu-dark dropdown-menu-end shadow-sm small">
                            {[0.5, 0.75, 1, 1.25, 1.5, 2].map((rate) => (
                              <li key={rate}>
                                <button
                                  type="button"
                                  className={`dropdown-item ${playbackRate === rate ? 'active' : ''}`}
                                  onClick={() => handleRateChange(rate)}
                                >
                                  Kecepatan {rate}x
                                </button>
                              </li>
                            ))}
                          </ul>
                        </div>

                        <button
                          type="button"
                          className="btn btn-sm text-white p-0 ms-1"
                          onClick={handleToggleFullscreen}
                          title="Layar Penuh"
                        >
                          <i className={`fa-solid ${isFullscreen ? 'fa-compress' : 'fa-expand'} text-slate-300`}></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                {/* CURRENT VIDEO DETAILS & CHAPTER TIMESTAMPS */}
                <div className="card mt-3 border-0 bg-light rounded-4 p-3 shadow-xs">
                  <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-2">
                    <h5 className="fw-bold text-dark mb-0 fs-6">
                      {selectedVideo.title}
                    </h5>
                    <button
                      type="button"
                      className="btn btn-sm btn-outline-primary rounded-pill px-3 py-1"
                      onClick={() => setShowCustomModal(true)}
                    >
                      <i className="fa-solid fa-link me-1"></i> Putar Video Eksternal
                    </button>
                  </div>
                  <p className="text-secondary small mb-3" style={{ lineHeight: 1.6 }}>
                    {selectedVideo.description}
                  </p>

                  {/* Chapters bookmark timeline */}
                  <div className="border-top pt-2.5">
                    <div className="text-muted fw-bold small mb-2" style={{ fontSize: '0.74rem' }}>
                      <i className="fa-solid fa-bookmark me-1.5 text-primary"></i> TAHAP &amp; CHAPTER PANDUAN (KLIK UNTUK LONCAT):
                    </div>
                    <div className="d-flex flex-wrap gap-1.5">
                      {selectedVideo.chapters.map((ch, idx) => (
                        <button
                          type="button"
                          key={idx}
                          className="btn btn-sm btn-white bg-white border rounded-pill px-2.5 py-1 text-start small shadow-2xs hover-primary"
                          onClick={() => handleJumpToChapter(ch.time)}
                          style={{ fontSize: '0.74rem' }}
                        >
                          <strong className="text-primary">{ch.label.split(' - ')[0]}</strong>
                          <span className="text-secondary ms-1.5">{ch.label.split(' - ')[1]}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Key Takeaways */}
                  <div className="mt-3 bg-white p-3 rounded-3 border">
                    <div className="small fw-bold text-dark mb-1.5">
                      <i className="fa-solid fa-circle-check text-success me-1.5"></i> Poin Kunci Standar Operasional:
                    </div>
                    <ul className="mb-0 ps-3 small text-secondary" style={{ fontSize: '0.78rem' }}>
                      {selectedVideo.keyPoints.map((point, pIdx) => (
                        <li key={pIdx} className="mb-1">{point}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* RIGHT COLUMN: PLAYLIST & CATALOG */}
              <div className="col-12 col-lg-4">
                <div className="d-flex align-items-center justify-content-between mb-2">
                  <div className="small fw-bold text-dark">
                    <i className="fa-solid fa-list-check me-1.5 text-primary"></i> DAFTAR VIDEO PANDUAN ({DEFAULT_VIDEOS.length}):
                  </div>
                  <span className="badge bg-primary-subtle text-primary border small">
                    PJT II Curug
                  </span>
                </div>

                <div className="d-grid gap-2">
                  {DEFAULT_VIDEOS.map((track) => {
                    const isSelected = selectedVideo.id === track.id;
                    return (
                      <div
                        key={track.id}
                        className={`card border transition-all cursor-pointer p-2 rounded-3 ${
                          isSelected
                            ? 'border-primary bg-primary-subtle bg-opacity-30 shadow-xs'
                            : 'bg-white hover-border-primary'
                        }`}
                        onClick={() => handleSelectVideoTrack(track)}
                        style={{ cursor: 'pointer' }}
                      >
                        <div className="d-flex gap-2.5">
                          {/* Thumbnail with duration badge */}
                          <div className="position-relative flex-shrink-0" style={{ width: '90px', height: '62px' }}>
                            <img
                              src={track.thumbnail}
                              alt={track.title}
                              className="w-100 h-100 object-fit-cover rounded-2"
                            />
                            <span
                              className="position-absolute bottom-0 end-0 m-1 badge bg-dark bg-opacity-80 text-white font-monospace"
                              style={{ fontSize: '0.62rem', padding: '2px 4px' }}
                            >
                              {track.duration}
                            </span>
                            {isSelected && (
                              <div
                                className="position-absolute top-50 start-50 translate-middle badge bg-primary rounded-circle p-1"
                              >
                                <i className="fa-solid fa-play text-white" style={{ fontSize: '0.6rem' }}></i>
                              </div>
                            )}
                          </div>

                          {/* Content */}
                          <div className="flex-grow-1 overflow-hidden">
                            <div className="d-flex align-items-center gap-1 mb-1">
                              <span className={`badge ${track.badgeColor} py-0 px-1.5`} style={{ fontSize: '0.62rem' }}>
                                {track.categoryBadge}
                              </span>
                            </div>
                            <div className="fw-bold text-dark small text-truncate-2" style={{ fontSize: '0.78rem', lineHeight: 1.3 }}>
                              {track.title}
                            </div>
                            <div className="text-muted small mt-1" style={{ fontSize: '0.68rem' }}>
                              {track.chapters.length} Tahap Prosedur
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Quick Info Box */}
                <div className="mt-3 p-3 bg-light rounded-3 border">
                  <div className="d-flex align-items-center gap-2 mb-1.5">
                    <i className="fa-solid fa-shield-halved text-success"></i>
                    <strong className="small text-dark">Kepatuhan K3 &amp; Dokumen F-20</strong>
                  </div>
                  <p className="text-secondary small mb-0" style={{ fontSize: '0.74rem', lineHeight: 1.5 }}>
                    Seluruh materi video didasarkan pada SOP resmi Divisi Operasi PJT II. Setiap pengoperasian diwajibkan mencatat log book serta diverifikasi oleh Asisten Manajer Wilayah.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ======================================================== */}
        {/* TAB 2: ANIMASI FISIKA & SKEMATIK INTERAKTIF              */}
        {/* ======================================================== */}
        {activeTab === 'animasi' && (
          <div className="animasi-section">
            <div className="card border-0 bg-dark text-white rounded-4 p-3 shadow-sm mb-3">
              <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
                <div>
                  <h5 className="fw-bold text-white mb-0 fs-6">
                    <i className="fa-solid fa-atom text-cyan-400 me-2"></i>
                    Simulasi Skematik Aliran Air &amp; Turbin Curug (2x3400 kW)
                  </h5>
                  <small className="text-cyan-200" style={{ fontSize: '0.75rem' }}>
                    Visualisasi dinamika fluida dari Intake Bendung Curug (+10.50 m) menuju Penstock, Sudu Turbin Francis, Generator Sinkron, hingga Transmisi GI Curug 70 kV.
                  </small>
                </div>

                {/* Simulation Control Buttons */}
                <div className="d-flex align-items-center gap-2">
                  <button
                    type="button"
                    className={`btn btn-sm ${simRunning ? 'btn-danger' : 'btn-success'} rounded-pill px-3 py-1 font-monospace`}
                    onClick={() => setSimRunning(!simRunning)}
                    style={{ fontSize: '0.76rem' }}
                  >
                    <i className={`fa-solid ${simRunning ? 'fa-pause' : 'fa-play'} me-1`}></i>
                    {simRunning ? 'Jeda Simulasi' : 'Jalankan'}
                  </button>

                  <button
                    type="button"
                    className="btn btn-sm btn-outline-danger rounded-pill px-3 py-1 text-white font-monospace"
                    onClick={handleSimEmergencyTrip}
                    style={{ fontSize: '0.76rem' }}
                    title="Simulasi Emergency Trip"
                  >
                    <i className="fa-solid fa-triangle-exclamation me-1"></i> Trip Darurat
                  </button>

                  <button
                    type="button"
                    className="btn btn-sm btn-outline-info rounded-pill px-3 py-1 text-white font-monospace"
                    onClick={handleSimNormalise}
                    style={{ fontSize: '0.76rem' }}
                  >
                    <i className="fa-solid fa-rotate me-1"></i> Normalisasi
                  </button>
                </div>
              </div>

              {/* CANVAS SIMULATION SCREEN */}
              <div className="position-relative rounded-3 overflow-hidden border border-slate-700 bg-black">
                <canvas
                  ref={canvasRef}
                  width={920}
                  height={380}
                  className="w-100 d-block"
                  style={{ maxHeight: '420px' }}
                />

                {/* Real-time Telemetry Overlay Bar */}
                <div
                  className="position-absolute bottom-0 start-0 end-0 p-2.5 px-3 d-flex flex-wrap align-items-center justify-content-between gap-2"
                  style={{ background: 'rgba(5, 15, 28, 0.88)', backdropFilter: 'blur(8px)', borderTop: '1px solid rgba(56, 189, 248, 0.2)' }}
                >
                  <div className="d-flex align-items-center gap-3">
                    <span className="small text-slate-300">
                      TMA Hulu: <strong className="text-cyan-400 font-monospace">+{waterHead.toFixed(2)} m</strong>
                    </span>
                    <span className="small text-slate-300">
                      Debit Q: <strong className="text-cyan-400 font-monospace">{waterDischarge} m³/s</strong>
                    </span>
                    <span className="small text-slate-300">
                      Putaran Turbin: <strong className="text-warning font-monospace">{turbineRpm} RPM</strong>
                    </span>
                    <span className="small text-slate-300">
                      Daya Listrik: <strong className="text-success font-monospace">{generatorLoadKw} kW</strong>
                    </span>
                  </div>

                  <span className={`badge ${simRunning ? 'bg-success' : 'bg-danger'} px-2.5 py-1 rounded-pill small font-monospace`}>
                    Status: {simRunning ? 'RUNNING NORMAL (SYNCHRONISED)' : 'STOPPED / TRIP'}
                  </span>
                </div>
              </div>

              {/* INTERACTIVE OPERATOR CONTROLS SLIDERS */}
              <div className="row g-3 mt-2">
                <div className="col-12 col-md-3">
                  <div className="p-2.5 rounded-3 bg-slate-900 border border-slate-800">
                    <div className="d-flex justify-content-between text-slate-300 small mb-1">
                      <span>Bukaan Governor Valve:</span>
                      <strong className="text-cyan-400 font-monospace">{valveOpening}%</strong>
                    </div>
                    <div className="d-flex gap-1.5">
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-secondary w-50 py-0.5 text-white"
                        onClick={handleGovernorDecrease}
                        disabled={!simRunning}
                      >
                        <i className="fa-solid fa-minus"></i> Kurang
                      </button>
                      <button
                        type="button"
                        className="btn btn-sm btn-info w-50 py-0.5 text-dark fw-bold"
                        onClick={handleGovernorIncrease}
                        disabled={!simRunning}
                      >
                        <i className="fa-solid fa-plus"></i> Tambah
                      </button>
                    </div>
                  </div>
                </div>

                <div className="col-12 col-md-3">
                  <div className="p-2.5 rounded-3 bg-slate-900 border border-slate-800">
                    <div className="d-flex justify-content-between text-slate-300 small mb-1">
                      <span>Elevasi TMA Hulu:</span>
                      <strong className="text-cyan-400 font-monospace">+{waterHead.toFixed(2)} m</strong>
                    </div>
                    <input
                      type="range"
                      className="form-range"
                      min={8.0}
                      max={12.0}
                      step={0.1}
                      value={waterHead}
                      onChange={(e) => setWaterHead(parseFloat(e.target.value))}
                      disabled={!simRunning}
                    />
                  </div>
                </div>

                <div className="col-12 col-md-3">
                  <div className="p-2.5 rounded-3 bg-slate-900 border border-slate-800">
                    <div className="d-flex justify-content-between text-slate-300 small mb-1">
                      <span>Frekuensi Putaran:</span>
                      <strong className="text-warning font-monospace">{turbineRpm} RPM</strong>
                    </div>
                    <input
                      type="range"
                      className="form-range"
                      min={0}
                      max={550}
                      step={10}
                      value={turbineRpm}
                      onChange={(e) => {
                        const rpm = parseInt(e.target.value);
                        setTurbineRpm(rpm);
                        setGeneratorLoadKw(Math.round((rpm / 500) * 3400));
                      }}
                      disabled={!simRunning}
                    />
                  </div>
                </div>

                <div className="col-12 col-md-3">
                  <div className="p-2.5 rounded-3 bg-slate-900 border border-slate-800">
                    <div className="d-flex justify-content-between text-slate-300 small mb-1">
                      <span>Tegangan Terminal:</span>
                      <strong className="text-success font-monospace">6,3 kV ➔ 70.4 kV</strong>
                    </div>
                    <div className="small text-slate-400 mt-1" style={{ fontSize: '0.72rem' }}>
                      Sinkron busbar Kosambi/JTL aktif
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ======================================================== */}
        {/* TAB 3: DIAGRAM & KOMPONEN TEKNIS                         */}
        {/* ======================================================== */}
        {activeTab === 'komponen' && (
          <div className="komponen-section">
            <div className="row g-3">
              <div className="col-12 col-md-6 col-lg-4">
                <div className="card h-100 border p-3 rounded-4 bg-white shadow-2xs">
                  <div className="d-flex align-items-center gap-2 mb-2">
                    <span className="badge bg-info-subtle text-info border p-2 rounded-circle">
                      <i className="fa-solid fa-fan fs-6"></i>
                    </span>
                    <div>
                      <h6 className="fw-bold text-dark mb-0 fs-6">Runner Turbin Francis</h6>
                      <small className="text-muted">Jantung Penggerak Hidrolik</small>
                    </div>
                  </div>
                  <p className="small text-secondary mb-2" style={{ lineHeight: 1.5 }}>
                    Sudu-sudu turbin jenis reaksi (Francis) berputar pada putaran nominal 500 RPM ketika menerima benturan dan aliran air dari pipa penstock dengan elevasi head efektif Bendung Curug.
                  </p>
                  <div className="mt-auto pt-2 border-top text-muted small" style={{ fontSize: '0.72rem' }}>
                    <i className="fa-solid fa-circle-info text-info me-1"></i> Kapasitas: 3.400 kW per unit
                  </div>
                </div>
              </div>

              <div className="col-12 col-md-6 col-lg-4">
                <div className="card h-100 border p-3 rounded-4 bg-white shadow-2xs">
                  <div className="d-flex align-items-center gap-2 mb-2">
                    <span className="badge bg-primary-subtle text-primary border p-2 rounded-circle">
                      <i className="fa-solid fa-arrows-split-up-and-left fs-6"></i>
                    </span>
                    <div>
                      <h6 className="fw-bold text-dark mb-0 fs-6">Spiral Casing &amp; Guide Vane</h6>
                      <small className="text-muted">Rumah Keong &amp; Pengatur Debit</small>
                    </div>
                  </div>
                  <p className="small text-secondary mb-2" style={{ lineHeight: 1.5 }}>
                    Mendistribusikan air secara merata ke sekeliling runner sudu dengan kecepatan konstan. Bukaan guide vane digerakkan oleh governor hidrolik bertekanan oli 120 bar untuk menjaga kestabilan frekuensi 50.0 Hz.
                  </p>
                  <div className="mt-auto pt-2 border-top text-muted small" style={{ fontSize: '0.72rem' }}>
                    <i className="fa-solid fa-circle-info text-primary me-1"></i> Tekanan Hidrolik: 60/120 bar
                  </div>
                </div>
              </div>

              <div className="col-12 col-md-6 col-lg-4">
                <div className="card h-100 border p-3 rounded-4 bg-white shadow-2xs">
                  <div className="d-flex align-items-center gap-2 mb-2">
                    <span className="badge bg-success-subtle text-success border p-2 rounded-circle">
                      <i className="fa-solid fa-bolt fs-6"></i>
                    </span>
                    <div>
                      <h6 className="fw-bold text-dark mb-0 fs-6">Generator Sinkron 6,3 kV</h6>
                      <small className="text-muted">Konversi Energi Mekanik ke Listrik</small>
                    </div>
                  </div>
                  <p className="small text-secondary mb-2" style={{ lineHeight: 1.5 }}>
                    Rotor kutub menonjol berputar menghasilkan medan magnetik yang menginduksi tegangan 6,3 kV pada stator winding. Dilengkapi sistem pendingin udara dan pelumasan bearing terus menerus.
                  </p>
                  <div className="mt-auto pt-2 border-top text-muted small" style={{ fontSize: '0.72rem' }}>
                    <i className="fa-solid fa-circle-info text-success me-1"></i> Tegangan Generator: 6,3 kV AC
                  </div>
                </div>
              </div>

              <div className="col-12 col-md-6 col-lg-4">
                <div className="card h-100 border p-3 rounded-4 bg-white shadow-2xs">
                  <div className="d-flex align-items-center gap-2 mb-2">
                    <span className="badge bg-warning-subtle text-warning border p-2 rounded-circle">
                      <i className="fa-solid fa-cubes fs-6"></i>
                    </span>
                    <div>
                      <h6 className="fw-bold text-dark mb-0 fs-6">Cubicle LGB001JD &amp; PMT</h6>
                      <small className="text-muted">Panel Sinkronisasi &amp; Interkoneksi</small>
                    </div>
                  </div>
                  <p className="small text-secondary mb-2" style={{ lineHeight: 1.5 }}>
                    Cubicle gardu penghubung antara unit generator turbin mini hydro dengan sistem gardu induk. Mengandung breaker pemutus vakum/SF6 dan synchroscope otomatis.
                  </p>
                  <div className="mt-auto pt-2 border-top text-muted small" style={{ fontSize: '0.72rem' }}>
                    <i className="fa-solid fa-circle-info text-warning me-1"></i> Standar SOP: F-20/DPL/IK.10-01
                  </div>
                </div>
              </div>

              <div className="col-12 col-md-6 col-lg-4">
                <div className="card h-100 border p-3 rounded-4 bg-white shadow-2xs">
                  <div className="d-flex align-items-center gap-2 mb-2">
                    <span className="badge bg-danger-subtle text-danger border p-2 rounded-circle">
                      <i className="fa-solid fa-tower-broadcast fs-6"></i>
                    </span>
                    <div>
                      <h6 className="fw-bold text-dark mb-0 fs-6">Trafo Utama 6,3 / 70 kV</h6>
                      <small className="text-muted">Step-Up Transmisi Tegangan Tinggi</small>
                    </div>
                  </div>
                  <p className="small text-secondary mb-2" style={{ lineHeight: 1.5 }}>
                    Menaikkan tegangan dari 6,3 kV ke 70 kV untuk efisiensi penyaluran jarak jauh ke Gardu Induk Curug dan jaringan interkoneksi Jatiluhur - Kosambi PLN.
                  </p>
                  <div className="mt-auto pt-2 border-top text-muted small" style={{ fontSize: '0.72rem' }}>
                    <i className="fa-solid fa-circle-info text-danger me-1"></i> Proteksi: Relai Buchholz &amp; Diferensial
                  </div>
                </div>
              </div>

              <div className="col-12 col-md-6 col-lg-4">
                <div className="card h-100 border p-3 rounded-4 bg-white shadow-2xs">
                  <div className="d-flex align-items-center gap-2 mb-2">
                    <span className="badge bg-secondary-subtle text-secondary border p-2 rounded-circle">
                      <i className="fa-solid fa-water fs-6"></i>
                    </span>
                    <div>
                      <h6 className="fw-bold text-dark mb-0 fs-6">Draft Tube &amp; Saluran Tailrace</h6>
                      <small className="text-muted">Pelepasan Air ke Sungai Citarum</small>
                    </div>
                  </div>
                  <p className="small text-secondary mb-2" style={{ lineHeight: 1.5 }}>
                    Mengurangi kecepatan air buangan yang keluar dari turbin dan mengembalikan energi sisa (regaining velocity head) sebelum dialirkan kembali ke hilir Bendung Curug (+2.10 m).
                  </p>
                  <div className="mt-auto pt-2 border-top text-muted small" style={{ fontSize: '0.72rem' }}>
                    <i className="fa-solid fa-circle-info text-secondary me-1"></i> Elevasi Hilir Curug: +2.10 m
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* MODAL INPUT VIDEO EKSTERNAL */}
      {showCustomModal && (
        <div
          className="modal fade show d-block"
          tabIndex={-1}
          style={{ backgroundColor: 'rgba(0,0,0,0.65)', backdropFilter: 'blur(4px)' }}
        >
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content rounded-4 border-0 shadow-lg">
              <div className="modal-header border-bottom py-3">
                <h6 className="modal-title fw-bold text-dark">
                  <i className="fa-solid fa-link text-primary me-2"></i> Muat Video Panduan Kustom
                </h6>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowCustomModal(false)}
                ></button>
              </div>
              <div className="modal-body p-4">
                <p className="small text-secondary mb-3">
                  Masukkan URL langsung berkas video (MP4, WebM) dari dokumentasi perusahaan PJT II, server intranet, atau cloud storage:
                </p>
                <div className="mb-3">
                  <label className="form-label small fw-bold text-dark">URL Video (MP4 / WebM):</label>
                  <input
                    type="url"
                    className="form-control rounded-3"
                    placeholder="https://example.com/video-panduan-plta-curug.mp4"
                    value={customVideoUrl}
                    onChange={(e) => setCustomVideoUrl(e.target.value)}
                  />
                  <div className="form-text small" style={{ fontSize: '0.72rem' }}>
                    Mendukung link langsung CDN, Google Cloud Storage, atau video internal PJT II.
                  </div>
                </div>
              </div>
              <div className="modal-footer border-top py-2.5">
                <button
                  type="button"
                  className="btn btn-sm btn-light border rounded-pill px-3"
                  onClick={() => setShowCustomModal(false)}
                >
                  Batal
                </button>
                <button
                  type="button"
                  className="btn btn-sm btn-primary rounded-pill px-4"
                  onClick={handleApplyCustomUrl}
                  disabled={!customVideoUrl.trim()}
                >
                  <i className="fa-solid fa-play me-1.5"></i> Muat ke Pemutar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
