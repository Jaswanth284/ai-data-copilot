import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="AI Data Copilot", page_icon="🤖", layout="centered")

st.title("🤖 AI Data Copilot")
st.caption("Upload-aware dataset assistant powered by FastAPI and OpenAI")

filename = st.text_input("Dataset filename", value="sample.csv")
question = st.text_area(
    "Ask a question about your dataset",
    placeholder="Example: What is the total revenue and which customer has the highest revenue?"
)

if st.button("Ask AI"):
    if not filename.strip() or not question.strip():
        st.warning("Please enter both filename and question.")
    else:
        payload = {
            "filename": filename.strip(),
            "question": question.strip()
        }

        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(f"{API_URL}/ai/ask", json=payload, timeout=60)

                if response.status_code == 200:
                    data = response.json()
                    st.success("AI response generated")
                    st.markdown("### Answer")
                    st.write(data.get("answer", "No answer found"))
                    st.markdown("### Source")
                    st.info(data.get("source", "N/A"))
                else:
                    st.error(f"Backend error: {response.status_code}")
                    st.json(response.json())

            except Exception as e:
                st.error(f"Could not connect to backend: {str(e)}")