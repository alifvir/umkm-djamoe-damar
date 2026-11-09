# DESIGN.md - Djamoe Damar (situs statis)

Arahan desain untuk `djamoe-damar-web`. Dibaca bersama skill `antislop` sebagai filter.

## Dial

ENERGY 2 / RHYTHM 3 / MOTION 1

- ENERGY 2: hangat dan percaya diri, bukan halaman kampanye. Produk dan labelnya jadi fokus.
- RHYTHM 3: komposisi antarbagian sengaja berbeda (hero belah dua, grid kartu, pita hijau penuh, daftar harga bergaris, kutipan asimetris, langkah bernomor).
- MOTION 1: hanya hover dan transisi 120ms. Tidak ada animasi saat scroll.

Design read: situs profil dan katalog untuk pembeli jamu rumahan di Tangerang, dengan bahasa visual etiket jamu (krem, hijau daun, kuning kunyit, merah damar), dial ENERGY 2 / RHYTHM 3 / MOTION 1.

## Kenapa arah ini

Logo Djamoe Damar sudah punya bahasa sendiri: krem seperti kertas etiket, hijau daun, kuning kunyit dengan garis merah damar. Situs mengikuti warna itu, bukan palet baru, supaya botol dan halaman terlihat satu keluarga. Bentuk label botol (lengkung di atas) dipakai sebagai satu-satunya motif bentuk, muncul di bingkai foto produk. Tidak ada ilustrasi, tidak ada pola batik buatan, tidak ada ornamen tambahan.

## Palet

| Token | Nilai | Alasan |
|---|---|---|
| paper | #FBF1DA | krem etiket, dasar seluruh halaman |
| paper-2 | #F6E8C9 | pemisah bagian tanpa garis |
| card | #FFFCF3 | permukaan kartu dan panel, satu tingkat lebih terang dari kertas |
| ink | #23251C | teks utama, hitam kehijauan seperti tinta kemasan |
| muted | #5E5B4A | teks penjelas, tetap lolos kontras AA |
| green | #1D5B37 | warna daun pada logo, dipakai untuk tombol dan tautan |
| green-deep | #123B26 | pita proses dan footer, membuat satu bagian gelap sebagai jeda |
| amber-ink | #8F4E12 | harga dan penanda nomor bagian, kunyit yang digelapkan agar terbaca |
| damar | #8B3A22 | aksen kecil: tanda kutip dan garis logo |
| line | #E3D4B3 | garis rambut pemisah |

Tiga warna inti (krem, hijau, kuning kunyit) plus satu aksen (merah damar). Merah damar tidak dipakai untuk tombol atau teks panjang.

## Tipografi

- Judul: Gloock (serif display), karena huruf etiket jamu lama memakai serif tebal, dan Gloock punya kontras tinggi yang terasa seperti cetakan label, bukan sans-serif modern.
- Teks: Plus Jakarta Sans, netral dan nyaman dibaca di HP, dipakai konsisten dengan situs lain milik user.
- Skala: judul hero clamp(2.5rem, 5.4vw, 4.2rem), line-height 1.04. Judul bagian clamp(1.7rem, 3vw, 2.35rem). Teks isi 1.02rem, line-height 1.65.

## Motif identitas

1. Lengkung label: bingkai foto produk memakai sudut atas membulat lebar, meniru siluet etiket botol. Hanya dipakai di foto produk.
2. Nomor bagian: label `01 / Varian`, `02 / Proses`, dan seterusnya dengan garis rambut di bawahnya, dipakai di semua halaman.

## Aturan yang dipegang

- Tidak ada statistik, jumlah pelanggan, atau testimoni karangan. Kutipan diambil dari tangkapan layar chat pelanggan yang diberikan pemilik toko, tanpa foto dan tanpa nama lengkap.
- Foto produk adalah foto asli botol Djamoe Damar. Logo memakai berkas logo asli yang diberikan.
- Klaim halal dan merek hanya menyebut yang tercetak di kemasan dan sertifikat: Halal Indonesia, merek terdaftar No. IDM001479970, sejak 2019.
- Harga satu angka: Rp10.000 per botol 250 ml. Tidak ada kata "mulai dari".
- Tidak ada em dash, tidak ada emoji, tidak ada ikon dekoratif.
- Setiap tautan punya tujuan nyata. Tombol order membuka WhatsApp dengan pesan yang menyebut varian.
- Tombol WhatsApp melayang satu-satunya elemen dengan bayangan, karena harus terangkat di atas konten yang bergulir.
