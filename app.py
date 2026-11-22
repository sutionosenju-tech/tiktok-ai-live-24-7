import streamlit as st
import subprocess
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="TikTok AI LIVE 24/7", page_icon="🎥", layout="wide")
st.title("🎥 TikTok AI LIVE 24/7")
st.caption("MVP khusus TikTok: video loop melalui RTMP, naskah presenter, dan simulasi komentar.")

if "proc" not in st.session_state:
    st.session_state.proc = None
if "chat" not in st.session_state:
    st.session_state.chat = []
if "script" not in st.session_state:
    st.session_state.script = ""

def is_running():
    p = st.session_state.proc
    return p is not None and p.poll() is None

def answer(q):
    q = q.lower()
    if any(x in q for x in ["halo", "hai", "pagi", "malam", "assalam"]):
        return "Halo, selamat datang di LIVE! Terima kasih sudah bergabung. Silakan bertanya."
    if any(x in q for x in ["bibit", "benih", "sawit"]):
        return "Untuk memilih bibit sawit, periksa label, asal sumber benih, dan dokumen pendukungnya. Jangan hanya mengandalkan klaim penjual."
    if any(x in q for x in ["harga", "berapa", "biaya"]):
        return "Harga dapat berbeda menurut produk, lokasi, dan waktu. Sebutkan detailnya agar bisa dijawab lebih tepat."
    return "Terima kasih sudah bertanya! Boleh tambahkan sedikit detail supaya saya bisa menjawab dengan lebih tepat."

with st.sidebar:
    st.header("Pengaturan TikTok")
    st.info("Masukkan URL RTMP dan Stream Key yang diberikan TikTok. Jangan bagikan Stream Key.")
    server = st.text_input("TikTok Server URL", placeholder="rtmp://...")
    key = st.text_input("TikTok Stream Key", type="password")
    videos_text = st.text_area("Path video MP4 (satu per baris)", "media/live_loop.mp4", height=100)

a, b = st.columns(2)
with a:
    st.subheader("🗣️ Naskah presenter")
    topic = st.text_input("Topik LIVE", "Obrolan santai dan tanya jawab")
    if st.button("Buat naskah pembuka"):
        st.session_state.script = f"Halo semuanya! Selamat datang di TikTok LIVE kami. Hari ini kita membahas {topic.lower()}. Silakan tulis pertanyaan di komentar. Saya akan berusaha menjawab dengan jelas. Terima kasih sudah bergabung!"
    st.text_area("Naskah", key="script", height=160)
    st.caption("Naskah ini belum dibacakan otomatis. TTS dan avatar AI akan menjadi tahap berikutnya.")

with b:
    st.subheader("💬 Panel komentar")
    st.warning("Mode demo/manual. Belum terhubung langsung ke komentar TikTok.")
    q = st.text_input("Masukkan komentar contoh")
    if st.button("Buat jawaban"):
        if q.strip():
            st.session_state.chat.append((datetime.now().strftime("%H:%M:%S"), q.strip(), answer(q)))
    for tm, question, response in reversed(st.session_state.chat[-8:]):
        st.markdown(f"**Penonton ({tm}):** {question}")
        st.markdown(f"**Jawaban AI demo:** {response}")

st.divider()
st.subheader("🔴 Kontrol streaming TikTok RTMP")
c1, c2 = st.columns(2)
with c1:
    if st.button("▶ MULAI LIVE", type="primary", use_container_width=True):
        if is_running():
            st.info("Streaming sudah berjalan.")
        elif not server.strip() or not key.strip():
            st.error("Isi Server URL dan Stream Key terlebih dahulu.")
        else:
            videos = [x.strip() for x in videos_text.splitlines() if x.strip()]
            missing = [x for x in videos if not Path(x).is_file()]
            if not videos or missing:
                st.error("Video tidak ditemukan: " + ", ".join(missing or ["masukkan path video"]))
            else:
                # Satu video diputar berulang; playlist multi-video dapat ditambahkan pada versi lanjutan.
                destination = server.rstrip("/") + "/" + key.strip()
                cmd = ["ffmpeg", "-hide_banner", "-loglevel", "warning",
                       "-stream_loop", "-1", "-re", "-i", videos[0],
                       "-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency",
                       "-pix_fmt", "yuv420p", "-r", "30", "-g", "60",
                       "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                       "-f", "flv", destination]
                try:
                    st.session_state.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    st.success("FFmpeg dimulai. Periksa preview/status LIVE di TikTok.")
                except FileNotFoundError:
                    st.error("FFmpeg belum terpasang atau tidak tersedia di PATH.")
                except Exception as e:
                    st.error(f"Gagal memulai: {e}")
with c2:
    if st.button("⏹ HENTIKAN LIVE", use_container_width=True):
        if is_running():
            st.session_state.proc.terminate()
            st.session_state.proc = None
            st.success("Perintah berhenti dikirim.")
        else:
            st.info("Tidak ada streaming aktif.")

if is_running():
    st.success("Status lokal: proses FFmpeg berjalan.")
else:
    st.info("Status lokal: streaming tidak aktif.")

st.error("Batasan MVP: belum membaca komentar TikTok secara langsung, belum menjawab dengan suara, dan belum memiliki avatar AI. Komentar otomatis harus memakai integrasi yang diizinkan dan tersedia untuk akun Anda. Streaming 24/7 memerlukan PC/server dan internet yang selalu aktif.")
