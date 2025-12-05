# ----------------------------------------------------------------------- #
#                               LIBRARIES                                 #
# ----------------------------------------------------------------------- #

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from services_ai import AI_Analyst
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

# ----------------------------------------------------------------------- #
# Bangun FastAPI app
app = FastAPI()

# Buat CORS Middleware sebagai izin akses komunikasi dari Frontend ke Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Buat endpoint untuk upload image
@app.post("/upload-image")

# Define fungsi upload image
def upload_image(file: UploadFile = File(...)):
    try:
        # Baca file gambar yang diupload
        img_bytes = file.file.read()

        # Hasil analisis
        analysis_result = AI_Analyst(img_bytes)

        # Return hasil analisis dalam bentuk JSON
        return JSONResponse(
            content={
                "status": "success",
                "analysis_result": analysis_result.get("analysis"),
            }
        )

    except Exception as e:
        # Jika terjadi error, kembalikan pesan error
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Analisis gagal: {e}"},
        )


@app.post("/scan-image")
async def scan_image(file: UploadFile = File(...)):
    try:

        # Baca file gambar yang diupload
        img_bytes = await file.read()
        # Debug ukuran (SANGAT PENTING)
        print("File size:", len(img_bytes), "bytes")
        print("MIME:", file.content_type)
        # Hasil analisis
        analysis_result = AI_Analyst(img_bytes)

        # Return hasil analisis dalam bentuk JSON
        return JSONResponse(
            content={
                "status": "success",
                "analysis_result": analysis_result.get("analysis"),
            }
        )

    except Exception as e:
        # Jika terjadi error, kembalikan pesan error
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Analisis gagal: {e}"},
        )
