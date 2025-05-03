import streamlit as st
from firebase_config import get_data, set_data, db
from gemini_chat import ask_gemini
import time

# 🔧 Inisialisasi session_state SEBELUM digunakan
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "Chat 1"
if st.session_state.current_chat_id not in st.session_state.chat_sessions:
    st.session_state.chat_sessions[st.session_state.current_chat_id] = []

st.set_page_config(page_title="MindKeeper", layout="centered")
st.title("🧠 MindKeeper Dashboard")
st.write("Kontrol perangkat fokus & bantuan AI")

# Ambil status dari Firebase
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

# =============== Fokus Timer Section ===================
with st.expander("⏱️ Atur Sesi Fokus", expanded=True):
    duration = st.slider("Durasi Fokus (menit)", 5, 90, 25)

    col1, col2 = st.columns(2)
    if col1.button("Mulai Fokus"):
        db.child("focus").set(True)
        db.child("timer").set(duration * 60)
        st.success("Fokus dimulai!")
        st.experimental_rerun()

    if col2.button("Akhiri Fokus"):
        db.child("focus").set(False)
        db.child("timer").set(0)
        st.warning("Fokus dihentikan.")
        st.experimental_rerun()

    st.info(f"Status Fokus: **{'AKTIF' if focus_state else 'NONAKTIF'}**")

    # Countdown timer yang tidak mengganggu elemen lain
    timer_placeholder = st.empty()
    notif_placeholder = st.empty()

    if focus_state and timer_state > 0:
        mins, secs = divmod(timer_state, 60)
        timer_placeholder.markdown(f"⏳ Timer tersisa: **{mins:02d}:{secs:02d}**", unsafe_allow_html=True)
        # Update timer tanpa blocking loop
        time.sleep(1)
        db.child("timer").set(timer_state - 1)
    elif focus_state and timer_state <= 0:
        db.child("focus").set(False)
        db.child("timer").set(0)
        notif_placeholder.success("🎉 Sesi Fokus selesai!")
    else:
        mins, secs = divmod(timer_state, 60)
        timer_placeholder.markdown(f"🕒 Timer tersisa: **{mins:02d}:{secs:02d}**", unsafe_allow_html=True)

# =============== Sidebar: Kamera & Chat ===============
with st.sidebar:
    st.markdown("## 📷 Kamera")
    st.link_button("Go to Camera", "http://192.168.1.23")  # Ganti sesuai alamat kamera

    st.markdown("## ✏️ Obrolan")
    if st.button("➕ Obrolan Baru"):
        new_id = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[new_id] = []
        st.session_state.current_chat_id = new_id

    st.markdown("### 💬 Daftar Obrolan")
    for chat_id in list(st.session_state.chat_sessions.keys()):
        is_active = chat_id == st.session_state.current_chat_id
        with st.container():
            cols = st.columns([6, 1])
            with cols[0]:
                if st.button(chat_id, key=f"select_{chat_id}"):
                    st.session_state.current_chat_id = chat_id
            with cols[1]:
                if st.button("⋮", key=f"menu_{chat_id}"):
                    st.session_state[f"menu_open_{chat_id}"] = not st.session_state.get(f"menu_open_{chat_id}", False)

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

# =============== Chat UI ===============================
st.markdown("---")
st.subheader("🤖 MindKeeper AI Chat")

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "Chat 1"
if st.session_state.current_chat_id not in st.session_state.chat_sessions:
    st.session_state.chat_sessions[st.session_state.current_chat_id] = []

chat_history = st.session_state.chat_sessions[st.session_state.current_chat_id]
for msg in chat_history:
    with st.chat_message("user"):
        st.markdown(msg["question"])
    with st.chat_message("assistant"):
        st.markdown(msg["answer"])

if prompt := st.chat_input("Tanya ke MindKeeper..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("MindKeeper sedang berpikir..."):
        response = ask_gemini(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.chat_sessions[st.session_state.current_chat_id].append({
        "question": prompt,
        "answer": response
    })

    current_id = st.session_state.current_chat_id
    if current_id.startswith("Chat ") and len(st.session_state.chat_sessions[current_id]) == 1:
        new_title = " ".join(prompt.strip().split()[:5])
        if new_title and new_title not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[new_title] = st.session_state.chat_sessions.pop(current_id)
            st.session_state.current_chat_id = new_title
            st.rerun()
