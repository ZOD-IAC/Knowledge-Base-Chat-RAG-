import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="Knowledge Base Chat", page_icon="🧠")
st.title("🧠 Personal Knowledge Base Chat")

# Upload section
st.header("1. Upload a PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Ingesting document..."):
        res = requests.post(
            f"{API}/upload",
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )
        data = res.json()
        st.success(f"Done! Ingested {data['chunks']} chunks from '{uploaded_file.name}'")
        st.session_state["collection"] = data["collection"]

# Chat section
if "collection" in st.session_state:
    st.header("2. Ask a Question")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask something about your document...")
    if question:
        st.session_state["messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                res = requests.post(f"{API}/query", json={
                    "question": question,
                    "collection_name": st.session_state["collection"]
                })
                print(res ,'<-----')
                answer = res.json()["answer"]
                st.write(answer)
                st.session_state["messages"].append({"role": "assistant", "content": answer})