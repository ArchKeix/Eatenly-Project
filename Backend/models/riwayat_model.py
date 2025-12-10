from pydantic import BaseModel


class riwayat_analisis(BaseModel):  # -> Model Riwayat Analisis di Database
    id_riwayat: int
    id_user: str
    hasil_analisis: str
    rekomendasi_produk: str
    tanggal_analisis: str
