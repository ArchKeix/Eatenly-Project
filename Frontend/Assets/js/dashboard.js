// =======================================================
// 1. LOGIKA UTAMA (LOAD SAAT DOM SIAP)
// =======================================================
document.addEventListener('DOMContentLoaded', () => {
    
    // A. CEK AUTH (Jaga Pintu)
    const token = localStorage.getItem('token');
    const idUser = localStorage.getItem('id_user');

    if (!token || !idUser) {
        alert("Sesi habis. Silakan login kembali.");
        window.location.href = '../pages/login.html';
        return;
    }

    // B. LOAD DATA PROFIL (Nama, Umur, Penyakit)
    // Fungsi ini akan mengisi data dari LocalStorage dulu, lalu update dari Backend
    loadUserData(idUser);

    // C. LOAD RIWAYAT SCAN (DARI DATABASE) 🔥
    loadRiwayatFromBackend();

    // D. LOGOUT LISTENER
    const logoutBtn = document.querySelector('.logout-link');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault(); 
            localStorage.clear(); 
            window.location.href = '../../index.html'; 
        });
    }
});

// =======================================================
// 2. FUNGSI LOAD DATA PROFIL (GET /personalize)
// =======================================================
async function loadUserData(idUser) {
    // 1. Tampilkan dulu data dari LocalStorage (biar cepat)
    renderUserProfile({
        nama_panggilan: localStorage.getItem('nama_panggilan'),
        umur: localStorage.getItem('umur'),
        jenis_kelamin: localStorage.getItem('jenis_kelamin'),
        riwayat_penyakit: localStorage.getItem('riwayat_penyakit'),
        preferensi: localStorage.getItem('preferensi')
    });

    // 2. Fetch data terbaru dari Backend (Background Update)
    try {
        const response = await fetch(`http://localhost:8000/personalize/${idUser}`);
        if (response.ok) {
            const data = await response.json();
            
            // Update Tampilan dengan data baru
            renderUserProfile(data);

            // Update LocalStorage agar sinkron
            if(data.nama_panggilan) localStorage.setItem('nama_panggilan', data.nama_panggilan);
            if(data.umur) localStorage.setItem('umur', data.umur);
            if(data.jenis_kelamin) localStorage.setItem('jenis_kelamin', data.jenis_kelamin);
            if(data.riwayat_penyakit) localStorage.setItem('riwayat_penyakit', data.riwayat_penyakit);
            if(data.preferensi) localStorage.setItem('preferensi', data.preferensi);
        }
    } catch (err) {
        console.log("Mode Offline atau Gagal Fetch Profil: Menggunakan data cache lokal.");
    }
}

function renderUserProfile(data) {
    // Helper untuk menampilkan data ke elemen HTML
    if(document.getElementById('displayNamaHeader')) {
        document.getElementById('displayNamaHeader').innerText = (data.nama_panggilan && data.nama_panggilan !== 'undefined') ? data.nama_panggilan : "User";
    }
    if(document.getElementById('displayUmur')) {
        document.getElementById('displayUmur').innerText = (data.umur && data.umur !== 'null') ? data.umur + " TAHUN" : "-";
    }
    if(document.getElementById('displayGender')) {
        document.getElementById('displayGender').innerText = (data.jenis_kelamin && data.jenis_kelamin !== 'null') ? data.jenis_kelamin.toUpperCase() : "-";
    }
    
    // Render List Penyakit & Preferensi
    renderListLimit('displayPenyakitContainer', 'btnShowPenyakit', data.riwayat_penyakit);
    renderListLimit('displayPreferensiContainer', 'btnShowPreferensi', data.preferensi);
}

// =======================================================
// 3. FUNGSI LOAD RIWAYAT (GET /ai/history)
// =======================================================
async function loadRiwayatFromBackend() {
    const token = localStorage.getItem('token');
    const wrapper = document.querySelector('.swiper-wrapper');
    if (!wrapper) return;

    wrapper.innerHTML = ''; // Bersihkan container sebelum diisi

    try {
        const response = await fetch('http://localhost:8000/ai/history', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        // Cek apakah ada datanya (result.data)
        if (response.ok && result.data && result.data.length > 0) {
            renderSwiperSlides(result.data);
        } else {
            // Tampilan jika riwayat kosong
            wrapper.innerHTML = `
                <div class="swiper-slide" style="display:flex; justify-content:center; align-items:center; height:100%;">
                    <p style="text-align:center; color:#fff; font-size:12px; opacity:0.8;">Belum ada riwayat scan.</p>
                </div>`;
        }
    } catch (error) {
        console.error("Gagal mengambil riwayat:", error);
        wrapper.innerHTML = `<p style="color:white; text-align:center; font-size:12px; padding:20px;">Gagal memuat data riwayat.</p>`;
    }
}

function renderSwiperSlides(dataList) {
    const wrapper = document.querySelector('.swiper-wrapper');
    
    // LOGIKA CHUNKING: Bagi data jadi halaman-halaman (1 halaman isi 2 kartu)
    for (let i = 0; i < dataList.length; i += 2) {
        
        // 1. Buat Container Slide (Halaman)
        const slide = document.createElement('div');
        slide.className = 'swiper-slide';

        // 2. Ambil potongan 2 data
        const chunk = dataList.slice(i, i + 2);

        // 3. Masukkan kartu-kartu ke dalam Slide
        chunk.forEach(item => {
            // Mapping key sesuai database python (route_ai.py)
            const title = item.nama_produk || 'Produk';
            const rekomen = item.rekomendasi_produk || '-';
            const halal = item.status_halal || '-';

            const card = document.createElement('div');
            card.className = 'history-card';
            card.innerHTML = `
                <h4>${title}</h4>
                <p>Rekomen: ${rekomen}</p>
                <p>Status: ${halal}</p>
            `;
            slide.appendChild(card);
        });

        wrapper.appendChild(slide);
    }

    // 4. INISIALISASI ULANG SWIPER
    // Kita destroy dulu yang lama biar ga error/double
    if (window.myHistorySwiper instanceof Swiper) {
        window.myHistorySwiper.destroy(true, true);
    }

    window.myHistorySwiper = new Swiper(".myHistorySwiper", {
        slidesPerView: 1,       // 1 Halaman penuh
        spaceBetween: 20,       // Jarak antar halaman
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        watchOverflow: true, 
    });
}

// =======================================================
// 4. FUNGSI UPLOAD & SCAN (POST /ai/)
// =======================================================
const scanModal = document.getElementById('scanModal');
function openScanModal() { if(scanModal) scanModal.style.display = 'flex'; }
function closeScanModal() { if(scanModal) scanModal.style.display = 'none'; }
window.onclick = function(event) { if (event.target == scanModal) closeScanModal(); };

function triggerCamera() { document.getElementById('cameraInput').click(); }
function triggerGallery() { document.getElementById('galleryInput').click(); }

async function handleFileSelect(input) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        closeScanModal();

        const resultSection = document.getElementById('analysisResult');
        const resultText = document.getElementById('resultText');
        const previewImage = document.getElementById('previewImage');

        if(resultSection) resultSection.style.display = 'block';
        if(previewImage) previewImage.src = URL.createObjectURL(file);
        
        // Scroll ke hasil
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

        if(resultText) {
            resultText.innerHTML = "⏳ <b>Sedang menganalisis...</b><br>Mohon tunggu sebentar";
            resultText.style.color = "#666";
        }

        const formData = new FormData();
        formData.append('img_product', file);
        const token = localStorage.getItem('token');

        try {
            const response = await fetch('http://localhost:8000/ai/', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData 
            });
            
            const data = await response.json();

            if (response.ok) {
                // 1. Tampilkan Hasil Analisis Teks
                let formatted = formatAIResponse(data.analysis);
                resultText.innerHTML = `✅ <b>Hasil Analisis:</b><br>${formatted}`;
                resultText.style.color = ""; // Reset warna agar class CSS jalan

                // 2. REFRESH RIWAYAT SCAN OTOMATIS 🔥
                // Kita beri delay 1 detik agar database selesai menyimpan
                setTimeout(() => {
                    loadRiwayatFromBackend();
                }, 1000);

            } else {
                resultText.innerHTML = `❌ Gagal: ${data.detail || "Error"}`;
                resultText.style.color = "red";
            }
        } catch (error) {
            console.error(error);
            resultText.innerHTML = "❌ Error Koneksi Server";
            resultText.style.color = "red";
        }
    }
}

// =======================================================
// 5. HELPER LAINNYA (Render List & Format Teks)
// =======================================================
function renderListLimit(containerId, buttonId, dataString) {
    const container = document.getElementById(containerId);
    const button = document.getElementById(buttonId);
    if (!container || !button) return;
    
    container.innerHTML = '';
    
    if (!dataString || dataString === 'null' || dataString === '-' || dataString === '') {
        container.innerHTML = '<span class="value-large">-</span>';
        button.style.display = 'none';
        return;
    }

    const items = dataString.split(',').map(item => item.trim()).filter(i => i);
    items.forEach((itemText, index) => {
        const div = document.createElement('div');
        div.className = 'list-item';
        div.innerText = itemText;
        if (index >= 3) div.classList.add('hidden-item');
        container.appendChild(div);
    });

    if (items.length > 3) {
        button.style.display = 'inline';
        button.innerText = 'Show all';
        
        const newBtn = button.cloneNode(true);
        button.parentNode.replaceChild(newBtn, button);
        
        newBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const hiddenItems = container.querySelectorAll('.hidden-item, .revealed-item');
            const isExpanding = newBtn.innerText === 'Show all';
            hiddenItems.forEach(item => {
                if (isExpanding) {
                    item.classList.remove('hidden-item');
                    item.classList.add('revealed-item');
                } else {
                    item.classList.add('hidden-item');
                    item.classList.remove('revealed-item');
                }
            });
            newBtn.innerText = isExpanding ? 'Show less' : 'Show all';
        });
    } else {
        button.style.display = 'none';
    }
}

function formatAIResponse(text) {
    if (!text) return "";
    let formatted = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    formatted = formatted.replace(/\*(.*?)\*/g, '<b>$1</b>');
    formatted = formatted.replace(/Halal/gi, '<span class="status-green">Halal</span>');
    formatted = formatted.replace(/Haram/gi, '<span class="status-red">Haram</span>');
    formatted = formatted.replace(/Tidak disarankan/gi, '<span class="status-red">Tidak disarankan</span>');
    formatted = formatted.replace(/Direkomendasikan/gi, '<span class="status-green">Direkomendasikan</span>');
    return formatted;
}