# ----------------------------------------------------------------------- #
#                               LIBRARIES                                 #
# ----------------------------------------------------------------------- #

import streamlit as st
import requests
from dotenv import load_dotenv
import os

# ----------------------------------------------------------------------- #
# Load .env
load_dotenv()

# Get Backend URL dari .env
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
                f"{BACKEND_URL}/upload-image", files=files, timeout=30
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

st.title("One Scan Analysis")
enable_camera = st.checkbox("Aktifkan kamera untuk scan produk")
scan_input = st.camera_input(
    "Ambil foto produk menggunakan kamera",
    disabled=not enable_camera,
)
if scan_input is not None:
    st.image(scan_input, caption="Gambar yang di-scan")
    img_byts = scan_input.getvalue()
    files = {"file": (scan_input.name, img_byts, scan_input.type)}
    try:
        response = requests.post(
            f"{BACKEND_URL}/scan-image",
            files=files,
            timeout=30,
        )

        if response.status_code == 200:
            result_dict = response.json()
            st.success("Analisis selesai!")
            st.write("Hasil Analisis:")
            st.write(result_dict.get("analysis_result"))

        else:
            result_dict = response.json()
            st.error(f"Analisis Gagal: {result_dict.get('message')}")
            st.write("----- DEBUG START -----")
            st.write("DEBUG TYPE:", type(scan_input))
            st.write("DEBUG RAW OBJECT:", scan_input)
            st.write("DEBUG MIME:", scan_input.type)
            st.write("DEBUG FILENAME:", scan_input.name)
            st.write("DEBUG BYTES LEN:", len(scan_input.getvalue()))
            st.write(
                "DEBUG REQUEST FILES:",
                {
                    "filename": "camera.jpg",
                    "mime": scan_input.type,
                    "size": len(scan_input.getvalue()),
                },
            )
            st.write("----- DEBUG END -----")

    except requests.exceptions.RequestException as e:
        st.error(f"Gagal terhubung ke server Backend: {e}")
