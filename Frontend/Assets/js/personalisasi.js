document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('personal-form');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const payload = {
      nama_panggilan: document.getElementById('nama-panggilan').value,
      jenis_kelamin: document.getElementById('jenis-kelamin').value,
      umur: document.getElementById('umur').value,
      riwayat_penyakit: document.getElementById('riwayat-penyakit').value,
      preferensi: document.getElementById('preferensi').value,
    };

    try {
      const id_user = localStorage.getItem('id_user');

      if (!id_user) {
        alert('ID User tidak ditemukan. Silakan regist terlebih dahulu.');
        return;
      }

      const response = await fetch(`http://localhost:8000/personalize/${id_user}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        alert('Preferensi berhasil disimpan untuk ' + payload.nama_panggilan);
        window.location.href = 'login.html';
      } else {
        alert('Error: ' + (data.detail || JSON.stringify(data)));
      }
    } catch (error) {
      console.error(error);
      alert('Terjadi kesalahan koneksi ke server.');
    }
  });
});
