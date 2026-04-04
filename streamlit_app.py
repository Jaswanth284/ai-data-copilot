import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "https://ai-data-copilot-api.onrender.com")

st.set_page_config(page_title="AI Data Copilot", page_icon="🤖", layout="centered")

st.title("🤖 AI Data Copilot")
st.caption("Ask questions on your dataset using real RAG + OpenAI")

filename = st.text_input("Dataset filename", value="sample.csv")
question = st.text_area(
    "Ask a question about your dataset",
    placeholder="Example: Which customer has the highest revenue?"
)

top_k = st.slider("Number of retrieved chunks", min_value=1, max_value=5, value=3)

col1, col2 = st.columns(2)

with col1:
    if st.button("Create RAG Index"):
        if not filename.strip():
            st.warning("Please enter a dataset filename.")
        else:
            payload = {"filename": filename.strip()}

            with st.spinner("Creating RAG index..."):
                try:
                    response = requests.post(f"{API_URL}/rag/index", json=payload, timeout=60)

                    if response.status_code == 200:
                        data = response.json()
                        st.success("RAG index created successfully")
                        st.json(data)
                    else:
                        st.error(f"Backend error: {response.status_code}")
                        st.json(response.json())

                except Exception as e:
                    st.error(f"Could not connect to backend: {str(e)}")

with col2:
    if st.button("Ask with RAG"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            payload = {
                "question": question.strip(),
                "top_k": top_k
            }

            with st.spinner("Retrieving relevant chunks and generating answer..."):
                try:
                    response = requests.post(f"{API_URL}/rag/ask", json=payload, timeout=60)

                    if response.status_code == 200:
                        data = response.json()

                        st.success("RAG response generated")

                        st.markdown("### Answer")
                        st.write(data.get("answer", "No answer found"))

                        st.markdown("### Source")
                        st.info(data.get("source", "N/A"))

                        st.markdown("### Retrieved Chunks")
                        retrieved_chunks = data.get("retrieved_chunks", [])
                        if retrieved_chunks:
                            for i, chunk in enumerate(retrieved_chunks, start=1):
                                st.markdown(f"**Chunk {i}:**")
                                st.code(chunk)
                        else:
                            st.write("No retrieved chunks found.")

                    else:
                        st.error(f"Backend error: {response.status_code}")
                        st.json(response.json())

                except Exception as e:
                    st.error(f"Could not connect to backend: {str(e)}")