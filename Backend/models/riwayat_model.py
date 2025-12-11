from pydantic import BaseModel


class riwayat_analisis(BaseModel):  # -> Model Riwayat Analisis di Database
    id_riwayat: int
    id_user: str
    nama_produk: str
    preferensi: str
    rekomendasi_produk: str
    hasil_analisis: str
    tanggal_analisis: str
