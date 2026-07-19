import streamlit as st
import requests

st.set_page_config(
    page_title="Multi-Agent AI Support Hub", 
    page_icon="🤖", 
    layout="wide"
)

# --- SIMULATED USER AUTHENTICATION (Module 1) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Multi-Agent AI Support Portal Login")
    st.caption("Please sign in with your enterprise credentials to access the agent cluster.")
    
    with st.form("login_form"):
        username = st.text_input("Username / Email", value="testuser@example.com")
        password = st.text_input("Password", type="password", value="password123")
        submit_btn = st.form_submit_button("Authenticate Session", type="primary")
        
        if submit_btn:
            if username == "testuser@example.com" and password == "password123":
                st.session_state.authenticated = True
                st.success("Session secured. Initializing agent cluster...")
                st.rerun()
            else:
                st.error("Invalid credentials. Access Denied.")
    st.stop() # Prevents the rest of the dashboard from rendering until logged in
    
# Custom Styling for modern elements
st.markdown("""
<style>
    .agent-badge {
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        margin: 4px;
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CLEAN & BALANCED ---
with st.sidebar:
    st.title("🛡️ Core Controls")
    st.markdown("---")
    
    st.markdown("### 📡 System Integrity")
    st.success("✔ Vector Store Index")
    st.success("✔ FastAPI Middleware")
    st.success("✔ Gemini Core Core Engine")
    
    st.markdown("---")
    if st.button("🔄 Clear Chat Data", type="primary", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# --- MAIN INTERFACE HEADER ---
st.title("🤖 Multi-Agent AI Customer Support Hub")
st.caption("Enterprise RAG Pipeline with Intent Classifiers & Dynamic Context Engines")

# Active Agent Infrastructure Display Grid (Mimicking your friend's system tags)
# Active Agent Infrastructure Display Grid (Mimicking your friend's system tags)
st.markdown("### 🌐 Specialized Cluster Nodes")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="agent-badge" style="background-color: rgba(46, 204, 113, 0.15); color: #2ecc71;">💰 Billing Agent: Ready</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="agent-badge" style="background-color: rgba(230, 126, 34, 0.15); color: #e67e22;">🛠️ Technical Agent: Ready</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="agent-badge" style="background-color: rgba(231, 76, 60, 0.15); color: #e74c3c;">🚨 Complaint Agent: Ready</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="agent-badge" style="background-color: rgba(52, 152, 219, 0.15); color: #3498db;">ℹ️ Policy Agent: Active</div>', unsafe_allow_html=True)

# Session state memory configuration
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- CONVERSATION STARTERS (If chat is empty) ---
if not st.session_state.chat_history:
    st.markdown("#### 💡 Quick Test Scenarios")
    scol1, scol2 = st.columns(2)
    with scol1:
        if st.button("👉 Test Billing: 'I was charged twice this month'", use_container_width=True):
            st.session_state.preset_query = "I was charged twice this month"
    with scol2:
        if st.button("👉 Test Policy: 'Can I get a full refund within 30 days?'", use_container_width=True):
            st.session_state.preset_query = "Can I get a full refund within 30 days?"

# Handle preset suggestions clicks injection
if "preset_query" in st.session_state and st.session_state.preset_query:
    user_query = st.session_state.preset_query
    del st.session_state.preset_query
else:
    user_query = st.chat_input("Type your support or policy inquiry here...")

# --- RENDER CHAT STREAM ---
for msg in st.session_state.chat_history:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# --- PROCESS INCOMING EXECUTION ---
if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.write(user_query)

    formatted_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[:-1]]

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Invoking router routing maps..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/chat",
                    json={"message": user_query},
                    timeout=70
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["response"]       
                    agent_name = data["routed_agent"] 
                    
                    # Modern alert tags based on routing context
                    if "Billing" in agent_name:
                        st.success(f"💰 **System Router:** Successfully routed to `{agent_name}`")
                    elif "Technical" in agent_name:
                        st.warning(f"🛠️ **System Router:** Successfully routed to `{agent_name}`")
                    elif "Complaint" in agent_name:
                        st.error(f"🚨 **System Router:** Successfully routed to `{agent_name}`")
                    else:
                        st.info(f"ℹ️ **System Router:** Successfully routed to `{agent_name}`")
                        
                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()
                else:
                    st.error(f"API Error {response.status_code}: Communication drop.")
            
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Refused: Ensure your backend FastAPI application is live.")
            except Exception as e:
                st.error(f"Exception: {str(e)}")