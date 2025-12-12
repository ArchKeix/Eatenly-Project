// =======================================================
// 1. LOGIKA USER DATA (PERSONALISASI) & AUTH
// =======================================================
document.addEventListener('DOMContentLoaded', () => {
    
    // A. CEK TOKEN / ID_USER (Security Check)
    const token = localStorage.getItem('token');
    const idUser = localStorage.getItem('id_user');

    if (!token || !idUser) {
        alert("Sesi habis atau belum login. Silakan login kembali.");
        window.location.href = '../pages/login.html';
        return;
    }

    // B. AMBIL DATA DARI LOCALSTORAGE
    const nama = localStorage.getItem('nama_panggilan');
    const umur = localStorage.getItem('umur');
    const gender = localStorage.getItem('jenis_kelamin');
    const penyakit = localStorage.getItem('riwayat_penyakit');
    const preferensi = localStorage.getItem('preferensi');

    // C. TEMPEL DATA KE HTML
    
    // 1. Header Sapaan
    const headerNama = document.getElementById('displayNamaHeader');
    if (headerNama) {
        headerNama.innerText = (nama && nama !== "undefined" && nama !== "null") ? nama : "User";
    }

    // 2. Kartu Umur
    const displayUmur = document.getElementById('displayUmur');
    if (displayUmur) {
        displayUmur.innerText = (umur && umur !== "null") ? umur + " TAHUN" : "-";
    }

    // 3. Kartu Gender
    const displayGender = document.getElementById('displayGender');
    if (displayGender) {
        displayGender.innerText = (gender && gender !== "null") ? gender.toUpperCase() : "-";
    }

    // 4. Kartu Penyakit & Preferensi (PAKAI FUNGSI BARU 'renderListLimit')
    renderListLimit('displayPenyakitContainer', 'btnShowPenyakit', penyakit);
    renderListLimit('displayPreferensiContainer', 'btnShowPreferensi', preferensi);

    // D. BACKGROUND UPDATE
    updateDataBackground(idUser);

    // E. FITUR LOGOUT
    const logoutBtn = document.querySelector('.logout-link');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.clear(); 
            window.location.href = '../../index.html';
        });
    }
});

// --- FUNGSI UPDATE DATA BACKGROUND ---
async function updateDataBackground(idUser) {
    try {
        const response = await fetch(`http://localhost:8000/personalize/${idUser}`);
        if(response.ok) {
            const data = await response.json();
            
            // Update Tampilan Biasa
            if(data.nama_panggilan) document.getElementById('displayNamaHeader').innerText = data.nama_panggilan;
            if(data.umur) document.getElementById('displayUmur').innerText = data.umur + " TAHUN";
            if(data.jenis_kelamin) document.getElementById('displayGender').innerText = data.jenis_kelamin.toUpperCase();
            
            // Update Tampilan List (Penyakit & Preferensi)
            renderListLimit('displayPenyakitContainer', 'btnShowPenyakit', data.riwayat_penyakit);
            renderListLimit('displayPreferensiContainer', 'btnShowPreferensi', data.preferensi);

            // Update LocalStorage
            localStorage.setItem('nama_panggilan', data.nama_panggilan || '');
            localStorage.setItem('umur', data.umur || '');
            localStorage.setItem('jenis_kelamin', data.jenis_kelamin || '');
            localStorage.setItem('riwayat_penyakit', data.riwayat_penyakit || '');
            localStorage.setItem('preferensi', data.preferensi || '');
        }
    } catch (err) {
        console.log("Mode Offline: Menggunakan data dari cache lokal.");
    }
}

// =======================================================
// 🔥 FUNGSI BARU: RENDER LIST DENGAN LIMIT & SHOW ALL
// =======================================================
function renderListLimit(containerId, buttonId, dataString) {
    const container = document.getElementById(containerId);
    const button = document.getElementById(buttonId);

    if (!container || !button) return;

    // Reset isi container
    container.innerHTML = '';

    // Cek jika data kosong
    if (!dataString || dataString === "null" || dataString === "-" || dataString.trim() === "") {
        container.innerHTML = '<span class="value-large">-</span>';
        button.style.display = 'none';
        return;
    }

    // 1. Pecah String jadi Array (Pemisah koma)
    // Contoh: "Diabetes, Asma, Jantung, Ginjal" -> ["Diabetes", "Asma", "Jantung", "Ginjal"]
    const items = dataString.split(',').map(item => item.trim()).filter(item => item !== "");

    // 2. Loop dan buat elemen HTML
    items.forEach((itemText, index) => {
        const div = document.createElement('div');
        div.className = 'list-item'; 
        div.innerText = itemText;

        // Jika urutan ke-4 dst (index > 2), sembunyikan
        if (index >= 3) {
            div.classList.add('hidden-item'); 
        }

        container.appendChild(div);
    });

    // 3. Logika Tombol Show All
    if (items.length > 3) {
        button.style.display = 'inline'; // Munculkan tombol
        button.innerText = 'Show all';
        
        // Clone button untuk reset event listener (agar tidak numpuk event klik)
        const newBtn = button.cloneNode(true);
        button.parentNode.replaceChild(newBtn, button);

        newBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const hiddenItems = container.querySelectorAll('.hidden-item, .revealed-item');
            
            // Cek status saat ini (Apakah sedang Show All atau Show Less?)
            const isExpanding = newBtn.innerText === 'Show all';

            hiddenItems.forEach(item => {
                if (isExpanding) {
                    // Tampilkan item
                    item.classList.remove('hidden-item');
                    item.classList.add('revealed-item'); 
                } else {
                    // Sembunyikan item lagi
                    item.classList.add('hidden-item');
                    item.classList.remove('revealed-item');
                }
            });

            // Ubah teks tombol
            newBtn.innerText = isExpanding ? 'Show less' : 'Show all';
        });

    } else {
        // Kalau item cuma 3 atau kurang, sembunyikan tombol
        button.style.display = 'none';
    }
}


// =======================================================
// 2. LOGIKA MODAL SCAN & KAMERA (TETAP SAMA)
// =======================================================

const scanModal = document.getElementById('scanModal');

function openScanModal() {
    if(scanModal) scanModal.style.display = 'flex';
}

function closeScanModal() {
    if(scanModal) scanModal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == scanModal) {
        closeScanModal();
    }
}

function triggerCamera() {
    const cameraInput = document.getElementById('cameraInput');
    if(cameraInput) cameraInput.click();
}

function triggerGallery() {
    const galleryInput = document.getElementById('galleryInput');
    if(galleryInput) galleryInput.click();
}

async function handleFileSelect(input) {
    
    // Cek apakah user benar-benar memilih file
    if (input.files && input.files[0]) {
        const file = input.files[0];

        // 1. Tutup modal
        closeScanModal();

        // 2. Ambil elemen HTML
        const resultSection = document.getElementById('analysisResult');
        const resultText = document.getElementById('resultText');
        const previewImage = document.getElementById('previewImage');

        // 3. Munculkan Section Hasil
        if(resultSection) resultSection.style.display = 'block';

        // 4. Tampilkan Preview Gambar (FileReader)
        const reader = new FileReader();
        reader.onload = function(e) {
            if(previewImage) previewImage.src = e.target.result;
        }
        reader.readAsDataURL(file);

        // 5. Set Status Loading
        if(resultText) {
            resultText.innerHTML = "⏳ <b>Sedang menganalisis dengan AI...</b><br>Mohon tunggu sebentar";
            resultText.style.color = "#666";
        }

        // 6. Scroll otomatis ke bagian hasil
        if(resultSection) {
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        // ============================================================
        // 7. INTEGRASI BACKEND
        // ============================================================
        
        const formData = new FormData();

        formData.append('img_product', file); 
        
        // Ambil token dari login
        const token = localStorage.getItem('token');

        try {
            const response = await fetch('http://localhost:8000/ai/', { // Tambah slash di akhir biar aman
                method: 'POST',
                headers: {
                    
                    'Authorization': `Bearer ${token}`
                    // Note: Jangan set 'Content-Type', biar browser yang atur boundary FormData
                },
                body: formData 
            });

            const data = await response.json();

            if (response.ok) {
                if(resultText) {
                    // Tampilkan hasil analisis
                    // Pastikan key 'analysis' sesuai dengan return backend: "analysis": answer["analysis"]
                    resultText.innerHTML = `✅ <b>Hasil Analisis:</b><br>${data.analysis}`;
                    resultText.style.color = "#333";
                }
            } else {
                if(resultText) {
                    // Tampilkan pesan error spesifik dari backend jika ada
                    const pesanError = data.detail || 'Terjadi kesalahan saat analisis.';
                    resultText.innerHTML = `❌ <b>Gagal:</b><br>${pesanError}`;
                    resultText.style.color = "red";
                    console.error("Backend Error:", data);
                }
            }

        } catch (error) {
            console.error("Error upload:", error);
            if(resultText) {
                resultText.innerHTML = "❌ <b>Error Koneksi:</b><br>Gagal menghubungi server.";
                resultText.style.color = "red";
            }
        }
    }
}

// =======================================================
// 🛠️ FUNGSI FORMATTER TEXT (Markdown to HTML)
// =======================================================
function formatAIResponse(text) {
    if (!text) return "";

    // 1. Ubah **Teks Tebal** menjadi <b>Teks Tebal</b>
    let formatted = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

    // 2. Ubah *Teks Tebal* (format lain) menjadi <b>Teks Tebal</b>
    formatted = formatted.replace(/\*(.*?)\*/g, '<b>$1</b>');

    // 3. (Opsional) Beri warna pada kata "Halal" atau "Haram"
    formatted = formatted.replace(/Halal/gi, '<span style="color: green; font-weight:bold;">Halal</span>');
    formatted = formatted.replace(/Haram/gi, '<span style="color: red; font-weight:bold;">Haram</span>');

    return formatted;
}