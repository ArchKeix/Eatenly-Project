from pydantic import BaseModel


class riwayat_analisis(BaseModel):  # -> Model Riwayat Analisis di Database
    id_riwayat: int
    id_user: str
    nama_produk: str
    status_halal: str
    rekomendasi_produk: str
    preferensi: str
    tanggal_analisis: str
