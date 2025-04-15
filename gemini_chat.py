import requests
import streamlit as st

API_KEY = st.secrets["GEMINI_API_KEY"]
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

def ask_gemini(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": API_KEY
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(API_URL, headers=headers, params=params, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"❌ Gagal menjawab. Status code: {response.status_code}"
