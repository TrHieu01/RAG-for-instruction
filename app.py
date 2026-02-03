
import streamlit as st
import os
import tempfile
from src.ingestion import ingest_file
from src.retrieval import get_advanced_retriever_chain
from src.llm import generate_response
from src.memory import UserMemory
from src.vector_db import list_documents, delete_document

# Page Config
st.set_page_config(page_title="Antigravity Vibe RAG", page_icon="🌌", layout="wide")

# Custom CSS for Premium Aesthetics
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables for Color Palette */
    :root {
        --primary-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        --accent-color: #e94560;
        --accent-secondary: #7b68ee;
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-primary: #f5f5f5;
        --text-secondary: #b0b0b0;
    }
    
    /* Main App Background */
    .stApp {
        background: var(--primary-gradient);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Title Styling */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e94560 0%, #7b68ee 50%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 5px rgba(233, 69, 96, 0.3)); }
        to { filter: drop-shadow(0 0 20px rgba(123, 104, 238, 0.5)); }
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
        border-right: 1px solid var(--glass-border);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3rem;
        font-weight: 600;
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 1rem;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: var(--glass-bg);
        border: 1px dashed var(--accent-secondary);
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-color);
        background: rgba(233, 69, 96, 0.05);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(233, 69, 96, 0.5);
    }
    
    /* Chat Messages Container */
    [data-testid="stChatMessageContainer"] {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatMessageContainer"]:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    /* User Message */
    [data-testid="stChatMessageContainer"][data-testid*="user"] {
        border-left: 3px solid var(--accent-color);
    }
    
    /* Assistant Message */
    [data-testid="stChatMessageContainer"][data-testid*="assistant"] {
        border-left: 3px solid var(--accent-secondary);
    }
    
    /* Chat Input - Force Dark Background with Light Text */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    .stChatInput,
    .stChatInput > div,
    .stChatInputContainer,
    [data-testid="stChatInputContainer"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 2px solid #7b68ee !important;
        border-radius: 25px !important;
    }
    
    /* All text inputs inside chat */
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input,
    .stChatInput textarea,
    .stChatInput input,
    [data-testid="stChatInputContainer"] textarea,
    [data-testid="stChatInputContainer"] input,
    .stChatInput div[data-baseweb] textarea,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="input"] input {
        background: transparent !important;
        background-color: transparent !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        caret-color: #e94560 !important;
    }
    
    /* Placeholder text */
    [data-testid="stChatInput"] textarea::placeholder,
    .stChatInput textarea::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: #666666 !important;
        -webkit-text-fill-color: #666666 !important;
        opacity: 1 !important;
    }
    
    /* Focus state */
    [data-testid="stChatInput"]:focus-within,
    .stChatInput:focus-within {
        border-color: #e94560 !important;
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.3) !important;
    }
    
    /* Override any inline styles */
    .stChatInput * {
        color: #00ff00 !important;
    }
    
    .stChatInput textarea {
        color: #00ff00 !important;
        -webkit-text-fill-color: #00ff00 !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: var(--accent-color) transparent transparent transparent;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-color);
    }
    
    /* Markdown Text in Chat */
    .stMarkdown {
        color: var(--text-primary);
    }
    
    .stMarkdown p {
        line-height: 1.7;
    }
    
    .stMarkdown code {
        background: rgba(123, 104, 238, 0.2);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    .stMarkdown pre {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Info Card in Sidebar */
    .info-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .info-card h4 {
        color: var(--accent-secondary);
        margin-bottom: 0.5rem;
    }
    
    .info-card p {
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<h1 class="main-title">🌌 Antigravity Vibe RAG</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent Document Assistant powered by Advanced RAG</p>', unsafe_allow_html=True)

# Global State Init
if "is_ingesting" not in st.session_state:
    st.session_state.is_ingesting = False
if "data_version" not in st.session_state:
    st.session_state.data_version = 0

@st.cache_resource
def get_retriever(user_id=None, version=0):
    """
    Retriever cache depends on data version. 
    When data changes, version increments -> new retriever created.
    """
    return get_advanced_retriever_chain(user_id=user_id)

@st.cache_resource
def get_shared_memory_client():
    """Initialize the heavy Memory object once and share it."""
    # We initialize with a system ID, but we only care about the .memory object
    try:
        # Check if lock file exists to fast fail or clean up
        lock_file = "./mem0_storage_v4/.lock"
        if os.path.exists(lock_file):
            # In a real prod environment we might wait, but for local app
            # we can try to warn or sometimes the lock is stale.
            pass

        init_mem = UserMemory(user_id="SYSTEM_INIT")
        return init_mem.memory
    except RuntimeError as e:
        if "already accessed" in str(e):
            st.warning("⚠️ Database is locked. Attempting to use temporary memory for this session.")
            # Fallback to an in-memory instance if possible or a slightly different config
            # Here we just stop to be safe, but we could return a mock
            st.error("🔒 Database file is locked by a lingering process. Please Restart the Terminal.")
            raise e
        return None

# Sidebar
with st.sidebar:
    st.markdown('<p class="sidebar-header">👤 User Profile</p>', unsafe_allow_html=True)
    
    # User Selection
    user_id = st.text_input("User ID / Name", value="user_1", help="Enter a unique name to load your personal memory.")
    
    # Reload memory if user changes or not set
    # We use the shared client to avoid file locking issues
    try:
        shared_mem_client = get_shared_memory_client()
    except Exception:
        st.stop()
    
    if "current_user_id" not in st.session_state or st.session_state.current_user_id != user_id:
        st.session_state.current_user_id = user_id
        st.session_state.user_memory = UserMemory(user_id=user_id, memory_client=shared_mem_client)
        st.session_state.messages = [] # Reset chat for new user
        # We don't necessarily need to rerun immediately if we just set the state, 
        # but rerunning ensures the UI reflects the new user's context everywhere
        st.rerun()

    # Display Memory
    with st.expander("🧠 User Memory (What I know)", expanded=False):
        memories = st.session_state.user_memory.get_all_memories()
        if memories:
            # Handle different return formats from mem0
            for mem in memories:
                if isinstance(mem, dict):
                    text = mem.get('text', str(mem))
                    st.markdown(f"- {text}")
                else:
                    st.markdown(f"- {mem}")
        else:
            st.markdown("*No memories yet.*")
    
    st.markdown("---")

    # ADMIN ONLY: Data Ingestion
    # Simple check: Only show ingestion if user is 'admin'
    if user_id.strip().lower() == "admin":
        st.markdown('<p class="sidebar-header">🛠️ Admin Control</p>', unsafe_allow_html=True)
        st.info("🔓 Admin Mode Active: You can ingest documents.")
        
        # Initialize ingestion state
        if "is_ingesting" not in st.session_state:
            st.session_state.is_ingesting = False
        
        uploaded_file = st.file_uploader(
            "Upload System Documents (Policies/Terms)", 
            type=["pdf", "docx"], 
            label_visibility="collapsed",
            disabled=st.session_state.is_ingesting
        )
        
        if uploaded_file:
            st.markdown(f"**📄 Selected:** `{uploaded_file.name}`")
            
            # Option to ingest as Global Knowledge
            is_global = st.checkbox("🌐 Ingest as Global Policy (All users can see)", value=True)
            
            if st.session_state.is_ingesting:
                st.warning("⏳ Ingestion in progress... Please wait.")
            else:
                if st.button("🚀 Ingest File", use_container_width=True):
                    st.session_state.is_ingesting = True
                    st.session_state.ingest_global = is_global # Store state
                    st.rerun()
        
        # Run ingestion if flag is set
        if st.session_state.is_ingesting and uploaded_file:
            # Determine effective user_id
            effective_user_id = st.session_state.current_user_id
            if st.session_state.get("ingest_global", False):
                effective_user_id = "GLOBAL"
                display_msg = "Global Knowledge Base"
            else:
                display_msg = f"User: {effective_user_id}"

            with st.status(f"✨ Extracting for {display_msg}...", expanded=True) as status:
                st.write("🔒 Chat is disabled during ingestion")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    st.write(f"📄 Converting document...")
                    # Pass effective_user_id to ingestion
                    result = ingest_file(tmp_path, user_id=effective_user_id, original_filename=uploaded_file.name)
                    
                    status.update(label="✅ Ingestion Complete!", state="complete", expanded=False)
                    st.session_state.is_ingesting = False
                    st.session_state.ingest_global = False # Reset
                    
                    # Force retriever update by incrementing version
                    st.session_state.data_version += 1
                    
                    st.success(f"✅ Document added to {display_msg}!")
                    st.rerun()
                    
                except Exception as e:
                    status.update(label="❌ Ingestion Failed", state="error", expanded=True)
                    st.session_state.is_ingesting = False
                    st.session_state.ingest_global = False # Reset
                    st.error(f"❌ Error: {e}")
        
        st.markdown("---")
        st.markdown('<p class="sidebar-header">🗂️ Document Management</p>', unsafe_allow_html=True)
        
        # Admin Document Management
        with st.expander("Manage Ingested Files", expanded=False):
            if st.button("🔄 Refresh List"):
                # Just rerunning to fetch fresh list
                st.rerun()
                
            docs_info = list_documents()
            
            if not docs_info:
                st.info("No documents found in database.")
            else:
                for source, info in docs_info.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        user_label = "🌐 GLOBAL" if info['user_id'] == "GLOBAL" else f"👤 {info['user_id']}"
                        st.markdown(f"**{source}**\n\n`{user_label}` • `{info['count']} chunks`")
                    with col2:
                        if st.button("🗑️", key=f"del_{source}", help=f"Delete {source}"):
                            if delete_document(source):
                                st.success(f"Deleted {source}")
                                st.session_state.data_version += 1 # Force cache update
                                st.rerun()
                            else:
                                st.error("Failed to delete")
                    st.markdown("---")

    else:
        # Regular User View
        st.markdown('<p class="sidebar-header">ℹ️ Information</p>', unsafe_allow_html=True)
        st.info("👋 Welcome! You are in Consultant Mode. You can query the system policies and guidance.")
    
    st.markdown("---")    
    st.markdown("---")
    
    # Info Card
    st.markdown("""
    <div class="info-card">
        <h4>💡 How to use</h4>
        <p>1. Enter your User ID</p>
        <p>2. Upload a PDF or DOCX file</p>
        <p>3. Click "Ingest File" to process</p>
        <p>4. Ask questions & I will learn about you!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Status Section
    st.markdown('<p class="sidebar-header">⚡ System Status</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🟢 **LLM**")
        st.markdown("🟢 **Vector DB**")
    with col2:
        st.markdown("🟢 **Memory**")
        if st.session_state.is_ingesting:
            st.markdown("🟡 **Ingesting...**")
        else:
            st.markdown("🟢 **Ready**")

# Memory Init - Fallback if not initialized
if "user_memory" not in st.session_state:
    # This might happen on first run before sidebar executes? 
    # Actually sidebar executes top-down usually, but safe to have fallback
    shared_mem_client = get_shared_memory_client()
    st.session_state.user_memory = UserMemory(user_id="user_1", memory_client=shared_mem_client)

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message when no messages
if not st.session_state.messages:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 3rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        border: 1px dashed rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
    ">
        <h2 style="color: #7b68ee; margin-bottom: 1rem;">👋 Welcome to Antigravity RAG</h2>
        <p style="color: #b0b0b0; font-size: 1.1rem;">
            Upload a document in the sidebar, then ask me anything about it!
        </p>
        <p style="color: #666; font-size: 0.9rem; margin-top: 1rem;">
            Powered by Qwen 2.5 • BGE-M3 Embeddings • Qdrant Vector Store
        </p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("💬 Ask me anything about your documents..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Retrieval - Pass current User ID and Data Version
        current_user = st.session_state.current_user_id
        retriever = get_retriever(user_id=current_user, version=st.session_state.data_version)
        relevant_docs = retriever.invoke(prompt)
        
        context_text = "\n\n".join([d.page_content for d in relevant_docs])
        
        # Memory
        mem_context = st.session_state.user_memory.get_context(prompt)
        
        # Generator
        full_response = ""
        stream = generate_response(context_text, mem_context, prompt)
        
        for chunk in stream:
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
        # Save to Memory
        st.session_state.user_memory.add_interaction(prompt, full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

