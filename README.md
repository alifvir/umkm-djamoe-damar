# Djamoe Damar, situs statis

Situs profil dan daftar harga jamu botolan Djamoe Damar, Talaga, Cikupa. Statis murni: tanpa database, tanpa server, tanpa login. Semua pesanan tetap lewat WhatsApp.

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
- Nama, catatan rasa, komposisi, dan foto tiap varian: list `VARIAN` di `build.py`.
- Foto baru: taruh JPEG di `assets-src/`, isi `foto` pada varian dengan nama berkasnya, lalu build ulang.
- Varian tanpa foto tetap tampil di halaman menu tanpa gambar.

## Yang perlu dikonfirmasi pemilik

1. Harga. Saat ini semua varian diisi Rp10.000 per botol 250 ml mengikuti contoh di `format product.txt`. Kalau ada varian yang beda harga, angka di `data/site.json` perlu dipecah per varian.
2. Alamat. Situs memakai `Jl. Pattimura K3 No.17, Talaga, Cikupa` dari format. Sertifikat merek dan halal menyebut `Perum Talaga Bestari Blok K-3/17`, jadi pastikan mana yang dipakai untuk pengambilan.
3. Halal. Sertifikat ID36110017000600324 mencantumkan 10 produk. Susut Perut dan Manjakani belum ada di lampiran. Kalau keduanya sudah tercakup di sertifikat terbaru, kirim berkasnya supaya lampiran ikut diperbarui.
4. Foto Empon-Empon, Sirih, dan Manjakani belum ada. Halaman menu menyebut tiga varian ini belum difoto.
5. Testimoni memakai 4 tangkapan layar chat yang diberikan. Nama dan nomor kontak sudah dipotong. Sertifikat yang ditampilkan di `/tentang/#legalitas` memuat alamat pemilik, beri tahu kalau bagian itu perlu disamarkan.

## Deploy

Lihat `DEPLOY.md`. Singkatnya: repo GitHub dulu, lalu Cloudflare Pages dengan Connect to Git, build command `pip install -r requirements.txt && python build.py`, output `dist`.
