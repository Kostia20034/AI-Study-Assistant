import streamlit as st
from pet import AIPet
from rag import RAGPipeline


st.set_page_config(page_title="AI Pet", page_icon="🐾")
st.title("🐾 AI Pet — Study Assistant")

# sidebar — pick your subject
st.sidebar.title("Your Pet")
subject = st.sidebar.selectbox(
    "Choose subject:",
    ["Machine Learning", "Python", "Data Structures", "Math"]
)

# initialize pet with name, subject and chat history
if "pet" not in st.session_state or st.session_state.get("current_subject") != subject:
    st.session_state.pet = AIPet("Nova", subject)
    st.session_state.current_subject = subject
    st.session_state.chat_history = []
 #intialize db with subject category
if "rag" not in st.session_state:
    with st.spinner("Loading RAG pipeline..."):
        safe_subject = subject.replace(" ", "_")
        st.session_state.rag = RAGPipeline(collection_name=f"notes_{safe_subject}")   
    
st.sidebar.divider()
st.sidebar.title("📚 Upload Notes")
#upload file menu
uploaded_file = st.sidebar.file_uploader(
    "Upload your class notes",
    type=["txt", "pdf"]
)
#process pdf or text file
if uploaded_file is not None:
    # read the file
    if uploaded_file.type == "application/pdf":
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        file_content = ""
        for page in reader.pages:
            file_content += page.extract_text()
    else:
        file_content = uploaded_file.read().decode("utf-8")
    

    # feed content to Nova
    if "file_loaded" not in st.session_state or st.session_state.file_loaded != uploaded_file.name:
        st.session_state.file_loaded = uploaded_file.name
        
        with st.spinner("Processing your notes..."):
            num_chunks = st.session_state.rag.add_document(
                file_content,
                uploaded_file.name
            )
        
        confirmation = f"📚 I've processed your notes into {num_chunks} searchable chunks. Ask me anything about them!"
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": confirmation
        })
        st.sidebar.success(f"✅ {uploaded_file.name} loaded!")
        
# display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar="🐾"):
            st.write(message["content"])

# chat input at bottom
user_input = st.chat_input("Davai zadavai")

if user_input:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Nova is thinking..."):
        if user_input == "quiz":
            response = st.session_state.pet.quiz_me()
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
        else:
            # get chunks with sources
            sources = st.session_state.rag.search_with_sources(user_input)
            context = "\n\n".join([chunk for chunk, distance in sources])

            if context.strip():
                # build source message — your idea
                source_message = "🔍 **RAG found these matches from your notes:**\n\n"
                for i, (chunk, distance) in enumerate(sources):
                    # convert distance to similarity percentage
                    similarity = round((1 - distance) * 100)
                    source_message += f"**Match {i+1}** ({similarity}% similar):\n_{chunk[:150]}..._\n\n"

                # add source message to chat
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": source_message
                })

                # now get Nova's actual response
                response = st.session_state.pet.chat(f"""
Use this context from the student's notes to answer the question.
If the context doesn't contain the answer, use your own knowledge.

Context:
{context}

Question: {user_input}
""")
            else:
                response = st.session_state.pet.chat(user_input)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })

    st.rerun()
