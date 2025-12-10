// --- LOGIKA MODAL ---
const scanModal = document.getElementById('scanModal');

function openScanModal() {
    scanModal.style.display = 'flex';
}

function closeScanModal() {
    scanModal.style.display = 'none';
}

// Menutup modal saat klik di luar kotak putih
window.onclick = function(event) {
    if (event.target == scanModal) {
        closeScanModal();
    }
}

// --- Logika Pemilihan File ---

//1. Jika tombol 'Ambil Foto/Gambar' diklik maka akan men trigger input Kamera
function triggerCamera() {
    document.getElementById('cameraInput').click();
}

//2. Jika tombol 'Upload file' diklik maka akan men trigger input galeri
function triggerGallery() {
    document.getElementById('galleryInput').click();
}

// Logika utama (Setelah Foto Dipilih)
function handleFileSelect(input) {
    //cek apakah user benar-benar memilih file
    if (input.files && input.files[0]) {
        const file = input.files[0];

        // tutup modal dlu
        closeScanModal();

        // Tampilkan Section Hasil (Simulasi Loading)
        const resultSection = document.getElementById('analysisResult');
        const resultText = document.getElementById('resultText');
        const previewImage = document.getElementById('previewImage');

        // 1. Munculkan Section
        resultSection.style.display = 'block';

        // 2. Tampilkan Preview Gambar User
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
        }
        reader.readAsDataURL(file);

        // 3. Status Loading
        resultText.innerHTML = "⏳ Sedang menganalisis foto dengan AI...";
        resultText.style.color = "666";

        // Scroll ke hasil
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // --- BAGIAN INTEGRASI BACKEND ---
        // Mengirim 'file' ke Python/MongoDB di sini.
        // Makai setTimeout untuk simulasi.

        setTimeout(() => {
            // Simulasi Hasil Sukses dari Backend
            resultText.innerHTML = "✅ <b>Hasil Analisis:</b><br>Makanan ini <b>Cocok</b> untukmu! Kandungan gulanya rendah, aman untuk riwayat diabetesmu.";
            resultText.style.color = "#333";
            
            // Scroll otomatis ke hasil agar user sadar
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
        }, 3000); // Simulasi loading 3 detik
    }
}