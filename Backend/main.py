from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from services_ai import AI_Analyst

app = FastAPI()


@app.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    try:
        # Baca file gambar yang diupload
        img_bytes = file.file.read()

        analysis_result = AI_Analyst(img_bytes)

        # Kembalikan hasil analisis sebagai respons JSON
        return JSONResponse(
            content={
                "status": "success",
                "analysis_result": analysis_result.get("analysis"),
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Analisis gagal: {e}"},
        )
