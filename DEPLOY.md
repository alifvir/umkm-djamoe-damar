# Deploy Djamoe Damar

## Sebelum deploy

1. Konfirmasi harga dan alamat ke pemilik (lihat README bagian "Yang perlu dikonfirmasi").
2. Pastikan foto dan teks sudah disetujui.
3. Jalankan build bersih:

```bash
pip install -r requirements.txt
python build.py
python tools/audit.py
```

`tools/audit.py` harus berakhir `masalah: 0` dan `dist/` berisi 5 halaman.

## Urutan yang benar: repo dulu, Pages belakangan

Proyek Pages yang dibuat lewat Upload assets tidak bisa dihubungkan ke GitHub setelahnya. Jadi:

1. Buat repo publik `alifvir/umkm-djamoe-damar` (satu klien satu repo).
2. Push seluruh isi proyek, termasuk `assets-src/` dan `data/`. Jangan push `dist/`.
3. Di Cloudflare: Workers & Pages, Create, Pages, Connect to Git, pilih repo tersebut.
4. Setelan build:
   - Framework preset: None
   - Build command: `pip install -r requirements.txt && python build.py`
   - Build output directory: `dist`
   - Root directory: kosong
5. Deploy. Alamat akan menjadi `https://umkm-djamoe-damar.pages.dev` (nama proyek menentukan subdomain, jadi putuskan sebelum klik pertama).

## Setelah live

1. Isi `url` di `data/site.json` dengan alamat live, tanpa garis miring di akhir.
2. Build ulang dan push. Dengan `url` terisi, `sitemap.xml` dan baris `Sitemap:` di `robots.txt` ikut dibuat.
3. Uji alamat produksi:

```bash
for p in / /menu/ /tentang/ /kontak/ /404.html /assets/css/style.css; do
  printf "%s " "$p"; curl -s -o /dev/null -w "%{http_code}\n" "https://umkm-djamoe-damar.pages.dev$p"
done
curl -s -o /dev/null -w "%{http_code}\n" "https://umkm-djamoe-damar.pages.dev/halaman-ngawur"
```

Semua harus 200, kecuali path ngawur yang harus 404 dengan halaman sendiri.

4. Cek satu tombol WhatsApp di HP: harus membuka `api.whatsapp.com/send?phone=6283890790145` dengan pesan pembuka.

## Update harga atau foto

1. Ubah `data/site.json` (harga) atau `assets-src/` + list `VARIAN` di `build.py` (foto dan varian).
2. `python build.py`
3. `git add -A && git commit -m "Update harga" && git push`
4. Cloudflare membangun ulang otomatis. Tunggu sampai `sitemap.xml` di alamat produksi memuat versi baru.

Harga tidak berubah sendiri di halaman yang sudah terbit: harus lewat build dan push.

## Domain sendiri

Kalau nanti memakai domain, tambahkan di Cloudflare Pages, Custom domains. Setelah aktif, ganti `url` di `data/site.json` ke domain itu, build ulang, lalu push. Canonical dan sitemap ikut menyesuaikan.
