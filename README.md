# TikTok AI LIVE 24/7 — MVP

## Menjalankan
1. Instal Python 3.10+.
2. Instal FFmpeg dan pastikan perintah `ffmpeg` tersedia di terminal.
3. Ekstrak ZIP ini.
4. Buka terminal pada folder proyek.
5. Jalankan `pip install -r requirements.txt`.
6. Jalankan `streamlit run app.py`.
7. Letakkan video MP4 di folder `media/` dan ubah path-nya di sidebar.
8. Masukkan TikTok Server URL dan Stream Key yang diberikan TikTok, lalu tekan MULAI LIVE.

## Keamanan dan batasan
- Jangan unggah Stream Key ke GitHub atau membagikannya.
- Gunakan hanya akses RTMP/encoder yang resmi tersedia pada akun TikTok Anda.
- Versi ini melakukan streaming video loop melalui FFmpeg.
- Panel komentar masih demo/manual; belum membaca komentar TikTok langsung.
- Belum ada TTS otomatis dan avatar lip-sync.
- Streaming 24 jam memerlukan komputer/server yang terus aktif dan internet stabil; hosting gratis biasanya tidak menjamin uptime.
- Gunakan video yang Anda miliki haknya dan patuhi pedoman TikTok.

## Upgrade berikutnya
Integrasi komentar yang diizinkan, moderasi, TTS bahasa Indonesia, avatar presenter, auto-reconnect, dan monitoring.
