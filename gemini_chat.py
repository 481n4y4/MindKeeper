import google.generativeai as genai

# Set API Key
genai.configure(api_key="AIzaSyB6FwS-ydW95Nc9kWRAmzFCInegtLPVJBg")

model = genai.GenerativeModel("gemini-1.5-pro")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text
