import streamlit as st

st.set_page_config(page_title="Live Kamera - MindKeeper", layout="centered")
st.title("📷 Live Kamera ESP32-CAM")
st.caption("Pastikan ESP32-CAM dan laptop terhubung ke WiFi yang sama.")

# Ganti IP di bawah ini dengan IP ESP32-CAM milikmu
esp32cam_ip = "http://192.168.67.99"

st.markdown("### 🔴 Streaming Kamera")
st.components.v1.html(f"""
    <div style="text-align: center;">
        <img src="{esp32cam_ip}/stream" width="480" height="360" style="border: 1px solid #ccc; border-radius: 8px;" />
    </div>
""", height=400)
