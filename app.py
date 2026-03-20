import streamlit as st
from pet import AIPet

# page config
st.set_page_config(page_title="AI Pet", page_icon="🐾")

# title
st.title("🐾 AI Pet — Study Assistant")

# sidebar — pick your subject
st.sidebar.title("Your Pet")
subject = st.sidebar.selectbox(
    "Choose subject:",
    ["Machine Learning", "Python", "Data Structures", "Math"]
)

# initialize pet in session state — persists between reruns
if "pet" not in st.session_state:
    st.session_state.pet = AIPet("Nova", subject)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
st.sidebar.divider()
st.sidebar.title("📚 Upload Notes")

uploaded_file = st.sidebar.file_uploader(
    "Upload your class notes",
    type=["txt", "pdf"]
)

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
        conformation = st.session_state.pet.chat(
            f"""I am giving you the following study material. 
            Read it carefully and use it to answer my questions:
            
            {file_content}
            
            Confirm you have read it in one short sentence."""
        )
        st.session_state.chat_history.append({
        "role": "assistant",
        "content": f"📚 File loaded! {conformation}"
        })
        st.sidebar.success(f"✅ {uploaded_file.name} loaded!")
# display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

# chat input at bottom
user_input = st.chat_input("Ask Nova anything...")

if user_input:
    # add user message to display
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    # get response from Nova
    with st.spinner("Nova is thinking..."):
        if user_input == "quiz":
            response = st.session_state.pet.quiz_me()
        else:
            response = st.session_state.pet.chat(user_input)

    # add response to display
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

    # rerun to show new messages
    st.rerun()
