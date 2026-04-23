import streamlit as st
from pet import AIPet
from rag import RAGPipeline
import base64

st.set_page_config(page_title="AI Pet", page_icon="🐾")
st.title("🐾 AI Pet — Study Assistant")

# Sidebar - Subject Selection
st.sidebar.title("Your Pet")
subject = st.sidebar.selectbox(
    "Choose subject:",
    ["Machine Learning", "Python", "Data Structures", "Math"]
)

# Initialize Pet
if "pet" not in st.session_state or st.session_state.get("current_subject") != subject:
    st.session_state.pet = AIPet("Nova", subject)
    st.session_state.current_subject = subject
    st.session_state.chat_history = []

# Initialize RAG
if "rag" not in st.session_state:
    with st.spinner("Loading RAG pipeline..."):
        safe_subject = subject.replace(" ", "_")
        st.session_state.rag = RAGPipeline(collection_name=f"notes_{safe_subject}")

st.sidebar.divider()
st.sidebar.title("📚 Upload Material")

uploaded_file = st.sidebar.file_uploader("Upload notes (PDF/TXT) or Image", type=["txt", "pdf", "png", "jpg"])

# Logic for handling files
if uploaded_file is not None:
    # 1. Handle Images
    if uploaded_file.type in ["image/png", "image/jpeg"]:
        st.sidebar.image(uploaded_file)
        if st.sidebar.button("Analyze Image"):
            with st.spinner("Nova is looking..."):
                img_bytes = uploaded_file.getvalue()
                base64_img = base64.b64encode(img_bytes).decode('utf-8')
                response = st.session_state.pet.chat("What is in this image?", base64_img)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    # 2. Handle Documents (PDF/TXT)
    else:
        file_content = ""
        if uploaded_file.type == "application/pdf":
            from pypdf import PdfReader
            import io
            reader = PdfReader(io.BytesIO(uploaded_file.read()))
            for page in reader.pages:
                text = page.extract_text()
                if text: file_content += text
        else:
            file_content = uploaded_file.read().decode("utf-8")

        if st.sidebar.button("✅ Process Notes"):
            with st.spinner("Processing..."):
                num_chunks = st.session_state.rag.add_document(file_content, uploaded_file.name)
                st.sidebar.success(f"Added {num_chunks} chunks!")

# Chat Interface
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Ask Nova anything..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        # RAG Logic
        sources = st.session_state.rag.search_with_sources(user_input)
        context = "\n\n".join([chunk for chunk, dist in sources])

        if context.strip():
            # Show sources
            source_info = "🔍 **Found in notes:**\n"
            for i, (chunk, dist) in enumerate(sources):
                source_info += f"- Match {i+1}: _{chunk[:100]}..._\n"
            st.info(source_info)
            
            # RAG prompt
            rag_prompt = (
                f"Use this context to answer: \n{context}\n\n"
                f"Question: {user_input}"
            )
            response = st.session_state.pet.chat(rag_prompt)
        else:
            response = st.session_state.pet.chat(user_input)
        
        st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})