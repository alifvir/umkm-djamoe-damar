# Djamoe Damar, situs statis

Situs profil dan daftar harga jamu botolan Djamoe Damar, Talaga Bestari, Sindangjaya (Cikupa). Statis murni: tanpa database, tanpa server, tanpa login. Semua pesanan tetap lewat WhatsApp.

## Isi

| Path | Fungsi |
|---|---|
| `build.py` | generator semua halaman dan pemroses foto |
| `data/site.json` | identitas toko, WhatsApp, alamat, jam buka, pembayaran, harga |
| `assets/css/style.css` | seluruh tampilan, token warna ada di `:root` |
| `assets/js/site.js` | buka dan tutup menu di HP |
| `assets-src/` | foto asli botol, logo, QRIS. Tidak ikut diunggah |
| `dist/` | hasil build, ini yang diunggah ke hosting |
| `tools/audit.py` | pemeriksa tautan, alt, judul, harga, em dash |
| `DESIGN.md` | arah desain dan alasan tiap keputusan |

Halaman: `/`, `/menu/`, `/tentang/`, `/kontak/`, `/404.html`.

## Build

```bash
pip install -r requirements.txt
python build.py
python tools/audit.py
```

Hasil ada di `dist/`. Audit harus melaporkan `masalah: 0`.

## Lihat di komputer

Jalankan dari akar proyek, bukan dari dalam `dist/`:

```bash
python -m http.server 8100 -d dist
```

Buka `http://127.0.0.1:8100`.

## Ubah harga atau varian

- Harga per botol: `harga` di `data/site.json`. Semua halaman membaca angka ini.
- Nama, catatan rasa, komposisi, manfaat, dan foto tiap varian: list `VARIAN` di `build.py`.
- Foto baru: taruh JPEG di `assets-src/`, isi `foto` pada varian dengan nama berkasnya, lalu build ulang.
- Varian tanpa foto tetap tampil di halaman menu tanpa gambar.
- Tiap varian di `/menu/` menampilkan tiga baris berlabel: `Rasa` (dari `catatan`), `Komposisi` (dari `bahan`, dirender "Dibuat dari ..."), dan `Manfaat` (daftar butir dari `manfaat`). Baris komposisi dan manfaat tidak dirender kalau datanya kosong.

## Yang perlu dikonfirmasi pemilik

1. Tidak ada data varian yang masih kosong. Komposisi dan rasa 13 varian sudah terisi dari keterangan pemilik.
2. Komposisi Susu Jahe ditulis "wedang jahe, susu kental manis" sesuai keterangan pemilik. Kalau mau diurai (jahe emprit, gula merah, susu kental manis, dan seterusnya), minta daftar bahannya.
4. Foto pelanggan memegang 6 botol (sumber 11.43.36) belum dipasang karena wajah terlihat. Menunggu izin.
5. Testimoni memakai 4 tangkapan layar chat. Nama dan nomor kontak sudah dipotong. Sertifikat di `/tentang/#legalitas` memuat alamat pemilik, beri tahu kalau perlu disamarkan.

Sudah dikonfirmasi pemilik (10 Nov 2026): harga Rp10.000 per botol 250 ml untuk semua varian, sertifikat halal sudah benar, sebutan area "Talaga Bestari".

Alamat dipisah dua (12 Nov 2026): `alamat_1`/`alamat_2` untuk tampilan ("Jl. Pattimura Talaga Bestari K3/17" + "Sindangjaya, Tangerang, 15560") supaya warga sekitar mudah mengenali, sedangkan `alamat_resmi` ("Jl. Pattimura K3 No.17, Talaga, Cikupa, Tangerang Regency, Banten 15560") dipakai untuk JSON-LD LocalBusiness dan tautan Google Maps. Jangan samakan keduanya.

## Status

Live: https://djamoe-damar.pages.dev
Repo: https://github.com/alifvir/umkm-djamoe-damar
Cloudflare Pages terhubung ke repo, build otomatis setiap push ke `main`.

## Deploy

Lihat `DEPLOY.md`. Singkatnya: repo GitHub dulu, lalu Cloudflare Pages dengan Connect to Git, build command `pip install -r requirements.txt && python build.py`, output `dist`.
