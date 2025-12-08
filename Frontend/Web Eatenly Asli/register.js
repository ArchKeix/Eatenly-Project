document.getElementById('registerForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  if (password !== confirmPassword) {
    alert('Password tidak sama!');
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        username: email.split('@')[0],
        password: password,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      alert('Registrasi berhasil untuk ' + data.email);
      window.location.href = 'personalisasi.html';
    } else {
      let errorMessage = '';
      try {
        const error = await response.json();
        errorMessage = error.detail || JSON.stringify(error);
      } catch (parseErr) {
        errorMessage = 'Tidak bisa membaca error dari server.';
      }
      alert('Error: ' + errorMessage);
    }
  } catch (error) {
    console.error(error);
    alert('Terjadi kesalahan koneksi ke server.');
  }
});
