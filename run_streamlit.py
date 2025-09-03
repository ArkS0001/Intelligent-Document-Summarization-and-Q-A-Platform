import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📄 Agentic Document Summarizer & QnA")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    resp = requests.post(f"{API_URL}/ingest", files={"file": uploaded_file})
    if resp.status_code == 200:
        result = resp.json()
        st.write("### Summary")
        st.write(result["summary"])
        st.write("### Entities")
        st.write(result["entities"])
    else:
        st.error("Failed to process document")

query = st.text_input("Ask a question about your documents")
if query:
    resp = requests.get(f"{API_URL}/ask", params={"query": query})
    if resp.status_code == 200:
        st.write("### Answer")
        st.write(resp.json()["answer"])
    else:
        st.error("Failed to get answer")
