import streamlit as st
from firebase_config import get_data, set_data
from gemini_chat import ask_gemini
import streamlit as st
from esp_status import is_esp_connected

st.set_page_config(page_title="MindKeeper", layout="centered")
st.title("🧠 MindKeeper Dashboard")
st.write("Kontrol perangkat fokus & bantuan AI")


# === Ambil status dari Firebase terlebih dulu ===
try:
    focus_state = get_data("focus")
    timer_state = get_data("timer")
except Exception as e:
    st.error("Gagal baca dari Firebase")
    st.error(str(e))
    db.child("focus").set(False)
    db.child("timer").set(0)
    focus_state = False
    timer_state = 0

# === Fokus Timer === (dalam expandable)
with st.expander("⏱️ Atur Sesi Fokus", expanded=False):
    duration = st.slider("Durasi Fokus (menit)", 5, 90, 25)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Mulai Fokus"):
            db.child("focus").set(True)
            db.child("timer").set(duration * 60)
            st.success("Fokus dimulai!")

    with col2:
        if st.button("Akhiri Fokus"):
            db.child("focus").set(False)
            db.child("timer").set(0)
            st.warning("Fokus dihentikan.")

    st.info(f"Status Fokus: **{'AKTIF' if focus_state else 'NONAKTIF'}**")
    st.text(f"Timer tersisa: {timer_state} detik")


# === AI Assistant ===
st.markdown("---")
st.subheader("🤖 MindKeeper AI Chat")

# Inisialisasi histori chat dan chat saat ini
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}  # {id: list of messages}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "Chat 1"
if st.session_state.current_chat_id not in st.session_state.chat_sessions:
    st.session_state.chat_sessions[st.session_state.current_chat_id] = []

# Sidebar: Riwayat & tombol buat chat baru + edit/hapus
with st.sidebar:
    st.markdown("## ✏️ Obrolan")
    if st.button("➕ Obrolan Baru"):
        new_id = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[new_id] = []
        st.session_state.current_chat_id = new_id

    st.markdown("### 💬 Daftar Obrolan")
    chat_ids = list(st.session_state.chat_sessions.keys())
    for chat_id in chat_ids:
        is_active = chat_id == st.session_state.current_chat_id
        with st.container():
            cols = st.columns([6, 1])
            with cols[0]:
                if st.button(chat_id, key=f"select_{chat_id}"):
                    st.session_state.current_chat_id = chat_id
            with cols[1]:
                if st.button("⋮", key=f"menu_{chat_id}"):
                    st.session_state[f"menu_open_{chat_id}"] = not st.session_state.get(f"menu_open_{chat_id}", False)

            # Dropdown opsional
            if st.session_state.get(f"menu_open_{chat_id}", False):
                with st.container():
                    new_name = st.text_input("Ganti nama:", value=chat_id, key=f"input_{chat_id}")
                    if st.button("Simpan Nama", key=f"save_{chat_id}"):
                        if new_name and new_name != chat_id and new_name not in st.session_state.chat_sessions:
                            st.session_state.chat_sessions[new_name] = st.session_state.chat_sessions.pop(chat_id)
                            if st.session_state.current_chat_id == chat_id:
                                st.session_state.current_chat_id = new_name
                            st.rerun()

                    if st.button("🗑️ Hapus Chat", key=f"delete_{chat_id}"):
                        del st.session_state.chat_sessions[chat_id]
                        if st.session_state.current_chat_id == chat_id:
                            st.session_state.current_chat_id = (
                                list(st.session_state.chat_sessions.keys())[0]
                                if st.session_state.chat_sessions else None
                            )
                        st.experimental_rerun()

    st.markdown("---")
    st.caption("Klik nama untuk membuka. Gunakan ⋮ untuk opsi ganti nama / hapus.")


# Tampilan chat UI
chat_history = st.session_state.chat_sessions[st.session_state.current_chat_id]
for msg in chat_history:
    with st.chat_message("user"):
        st.markdown(msg["question"])
    with st.chat_message("assistant"):
        st.markdown(msg["answer"])

# Input pertanyaan
if prompt := st.chat_input("Tanya ke MindKeeper..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("MindKeeper sedang berpikir..."):
        response = ask_gemini(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    # Simpan ke histori aktif
    st.session_state.chat_sessions[st.session_state.current_chat_id].append({
        "question": prompt,
        "answer": response
    })

    # Jika nama chat masih default (misal Chat 1, Chat 2, dst), update berdasarkan pertanyaan
    current_id = st.session_state.current_chat_id
    if current_id.startswith("Chat ") and len(st.session_state.chat_sessions[current_id]) == 1:
        # Ambil max 5 kata dari prompt sebagai judul
        new_title = " ".join(prompt.strip().split()[:5])
        if new_title and new_title not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[new_title] = st.session_state.chat_sessions.pop(current_id)
            st.session_state.current_chat_id = new_title
            st.rerun()


    # Simpan ke histori aktif
    st.session_state.chat_sessions[st.session_state.current_chat_id].append({
        "question": prompt,
        "answer": response
    })

    st.title("MindKeeper: Kamera Live")
st.markdown("### Live Kamera dari ESP32-CAM")

# Ganti IP sesuai output Serial Monitor ESP32-CAM
esp_ip = "http://192.168.67.99/stream"

st.components.v1.html(f"""
    <div style="text-align: center;">
        <img src="{esp_ip}/stream" width="480" height="360" />
    </div>
""", height=400)

connected = get_data("status/connected")
if connected:
    st.success("✅ ESP32 terhubung (via Firebase)")
else:
    st.warning("⚠️ ESP32 belum mengirim sinyal")

st.set_page_config(page_title="MindKeeper", layout="centered")
st.title("🧠 MindKeeper AI Dashboard")
st.markdown("""
Selamat datang di **MindKeeper**!

Gunakan sidebar di kiri untuk mengakses:
- Kamera live dari ESP32-CAM
- Status koneksi perangkat ESP32
- Fokus session control (jika ada)
""")
