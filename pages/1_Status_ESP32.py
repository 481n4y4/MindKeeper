import streamlit as st
from esp_status import is_esp_connected

st.set_page_config(page_title="Status ESP32 - MindKeeper", layout="centered")
st.title("🔌 Status Koneksi ESP32")

if is_esp_connected():
    st.success("✅ ESP32 Terhubung ke laptop melalui USB.")
else:
    st.warning("⚠️ ESP32 belum terdeteksi di port USB.")
