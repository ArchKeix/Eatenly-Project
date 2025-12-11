document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    // Payload sesuai UserLogin (email, password)
    const payload = {
      email: email,
      password: password,
    };

    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || 'Login gagal');
        return;
      }

      // Simpan token & id_user ke localStorage
      localStorage.setItem('token', data.token);
      localStorage.setItem('id_user', data.id_user);

      // (Opsional) simpan data user lain
      localStorage.setItem('nama_panggilan', data.nama_panggilan || '');
      localStorage.setItem('umur', data.umur || '');
      localStorage.setItem('jenis_kelamin', data.jenis_kelamin || '');
      localStorage.setItem('riwayat_penyakit', data.riwayat_penyakit || '');
      localStorage.setItem('preferensi', data.preferensi || '');

      alert('Login berhasil!');

      // Redirect ke dashboard
      window.location.href = 'dashboard.html';
    } catch (error) {
      console.error('Error: ', error);
      alert('Terjadi kesalahan pada server.');
    }
  });
});
