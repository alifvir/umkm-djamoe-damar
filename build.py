"""Build situs statis Djamoe Damar.

Sumber data:
  data/site.json     identitas toko, nomor WA, rekening, alamat, jam buka
  assets-src/*.jpeg  foto botol, logo, QRIS, foto suasana

Hasil: dist/ siap diunggah ke Cloudflare Pages.

Jalankan: python build.py
"""

import json
import os
import shutil
from html import escape
from urllib.parse import quote

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "assets-src")
DIST = os.path.join(ROOT, "dist")
IMG = os.path.join(DIST, "assets", "img")

SITE = json.load(open(os.path.join(ROOT, "data", "site.json"), encoding="utf-8"))

HARGA = SITE["harga"]
ISI = SITE["isi"]

# Varian yang dijual. Urutan tampil mengikuti urutan di daftar harga.
# bahan hanya diisi kalau komposisinya terbaca di label botol.
# manfaat berupa daftar butir; kalau kosong, baris manfaat tidak dirender.
VARIAN = [
    {
        "nama": "Kunyit Asem",
        "slug": "kunyit-asem",
        "catatan": "Asam segar, manisnya pas.",
        "bahan": "Kunyit segar, asam jawa, sereh, gula merah, garam, perasan jeruk nipis.",
        "manfaat": [
            "Menurunkan kolesterol.",
            "Sumber antioksidan.",
            "Mengurangi risiko kanker.",
            "Menjaga kesehatan kulit.",
            "Mengurangi nyeri haid.",
        ],
        "foto": "kunyit-asem.jpeg",
    },
    {
        "nama": "Beras Kencur",
        "slug": "beras-kencur",
        "catatan": "Kencur yang lembut dan sedikit manis.",
        "bahan": "",
        "manfaat": [
            "Membantu menjaga daya tahan tubuh.",
            "Membantu meredakan batuk, pilek, masuk angin, dan badan pegal.",
            "Membantu pencernaan lebih nyaman.",
        ],
        "foto": "beras-kencur.jpeg",
    },
    {
        "nama": "Kunyit Tawar",
        "slug": "kunyit-tawar",
        "catatan": "Tanpa gula, untuk yang tidak suka manis.",
        "bahan": "",
        "manfaat": ["Meredakan mual, kembung, dan keluhan asam lambung."],
        "foto": "kunyit-tawar.jpeg",
    },
    {
        "nama": "Wedang Jahe",
        "slug": "wedang-jahe",
        "catatan": "Hangat, beraroma sereh dan pandan.",
        "bahan": "Jahe emprit, gula merah, sereh, daun pandan, daun jeruk, jeruk nipis.",
        "manfaat": [
            "Memberi sensasi hangat.",
            "Membantu meredakan mual.",
            "Mengandung antioksidan.",
        ],
        "foto": "wedang-jahe.jpeg",
    },
    {
        "nama": "Susu Jahe",
        "slug": "susu-jahe",
        "catatan": "Lebih lembut di tenggorokan.",
        "bahan": "",
        "manfaat": [
            "Menghangatkan tubuh.",
            "Menjaga kesehatan jantung.",
            "Menjaga kesehatan tulang.",
        ],
        "foto": "susu-jahe.jpeg",
    },
    {
        "nama": "Manjakani",
        "slug": "manjakani",
        "catatan": "Racikan khas Mama Damar.",
        "bahan": "",
        "manfaat": [
            "Membantu mengurangi masalah kewanitaan seperti keputihan dan bau tidak sedap.",
            "Membantu mengencangkan area kewanitaan.",
        ],
        "foto": "",
    },
    {
        "nama": "Susut Perut",
        "slug": "susut-perut",
        "catatan": "Racikan rempah khas Mama Damar.",
        "bahan": "",
        "manfaat": [
            "Membantu melancarkan BAB.",
            "Mengurangi lemak perut.",
            "Membantu mengurangi nafsu makan.",
        ],
        "foto": "susut-perut.jpeg",
    },
    {
        "nama": "Temulawak",
        "slug": "temulawak",
        "catatan": "Segar, sedikit pahit di akhir.",
        "bahan": "",
        "manfaat": [
            "Membantu menjaga kesehatan hati.",
            "Menambah nafsu makan.",
        ],
        "foto": "temulawak.jpeg",
    },
    {
        "nama": "Pahitan",
        "slug": "pahitan",
        "catatan": "Pahitnya khas, diminum sedikit demi sedikit.",
        "bahan": "",
        "manfaat": [
            "Membantu mengontrol gula darah dan kolesterol.",
            "Membantu menjaga stamina.",
        ],
        "foto": "pahitan.jpeg",
    },
    {
        "nama": "Empon-Empon",
        "slug": "empon-empon",
        "catatan": "Campuran rempah, hangat dan beraroma lengkap.",
        "bahan": "",
        "manfaat": [
            "Membantu gangguan lambung.",
            "Membantu menjaga daya tahan tubuh.",
            "Menghangatkan tubuh.",
        ],
        "foto": "",
    },
    {
        "nama": "Sirih",
        "slug": "sirih",
        "catatan": "Tanpa manis, tinggal wangi aroma daun sirih.",
        "bahan": "",
        "manfaat": [
            "Antibakteri.",
            "Mengurangi bau badan.",
            "Mendukung kesehatan organ kewanitaan.",
        ],
        "foto": "",
    },
    {
        "nama": "Gulas",
        "slug": "gulas",
        "catatan": "Asam manis, diminum dingin lebih segar.",
        "bahan": "",
        "manfaat": [
            "Menyegarkan tubuh.",
            "Melancarkan pencernaan.",
            "Membantu meredakan panas dalam.",
        ],
        "foto": "",
    },
    {
        "nama": "Semerai",
        "slug": "semerai",
        "catatan": "Asam, manis, aroma sereh yang khas. Cocok diminum dingin.",
        "bahan": "",
        "manfaat": [
            "Melancarkan pencernaan.",
            "Menyegarkan tubuh.",
            "Membantu melawan radikal bebas.",
        ],
        "foto": "",
    },
]

JUMLAH_VARIAN = len(VARIAN)
TANPA_FOTO = [v["nama"] for v in VARIAN if not v["foto"]]
JUMLAH_TANPA_FOTO = len(TANPA_FOTO)


def daftar_nama(nama):
    if len(nama) <= 1:
        return nama[0] if nama else ""
    return ", ".join(nama[:-1]) + ", dan " + nama[-1]

TESTIMONI_FOTO = [
    {
        "berkas": "testimoni-1.jpeg",
        "potong": (0, 0, 997, 612),
        "kutipan": "Jamunya cocok di aku.",
        "catatan": "Kunyit Asem dan Susut Perut, tidak terlalu manis",
        "alt": "Tangkapan layar chat pelanggan yang menyebut kunyit asem tidak terlalu manis dan susut perut segar",
    },
    {
        "berkas": "testimoni-2.jpeg",
        "potong": (0, 200, 1080, 784),
        "kutipan": "Sudah tahu kualitas rasa jamunya Mama Damar paling best.",
        "catatan": "Beras kencur jahe saat batuk",
        "alt": "Tangkapan layar chat pelanggan yang memuji kualitas rasa jamu Mama Damar",
    },
    {
        "berkas": "testimoni-3.jpeg",
        "potong": (0, 990, 1080, 1380),
        "kutipan": "Tapi jamu ini aku suka.",
        "catatan": "Minta dikabari saat buka lagi",
        "alt": "Tangkapan layar chat pelanggan yang menyukai jamu dan minta dikabari saat buka lagi",
    },
    {
        "berkas": "testimoni-4.jpeg",
        "potong": (0, 415, 720, 1075),
        "kutipan": "Aku juga abis Manjakani, enak bgt.",
        "catatan": "Manjakani, katanya enak banget",
        "alt": "Tangkapan layar chat pelanggan yang menyebut jamu Manjakani enak",
    },
]

KETENTUAN = [
    ("Pesanan dibuat setelah pembayaran", "Jamu diracik setelah pesanan dan pembayaran dikonfirmasi."),
    ("Botol selalu tersegel", "Kalau segel rusak saat diterima, jangan diminum. Kabari kami lewat WhatsApp."),
    ("Pengiriman lewat ojek online", "Biaya kirim mengikuti jarak. Bisa juga ambil sendiri di kios."),
    ("Varian bisa disesuaikan", "Sebutkan varian dan jumlahnya di WhatsApp, kami balas total dan waktu siapnya."),
]


def rupiah(n):
    return "Rp " + format(n, ",d").replace(",", ".")


def tulis(path, isi):
    tujuan = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(tujuan) or DIST, exist_ok=True)
    with open(tujuan, "w", encoding="utf-8", newline="\n") as f:
        f.write(isi)


# ---------------------------------------------------------------- gambar
def potong_logo():
    """Logo asli dipotong dari latar krem, lalu latarnya dibuat transparan."""
    im = Image.open(os.path.join(SRC, "logo.jpeg")).convert("RGB")
    kotak = (500, 240, 1100, 740)
    im = im.crop(kotak).convert("RGBA")
    px = im.load()
    W, H = im.size
    krem = (255, 240, 207)
    for y in range(H):
        for x in range(W):
            r, g, b, _a = px[x, y]
            jarak = max(abs(r - krem[0]), abs(g - krem[1]), abs(b - krem[2]))
            if jarak <= 14:
                px[x, y] = (255, 255, 255, 0)
            elif jarak < 46:
                alfa = round((jarak - 14) / 32 * 255)
                px[x, y] = (r, g, b, alfa)
            else:
                px[x, y] = (r, g, b, 255)
    im.thumbnail((360, 300), Image.LANCZOS)
    im.save(os.path.join(IMG, "logo.webp"), "WEBP", quality=90, method=6)

    icon = Image.new("RGBA", (128, 128), (251, 241, 218, 255))
    kecil = im.copy()
    kecil.thumbnail((110, 110), Image.LANCZOS)
    icon.alpha_composite(kecil, ((128 - kecil.width) // 2, (128 - kecil.height) // 2))
    icon.convert("RGB").save(os.path.join(DIST, "assets", "favicon.png"), "PNG")

    return im


def siapkan_gambar():
    if os.path.isdir(IMG):
        shutil.rmtree(IMG)
    os.makedirs(IMG, exist_ok=True)

    # foto botol, rasio asli 3:4 dipakai apa adanya
    foto = {}
    for v in VARIAN:
        if not v["foto"]:
            continue
        im = Image.open(os.path.join(SRC, v["foto"])).convert("RGB")
        im = im.resize((720, round(im.height * 720 / im.width)), Image.LANCZOS)
        berkas = v["slug"] + ".webp"
        im.save(os.path.join(IMG, berkas), "WEBP", quality=84, method=6)
        foto[v["slug"]] = {"berkas": "assets/img/" + berkas, "w": im.width, "h": im.height}

    # hero: botol kunyit asem di pinggir jalan, rasio 3:4
    hero = Image.open(os.path.join(SRC, "hero.jpeg")).convert("RGB")
    hero = hero.resize((860, round(hero.height * 860 / hero.width)), Image.LANCZOS)
    hero.save(os.path.join(IMG, "hero.webp"), "WEBP", quality=85, method=6)

    # foto tentang: botol beras kencur di halaman, hijau dan sesuai palet
    tentang = Image.open(os.path.join(SRC, "beras-kencur.jpeg")).convert("RGB")
    tentang = tentang.resize((720, round(tentang.height * 720 / tentang.width)), Image.LANCZOS)
    tentang.save(os.path.join(IMG, "tentang.webp"), "WEBP", quality=84, method=6)

    # QRIS
    qris = Image.open(os.path.join(SRC, "qris.jpeg")).convert("RGB")
    qris.thumbnail((760, 760), Image.LANCZOS)
    qris.save(os.path.join(IMG, "qris.webp"), "WEBP", quality=86, method=6)

    potong_logo()
    return foto


def siapkan_sertifikat():
    """Sertifikat ditampilkan sebagai dokumen. Halal berasal dari PDF pindaian."""
    hasil = {}

    merek = Image.open(os.path.join(SRC, "sertifikat-merek.jpeg")).convert("RGB")
    merek.save(os.path.join(IMG, "sertifikat-merek.webp"), "WEBP", quality=86, method=6)
    hasil["merek"] = {"berkas": "assets/img/sertifikat-merek.webp", "w": merek.width, "h": merek.height}

    for nomor in (1, 2):
        im = Image.open(os.path.join(SRC, "sertifikat-halal-%d.png" % nomor)).convert("RGB")
        # buang bilah "Dipindai dengan CamScanner" di dasar halaman
        im = im.crop((0, 0, im.width, round(im.height * 0.953)))
        im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        berkas = "sertifikat-halal%s.webp" % ("" if nomor == 1 else "-lampiran")
        im.save(os.path.join(IMG, berkas), "WEBP", quality=85, method=6)
        hasil["halal" if nomor == 1 else "lampiran"] = {
            "berkas": "assets/img/" + berkas, "w": im.width, "h": im.height,
        }
    return hasil


def siapkan_testimoni():
    """Potong tangkapan layar chat ke bagian percakapan saja."""
    hasil = []
    for nomor, t in enumerate(TESTIMONI_FOTO, 1):
        im = Image.open(os.path.join(SRC, t["berkas"])).convert("RGB")
        im = im.crop(t["potong"])
        if im.width > 900:
            im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
        berkas = "testimoni-%d.webp" % nomor
        im.save(os.path.join(IMG, berkas), "WEBP", quality=86, method=6)
        hasil.append({
            "berkas": "assets/img/" + berkas,
            "kutipan": t["kutipan"],
            "catatan": t["catatan"],
            "alt": t["alt"],
            "w": im.width,
            "h": im.height,
        })
    return hasil


def wa_tautan(pesan=None):
    nomor = (SITE.get("wa") or "").strip().replace("+", "").replace(" ", "").replace("-", "")
    if not nomor:
        return None
    if nomor.startswith("0"):
        nomor = "62" + nomor[1:]
    return "https://wa.me/%s?text=%s" % (nomor, quote(pesan or SITE.get("wa_pesan", "")))


def nomor_tampil():
    nomor = (SITE.get("wa") or "").strip().replace("+", "").replace(" ", "").replace("-", "")
    if not nomor:
        return ""
    lokal = "0" + nomor[2:] if nomor.startswith("62") else nomor
    if len(lokal) >= 11:
        return "%s-%s-%s" % (lokal[:4], lokal[4:8], lokal[8:])
    return lokal


def alamat_html():
    baris = [SITE.get("alamat_1"), SITE.get("alamat_2")]
    baris = [escape(b) for b in baris if b]
    if baris:
        return "<br>".join(baris)
    return escape(SITE.get("alamat", ""))


def tombol_order(kelas="tombol", teks="Pesan lewat WhatsApp", pesan=None):
    tautan = wa_tautan(pesan)
    if not tautan:
        return '<a class="%s" href="/kontak/">Cara pesan</a>' % kelas
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (
        kelas, escape(tautan), teks)


IKON_WA = ('<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" focusable="false">'
           '<path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2Zm5.8 14.13c-.24.68-1.4 1.3-1.93 1.35-.53.05-1.02.24-3.44-.72-2.93-1.15-4.75-4.2-4.9-4.4-.14-.2-1.16-1.55-1.16-2.96 0-1.4.73-2.09 1-2.38.26-.29.58-.36.77-.36l.56.01c.18 0 .42-.07.65.5.24.58.82 2 .89 2.14.07.14.12.31.02.5-.1.2-.15.32-.29.49-.15.17-.31.38-.44.51-.15.14-.3.3-.13.59.17.29.75 1.24 1.62 2.01 1.11.99 2.05 1.3 2.34 1.44.29.15.46.12.63-.07.17-.2.73-.85.93-1.14.19-.29.39-.24.65-.14.26.09 1.66.78 1.94.93.29.14.48.22.55.34.07.13.07.73-.17 1.41Z"/></svg>')


def tombol_wa_melayang():
    tautan = wa_tautan()
    if not tautan:
        return ""
    return ('<a class="wa-melayang" href="%s" target="_blank" rel="noopener" '
            'aria-label="Chat WhatsApp Djamoe Damar">%s</a>' % (escape(tautan), IKON_WA))


def nav_aktif(aktif, kunci, href, teks):
    tanda = ' aria-current="page"' if aktif == kunci else ""
    return '<li><a href="%s"%s>%s</a></li>' % (href, tanda, teks)


def kepala(judul, deskripsi, aktif, kanonikal=""):
    kanon = og_url = ""
    if SITE.get("url") and kanonikal:
        kanon = '<link rel="canonical" href="%s%s">' % (SITE["url"], kanonikal)
        og_url = '<meta property="og:url" content="%s%s">' % (SITE["url"], kanonikal)
    skema = ""
    if aktif == "beranda":
        skema = ('<script type="application/ld+json">'
                 + json.dumps({
                     "@context": "https://schema.org",
                     "@type": "LocalBusiness",
                     "name": SITE["brand"],
                     "description": SITE["deskripsi"],
                     "telephone": "+" + SITE["wa"],
                     "address": {
                         "@type": "PostalAddress",
                         "streetAddress": SITE["alamat"],
                         "addressLocality": "Cikupa",
                         "addressRegion": "Banten",
                         "postalCode": "15560",
                         "addressCountry": "ID",
                     },
                     "openingHours": "Mo-Su 06:00-20:00",
                     "priceRange": rupiah(HARGA),
                     "sameAs": [SITE["instagram"], SITE["maps"]],
                 }, ensure_ascii=False)
                 + "</script>")
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#FBF1DA">
<title>{escape(judul)}</title>
<meta name="description" content="{escape(deskripsi)}">
{kanon}
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(judul)}">
<meta property="og:description" content="{escape(deskripsi)}">
<meta property="og:image" content="/assets/img/hero.webp">
{og_url}
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gloock&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{skema}
</head>
<body>
<a class="skip" href="#utama">Lewati ke isi utama</a>
<header class="site-head">
  <div class="wrap site-head__row">
    <a class="merek" href="/">
      <img src="/assets/img/logo.webp" alt="Logo Djamoe Damar" width="72" height="60" decoding="async">
      <span class="merek__teks"><strong>Djamoe Damar</strong><small>Jamu botolan, Talaga Bestari</small></span>
    </a>
    <button class="nav-tombol" type="button" data-nav-tombol aria-expanded="false" aria-controls="nav-utama">
      <span class="nav-tombol__garis" aria-hidden="true"></span> Menu
    </button>
    <nav class="nav" id="nav-utama" data-nav data-terbuka="false" aria-label="Navigasi utama">
      <ul>
        {nav_aktif(aktif, "varian", "/menu/", "Varian dan harga")}
        {nav_aktif(aktif, "cara", "/#cara-order", "Cara pesan")}
        {nav_aktif(aktif, "tentang", "/tentang/", "Tentang")}
        {nav_aktif(aktif, "kontak", "/kontak/", "Kontak")}
      </ul>
    </nav>
    <div class="head-cta">{tombol_order("tombol tombol--kecil", "Pesan jamu")}</div>
  </div>
</header>
<main id="utama">
"""


def kaki():
    tautan_wa = wa_tautan()
    wa_kaki = ('<li><a href="%s" target="_blank" rel="noopener">WhatsApp %s</a></li>'
               % (escape(tautan_wa), nomor_tampil())) if tautan_wa else ""
    bayar = ", ".join(b["nama"] for b in SITE["bayar"])
    return f"""</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="site-foot__atas">
      <div class="site-foot__merek">
        <img src="/assets/img/logo.webp" alt="Logo Djamoe Damar" width="84" height="70" loading="lazy" decoding="async">
        <p>Jamu botolan 250 ml, diracik {escape(SITE["pemilik"])} di {escape(SITE["alamat_pendek"])}. Sejak {SITE["sejak"]}.</p>
      </div>
      <div>
        <h2>Halaman</h2>
        <ul>
          <li><a href="/menu/">Varian dan harga</a></li>
          <li><a href="/#cara-order">Cara pesan</a></li>
          <li><a href="/tentang/">Tentang</a></li>
          <li><a href="/tentang/#legalitas">Legalitas</a></li>
          <li><a href="/kontak/">Kontak dan pembayaran</a></li>
        </ul>
      </div>
      <div>
        <h2>Ambil di</h2>
        <p>{alamat_html()}</p>
        <ul>
          <li><a href="{escape(SITE["maps"])}">Buka Google Maps</a></li>
          <li><a href="{escape(SITE["instagram"])}">Instagram {escape(SITE["handle"])}</a></li>
          {wa_kaki}
        </ul>
      </div>
    </div>
    <div class="site-foot__bawah">
      <span>&copy; 2026 {escape(SITE["brand"])}. Harga {rupiah(HARGA)} per botol {ISI}.</span>
      <span>Bayar dengan {bayar}, atau QRIS.</span>
    </div>
  </div>
</footer>
{tombol_wa_melayang()}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def kartu_varian(v, foto):
    f = foto[v["slug"]]
    return f"""<article class="kartu">
  <a class="kartu__tautan" href="/menu/#{v['slug']}">
    <span class="kartu__bingkai">
      <img src="/{f['berkas']}" alt="Botol {escape(v['nama'])} 250 ml Djamoe Damar" width="{f['w']}" height="{f['h']}" loading="lazy" decoding="async">
    </span>
    <span class="kartu__isi">
      <strong class="kartu__nama">{escape(v['nama'])}</strong>
      <span class="kartu__catatan">{escape(v['catatan'])}</span>
      <span class="kartu__harga">{rupiah(HARGA)} <small>{ISI}</small></span>
    </span>
  </a>
</article>"""


def baris_harga(v):
    pesan = ("Halo Djamoe Damar, saya mau pesan %s %s. Boleh info waktu siapnya?"
             % (v["nama"], ISI))
    return f"""<div class="baris" id="{v['slug']}">
  <span class="baris__nama">{escape(v['nama'])}</span>
  <span class="baris__catatan">{escape(v['catatan'])}</span>
  <span class="baris__harga">{rupiah(HARGA)}</span>
  <span class="baris__aksi"><a href="{escape(wa_tautan(pesan))}" target="_blank" rel="noopener" aria-label="Pesan {escape(v['nama'])} lewat WhatsApp">Pesan</a></span>
</div>"""


def blok_ketentuan():
    return "".join(
        f"<li><b>{escape(j)}</b><span>{escape(t)}</span></li>" for j, t in KETENTUAN
    )


# ---------------------------------------------------------------- halaman
def halaman_beranda(foto, testimoni):
    kartu = "".join(kartu_varian(v, foto) for v in VARIAN if v["foto"])
    daftar = "".join(baris_harga(v) for v in VARIAN)
    chat = "".join(
        f"""<figure class="chat-kartu">
  <a class="chat-kartu__tautan" href="/{t['berkas']}" target="_blank" rel="noopener">
    <img src="/{t['berkas']}" alt="{escape(t['alt'])}" width="{t['w']}" height="{t['h']}" loading="lazy" decoding="async">
  </a>
  <figcaption>
    <strong>&ldquo;{escape(t['kutipan'])}&rdquo;</strong>
    <span>{escape(t['catatan'])}</span>
  </figcaption>
</figure>""" for t in testimoni
    )
    return kepala(
        "Djamoe Damar, jamu botolan segar dari Talaga Bestari",
        f"{JUMLAH_VARIAN} varian jamu botolan 250 ml, Rp10.000 per botol. Dibuat segar setelah pesanan masuk, diracik Mama Damar di Talaga Bestari. Ambil di kios atau kirim lewat ojek online.",
        "beranda",
        "/",
    ) + f"""
<section class="hero">
  <div class="wrap hero__isi">
    <div class="hero__teks">
      <h1>Jamu segar dari Talaga Bestari, <span>botol 250 ml.</span></h1>
      <p>{JUMLAH_VARIAN} varian, {rupiah(HARGA)} per botol. Dibuat segar setelah pesanan masuk, diracik {escape(SITE["pemilik"])}, lalu disegel. Ambil di kios Talaga Bestari atau kirim lewat ojek online.</p>
      <div class="hero__aksi">
        {tombol_order("tombol", "Pesan lewat WhatsApp")}
        <a class="tombol tombol--outline" href="/menu/">Lihat {JUMLAH_VARIAN} varian</a>
      </div>
      <p class="hero__kecil">Pesanan dibuat setelah pembayaran dikonfirmasi. Balasan mengikuti jam buka. {escape(SITE["jam"])}.</p>
    </div>
    <figure class="hero__foto">
      <img src="/assets/img/hero.webp" alt="Botol jamu kunyit asem Djamoe Damar 250 ml dipegang di pinggir jalan" width="860" height="1147" fetchpriority="high" decoding="async">
      <figcaption class="hero__kartu">
        <strong>Kunyit Asem</strong>
        <span>{rupiah(HARGA)} per botol {ISI}</span>
      </figcaption>
    </figure>
  </div>
</section>

<div class="wrap">
  <ul class="fakta">
    <li><strong>Halal Indonesia</strong><span>Sertifikat No. {escape(SITE["halal_nomor"])}, terbit {escape(SITE["halal_terbit"])}.</span></li>
    <li><strong>Merek terdaftar</strong><span>No. {escape(SITE["merek"])}, terdaftar di DJKI sejak Desember 2025.</span></li>
    <li><strong>Sejak {SITE["sejak"]}</strong><span>Melayani pesanan jamu botolan di Talaga Bestari.</span></li>
  </ul>
</div>

<section>
  <div class="wrap">
    <div class="kepala-bagian">
      <div>
        <p class="label" data-nomor="01">Varian</p>
        <h2>Satu harga untuk semua varian.</h2>
      </div>
      <p class="kepala-bagian__teks">Semua botol isi {ISI} dan dijual {rupiah(HARGA)}. Foto di bawah adalah botol yang benar-benar kami isi, bukan gambar contoh kemasan.</p>
    </div>
    <div class="varian-grid">{kartu}</div>
    <p class="setelah-grid">Varian lain, {daftar_nama(TANPA_FOTO)}, ada di <a class="tautan" href="/menu/">daftar lengkap</a>.</p>
  </div>
</section>

<section class="pita">
  <div class="wrap pita__isi">
    <div>
      <p class="label label--terang" data-nomor="02">Proses</p>
      <h2>Dibuat segar setiap hari, setelah pesanan masuk.</h2>
      <p class="pita__teks">Jamu diracik {escape(SITE["pemilik"])} di Talaga Bestari. Tidak ada stok lama: pesanan baru dibuat setelah masuk dan dikonfirmasi, lalu dimasak, dibotolkan, dan disegel.</p>
      <dl class="pita__daftar">
        <div><dt>Dibuat sesuai pesanan</dt><dd>Jamu baru diracik setelah pesanan dan pembayaran dikonfirmasi.</dd></div>
        <div><dt>Botol tersegel</dt><dd>Setiap botol ditutup rapat. Kalau segel rusak saat diterima, jangan diminum.</dd></div>
        <div><dt>Ambil atau diantar</dt><dd>Ambil di kios, atau kirim lewat ojek online dengan biaya sesuai jarak.</dd></div>
      </dl>
    </div>
    <figure class="pita__foto">
      <div class="pita__tiga">
        <img src="/assets/img/kunyit-asem.webp" alt="Botol kunyit asem Djamoe Damar" width="720" height="960" loading="lazy" decoding="async">
        <img src="/assets/img/beras-kencur.webp" alt="Botol beras kencur Djamoe Damar" width="720" height="960" loading="lazy" decoding="async">
        <img src="/assets/img/pahitan.webp" alt="Botol pahitan Djamoe Damar" width="720" height="960" loading="lazy" decoding="async">
      </div>
      <figcaption>Kunyit Asem, Beras Kencur, dan Pahitan. Tiga dari {JUMLAH_VARIAN} varian.</figcaption>
    </figure>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="kepala-bagian">
      <div>
        <p class="label" data-nomor="03">Harga</p>
        <h2>Daftar lengkap, tanpa biaya tambahan.</h2>
      </div>
      <p class="kepala-bagian__teks">Harga yang tertulis adalah harga per botol. Kirim pesan WhatsApp berisi varian dan jumlah, kami balas total dan perkiraan waktu siapnya.</p>
    </div>
    <div class="tabel" role="table" aria-label="Daftar varian dan harga Djamoe Damar">
      <div class="tabel__kepala" role="row">
        <span role="columnheader">Varian</span>
        <span role="columnheader">Catatan rasa</span>
        <span role="columnheader">Harga</span>
        <span role="columnheader"><span class="sr-only">Pesan</span></span>
      </div>
      {daftar}
    </div>
  </div>
</section>

<section class="bagian-kutipan">
  <div class="wrap">
    <div class="kepala-bagian">
      <div>
        <p class="label" data-nomor="04">Kata pelanggan</p>
        <h2>Enak, cocok, dan dicari lagi.</h2>
      </div>
      <p class="kepala-bagian__teks">Empat tangkapan layar dari WhatsApp Djamoe Damar, toko jamu yang melayani pesanan sejak 2019. Teks tidak diubah, hanya bagian percakapannya yang dipotong.</p>
    </div>
    <div class="chat-grid">{chat}</div>
    <p class="sumber">Ketuk gambar untuk membuka ukuran penuh. Nama dan nomor kontak tidak ditampilkan. Pengalaman tiap orang bisa berbeda.</p>
  </div>
</section>

<section class="alur" id="cara-order">
  <div class="wrap alur__isi">
    <div class="alur__kiri">
      <p class="label" data-nomor="05">Cara pesan</p>
      <h2>Tiga langkah, lewat WhatsApp.</h2>
      <p>Tidak perlu aplikasi baru atau akun. Semua pesanan dicatat dari chat, lalu dibuat setelah pembayaran dikonfirmasi.</p>
      <p class="alur__catatan">Bayar dengan {", ".join(b["nama"] for b in SITE["bayar"])}, atau QRIS. Kirim bukti transfer lewat chat.</p>
    </div>
    <ol class="langkah">
      <li>
        <div>
          <h3>Tanya varian</h3>
          <p>Chat WhatsApp, sebutkan varian dan jumlah botol. Kami balas total dan perkiraan waktu siapnya.</p>
        </div>
      </li>
      <li>
        <div>
          <h3>Konfirmasi dan bayar</h3>
          <p>Transfer DANA atau GoPay, atau pindai QRIS. Pesanan mulai dibuat setelah pembayaran dikonfirmasi.</p>
        </div>
      </li>
      <li>
        <div>
          <h3>Ambil atau kirim</h3>
          <p>Ambil di kios {escape(SITE["alamat_pendek"])}, atau minta dikirim lewat ojek online. Biaya kirim sesuai jarak.</p>
        </div>
      </li>
    </ol>
  </div>
</section>

<section class="lokasi">
  <div class="wrap lokasi__isi">
    <div>
      <p class="label" data-nomor="06">Lokasi dan jam buka</p>
      <h2>Kios di Talaga Bestari, buka setiap hari.</h2>
      <address>{alamat_html()}</address>
      <p class="lokasi__jam">{escape(SITE["jam"])}.</p>
      <div class="hero__aksi">
        <a class="tombol tombol--outline" href="{escape(SITE["maps"])}">Buka Google Maps</a>
        {tombol_order("tautan", "Tanya varian lewat WhatsApp")}
      </div>
    </div>
    <div class="lokasi__panel">
      <h3>Sebelum pesan</h3>
      <p>Kabari varian yang dicari lewat WhatsApp. Karena dibuat sesuai pesanan, waktu siap kami informasikan lewat chat.</p>
      <p class="teks-kecil">Alamat lengkap dan info pembayaran ada di <a class="tautan" href="/kontak/">halaman kontak</a>.</p>
    </div>
  </div>
</section>
""" + kaki()


def halaman_menu(foto):
    baris = []
    for v in VARIAN:
        f = foto.get(v["slug"])
        thumb = ""
        kelas = "varian"
        if f:
            thumb = ('<img class="baris__foto" src="/%s" alt="Botol %s Djamoe Damar" width="%d" height="%d" loading="lazy" decoding="async">'
                     % (f["berkas"], escape(v["nama"]), f["w"], f["h"]))
        else:
            kelas = "varian varian--teks"
        if v["bahan"]:
            isi_bahan = v["bahan"][0].lower() + v["bahan"][1:]
            bahan = ('<p class="varian__komposisi"><b class="varian__label">Komposisi</b> Dibuat dari %s</p>'
                     % escape(isi_bahan))
        else:
            bahan = ""
        if v.get("manfaat"):
            butir = "".join("<li>%s</li>" % escape(m) for m in v["manfaat"])
            manfaat = ('<div class="varian__manfaat"><b class="varian__label">Manfaat</b><ul>%s</ul></div>'
                       % butir)
        else:
            manfaat = ""
        pesan = "Halo Djamoe Damar, saya mau pesan %s %s. Boleh info waktu siapnya?" % (v["nama"], ISI)
        baris.append(f"""<article class="{kelas}" id="{v['slug']}">
  {thumb}
  <div class="varian__isi">
    <h3>{escape(v['nama'])}</h3>
    <p class="varian__rasa"><b class="varian__label">Rasa</b> {escape(v['catatan'])}</p>
    {bahan}
    {manfaat}
  </div>
  <div class="varian__beli">
    <strong>{rupiah(HARGA)}</strong>
    <span>{ISI}</span>
    <a class="tombol tombol--kecil tombol--outline" href="{escape(wa_tautan(pesan))}" target="_blank" rel="noopener">Pesan {escape(v['nama'])}</a>
  </div>
</article>""")
    return kepala(
        "Varian dan harga jamu, Djamoe Damar",
        f"Daftar {JUMLAH_VARIAN} varian jamu Djamoe Damar, Rp10.000 per botol 250 ml. Kunyit asem, beras kencur, wedang jahe, temulawak, dan lainnya.",
        "varian",
        "/menu/",
    ) + f"""
<div class="page-head">
  <div class="wrap">
    <p class="label" data-nomor="01">Varian dan harga</p>
    <h1>{JUMLAH_VARIAN} varian, {rupiah(HARGA)} per botol.</h1>
    <p>Semua botol isi {ISI}. Pesanan dibuat setelah pembayaran dikonfirmasi, waktu siap diinformasikan lewat WhatsApp. {JUMLAH_TANPA_FOTO} varian belum ada fotonya, tapi tetap tersedia.</p>
  </div>
</div>
<section class="bagian-varian">
  <div class="wrap">
    <h2 class="sr-only">Daftar varian dan harga</h2>
    <div class="daftar-varian">{''.join(baris)}</div>
    <p class="sumber">Komposisi yang tertulis di halaman ini diambil dari label botol. Untuk varian lain, tanyakan komposisinya lewat WhatsApp.</p>
  </div>
</section>
<section class="alur alur--ringkas" id="cara-order">
  <div class="wrap alur__isi">
    <div class="alur__kiri">
      <p class="label" data-nomor="02">Cara pesan</p>
      <h2>Pilih, bayar, lalu tunggu pesanan dibuat.</h2>
      <p>Pesanan dibuat setelah pembayaran dikonfirmasi. Bisa bayar dengan {", ".join(b["nama"] for b in SITE["bayar"])} atau QRIS.</p>
      <p class="alur__catatan">Waktu siap tergantung jumlah pesanan. Kami kabari lewat WhatsApp.</p>
    </div>
    <ol class="langkah">
      <li><div><h3>Pilih varian</h3><p>Sebutkan varian dan jumlah botol lewat WhatsApp. Kami balas total dan waktu siapnya.</p></div></li>
      <li><div><h3>Bayar</h3><p>Transfer atau QRIS, lalu kirim bukti. Pesanan mulai dibuat setelah pembayaran masuk.</p></div></li>
      <li><div><h3>Ambil atau kirim</h3><p>Ambil di kios Talaga Bestari, atau kirim lewat ojek online.</p></div></li>
    </ol>
  </div>
</section>
""" + kaki()


def halaman_tentang(sertifikat):
    halal = sertifikat["halal"]
    lampiran = sertifikat["lampiran"]
    merek = sertifikat["merek"]
    return kepala(
        "Tentang Djamoe Damar",
        "Djamoe Damar adalah usaha jamu botolan Mama Damar di Talaga Bestari. Sejak 2019, bersertifikat halal, dan merek terdaftar.",
        "tentang",
        "/tentang/",
    ) + f"""
<div class="page-head">
  <div class="wrap">
    <p class="label" data-nomor="01">Tentang</p>
    <h1>Jamu rumahan dari Talaga Bestari, sejak {SITE["sejak"]}.</h1>
    <p>Djamoe Damar adalah usaha jamu botolan {escape(SITE["pemilik"])} di {escape(SITE["alamat_pendek"])}. Jamu diracik dari bahan segar, dikemas dalam botol {ISI}, lalu dijual langsung ke pelanggan di sekitar Tangerang.</p>
  </div>
</div>
<section class="tentang">
  <div class="wrap tentang__isi">
    <div class="tentang__teks">
      <p class="label" data-nomor="02">Cara kerja</p>
      <h2>Dibuat segar, praktis dalam botol, pesanan harian.</h2>
      <p>Jamu diracik setelah pesanan masuk. Setelah dimasak, jamu dibotolkan dan disegel, lalu disiapkan untuk diambil atau dikirim. Pelanggan bisa mengambil di kios atau meminta dikirim lewat ojek online.</p>
      <p>Karena dibuat sesuai pesanan, waktu siap bisa berbeda tergantung jumlah pesanan. Konfirmasi lewat WhatsApp sebelum datang ke kios.</p>
      <ul class="tentang__fakta">
        <li><strong>Halal Indonesia</strong><span>Sertifikat No. {escape(SITE["halal_nomor"])}, terbit {escape(SITE["halal_terbit"])}.</span></li>
        <li><strong>Merek terdaftar</strong><span>No. {escape(SITE["merek"])}, berlaku 10 tahun sejak {escape(SITE["merek_terbit"])}.</span></li>
        <li><strong>Sejak {SITE["sejak"]}</strong><span>Melayani pesanan jamu botolan di {escape(SITE["alamat_pendek"])}.</span></li>
      </ul>
    </div>
    <figure class="tentang__foto">
      <img src="/assets/img/tentang.webp" alt="Botol beras kencur Djamoe Damar dipegang di halaman berdaun hijau" width="720" height="960" loading="lazy" decoding="async">
    </figure>
  </div>
</section>
<section class="legal" id="legalitas">
  <div class="wrap">
    <div class="kepala-bagian">
      <div>
        <p class="label" data-nomor="03">Legalitas</p>
        <h2>Halal dan merek, ada dokumennya.</h2>
      </div>
      <p class="kepala-bagian__teks">Sertifikat ditampilkan apa adanya. Ketuk gambar untuk membuka ukuran penuh.</p>
    </div>
    <div class="legal-grid">
      <figure class="legal-kartu">
        <a class="legal-kartu__tautan" href="/{halal['berkas']}" target="_blank" rel="noopener">
          <img src="/{halal['berkas']}" alt="Sertifikat halal Djamoe Damar nomor {escape(SITE['halal_nomor'])}" width="{halal['w']}" height="{halal['h']}" loading="lazy" decoding="async">
        </a>
        <figcaption>
          <strong>Sertifikat halal</strong>
          <span>No. {escape(SITE["halal_nomor"])}, terbit {escape(SITE["halal_terbit"])}. Sepuluh produk tercantum di lampiran.</span>
          <a class="tautan" href="/{lampiran['berkas']}" target="_blank" rel="noopener">Lihat lampiran daftar produk</a>
        </figcaption>
      </figure>
      <figure class="legal-kartu">
        <a class="legal-kartu__tautan" href="/{merek['berkas']}" target="_blank" rel="noopener">
          <img src="/{merek['berkas']}" alt="Sertifikat merek Djamoe Damar nomor {escape(SITE['merek'])}" width="{merek['w']}" height="{merek['h']}" loading="lazy" decoding="async">
        </a>
        <figcaption>
          <strong>Sertifikat merek</strong>
          <span>No. {escape(SITE["merek"])}, diterima {escape(SITE["merek_terbit"])}. Berlaku 10 tahun sampai 12 Desember 2035.</span>
        </figcaption>
      </figure>
    </div>
  </div>
</section>
<section class="pita pita--ringkas">
  <div class="wrap pita__isi">
    <div>
      <p class="label label--terang" data-nomor="04">Ketentuan</p>
      <h2>Yang perlu diketahui sebelum pesan.</h2>
      <ul class="daftar-ketentuan">{blok_ketentuan()}</ul>
    </div>
    <div class="pita__aksi">
      <p>Mau tanya varian atau waktu siapnya?</p>
      {tombol_order("tombol tombol--terang", "Chat WhatsApp")}
      <p class="teks-kecil">Jam buka {escape(SITE["jam"]).lower()}.</p>
    </div>
  </div>
</section>
""" + kaki()


def halaman_kontak():
    tautan = wa_tautan()
    kartu_wa = f"""
    <div class="kartu-info kartu-info--wa">
      <h2>WhatsApp</h2>
      <p class="kontak-nomor">{escape(nomor_tampil())}</p>
      <p>Tanya varian, pesan, atau kirim bukti transfer. Sebutkan varian dan jumlah botol supaya balasannya langsung berisi total.</p>
      <p class="teks-kecil">Balasan mengikuti jam buka. Kalau sedang memasak atau mengantar pesanan, balasan bisa agak lambat.</p>
      <p><a class="tombol" href="{escape(tautan)}" target="_blank" rel="noopener">Chat lewat WhatsApp</a></p>
    </div>""" if tautan else """
    <div class="kartu-info">
      <h2>WhatsApp</h2>
      <p>Nomor WhatsApp belum diisi pada <code>data/site.json</code>.</p>
    </div>"""

    bayar = "".join(
        f"""<div class="rekening">
      <h3>{escape(b['nama'])}</h3>
      <dl>
        <dt>Nomor</dt><dd>{escape(b['nomor'])}</dd>
        <dt>Atas nama</dt><dd>{escape(b['atas_nama'])}</dd>
      </dl>
    </div>""" for b in SITE["bayar"]
    )
    qris = ""
    if SITE.get("qris"):
        qris = """
      <figure class="qris">
        <img src="/assets/img/qris.webp" alt="Kode QRIS Jamu Mama Damar, NMID ID1025406177978" width="539" height="760" loading="lazy" decoding="async">
        <figcaption>QRIS atas nama Jamu Mama Damar. Pindai dengan aplikasi bank atau e-wallet, lalu kirim bukti pembayaran.</figcaption>
      </figure>"""

    return kepala(
        "Kontak dan pembayaran, Djamoe Damar",
        "Nomor WhatsApp, alamat kios, jam buka, pembayaran DANA, GoPay, dan QRIS Djamoe Damar di Talaga Bestari.",
        "kontak",
        "/kontak/",
    ) + f"""
<div class="page-head">
  <div class="wrap">
    <p class="label" data-nomor="01">Kontak</p>
    <h1>Pesan, bayar, lalu ambil atau kirim.</h1>
    <p>Semua pesanan diproses lewat WhatsApp supaya varian, jumlah, dan waktu pengambilan bisa langsung dikonfirmasi.</p>
  </div>
</div>
<section class="kontak">
  <div class="wrap kontak__isi">
    <div class="kontak__kolom">
      {kartu_wa}
      <div class="kartu-info">
        <h2>Alamat kios</h2>
        <address>{alamat_html()}</address>
        <p>{escape(SITE["jam"])}.</p>
        <p><a class="tautan" href="{escape(SITE["maps"])}">Buka Google Maps</a></p>
      </div>
      <div class="kartu-info">
        <h2>Instagram</h2>
        <p>Foto varian terbaru dan info stok kadang kami unggah di Instagram.</p>
        <p><a class="tautan" href="{escape(SITE["instagram"])}">{escape(SITE["handle"])}</a></p>
      </div>
    </div>
    <div class="kontak__kolom">
      <div class="kartu-info">
        <h2>Pembayaran</h2>
        <p>Pilih salah satu. Pesanan disiapkan setelah pembayaran dikonfirmasi.</p>
        <div class="daftar-rekening">{bayar}</div>
        {qris}
      </div>
      <div class="kartu-info">
        <h2>Ketentuan pemesanan</h2>
        <ul class="daftar-ketentuan">{blok_ketentuan()}</ul>
        <p class="teks-kecil">Sertifikat halal dan sertifikat merek bisa dilihat di <a class="tautan" href="/tentang/#legalitas">halaman Tentang</a>.</p>
      </div>
    </div>
  </div>
</section>
""" + kaki()


def halaman_404():
    return kepala(
        "Halaman tidak ditemukan, Djamoe Damar",
        "Halaman yang kamu cari tidak ada.",
        "beranda",
        "/404.html",
    ) + """
<section class="hero hero--404">
  <div class="wrap">
    <p class="label" data-nomor="404">Tidak ditemukan</p>
    <h1>Halaman ini tidak ada.</h1>
    <p class="hero__teks">Mungkin tautannya salah ketik. Daftar varian dan harga ada di halaman menu.</p>
    <div class="hero__aksi">
      <a class="tombol" href="/menu/">Lihat varian</a>
      <a class="tombol tombol--outline" href="/">Kembali ke beranda</a>
    </div>
  </div>
</section>
""" + kaki()


# ---------------------------------------------------------------- main
def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(IMG, exist_ok=True)
    foto = siapkan_gambar()
    sertifikat = siapkan_sertifikat()
    testimoni = siapkan_testimoni()

    tulis("index.html", halaman_beranda(foto, testimoni))
    tulis("menu/index.html", halaman_menu(foto))
    tulis("tentang/index.html", halaman_tentang(sertifikat))
    tulis("kontak/index.html", halaman_kontak())
    tulis("404.html", halaman_404())

    for nama in ("style.css", "site.js"):
        sub = "css" if nama.endswith(".css") else "js"
        tujuan = os.path.join(DIST, "assets", sub, nama)
        os.makedirs(os.path.dirname(tujuan), exist_ok=True)
        shutil.copy(os.path.join(ROOT, "assets", sub, nama), tujuan)

    if SITE.get("url"):
        halaman = ["", "menu/", "tentang/", "kontak/"]
        urls = "".join(
            "  <url><loc>%s/%s</loc></url>\n" % (SITE["url"].rstrip("/"), h) for h in halaman
        )
        tulis("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
              + urls + "</urlset>\n")
        tulis("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"
              % SITE["url"].rstrip("/"))
    else:
        tulis("robots.txt", "User-agent: *\nAllow: /\n")

    jumlah = sum(len(f) for _, _, f in os.walk(DIST))
    ukuran = 0
    for akar, _, berkas in os.walk(DIST):
        for b in berkas:
            ukuran += os.path.getsize(os.path.join(akar, b))
    print("halaman: 5")
    print("berkas: %d, total %.1f KB" % (jumlah, ukuran / 1024))


if __name__ == "__main__":
    main()
