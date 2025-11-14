# Di dalam Frontend/app.py (Contoh)

import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

st.title("Upload Gambar & Analisis AI")
uploaded_file = st.file_uploader("Pilih gambar...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)

    if st.button("Analisis Gambar"):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

        # Kirim "telepon" ke backend
        try:
            response = requests.post(
                f"{BACKEND_URL}/upload-image", files=files, timeout=180
            )

            # Cek status code HTTP-nya
            if response.status_code == 200:
                # Ini berarti Koki SUKSES
                result_dict = response.json()
                st.success("Analisis selesai!")

                # Tampilkan HANYA HASILNYA saja
                st.write("Hasil Analisis:")
                st.write(result_dict.get("analysis_result"))

            else:
                # Ini berarti Koki GAGAL (status 500)
                # atau Frontend salah kirim (status 400)
                result_dict = response.json()
                st.error(f"Analisis Gagal: {result_dict.get('message')}")

        except requests.exceptions.RequestException as e:
            # Ini jika server FastAPI-nya MATI
            st.error(f"Gagal terhubung ke server Backend: {e}")
