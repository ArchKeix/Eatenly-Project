document.getElementById('registerForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  if (password !== confirmPassword) {
    alert('Password dan konfirmasi tidak sama!');
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
        confirm_password: confirmPassword
      }),
    });

    const data = await response.json();

    if (response.ok) {
      alert('Registrasi berhasil untuk ' + data.email );
      window.location.href = 'personalisasi.html';
    } else {
      alert('Error: ' + (data.detail || JSON.stringify(data)));
    }
  } catch (error) {
    console.error(error);
    alert('Terjadi kesalahan koneksi ke server.');
  }
});
