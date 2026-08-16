import streamlit as st
import requests

st.set_page_config(
    page_title="AI Code Review & Security Analysis Assistant",
    page_icon="🛡️",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

st.title("🛡️ AI Code Review & Security Analysis Assistant")
st.markdown("Automated Code Quality Inspection, OWASP Vulnerability Scanning & Fix Remediation")

# Sidebar - Settings & Language Selection
st.sidebar.header("Settings")
language = st.sidebar.selectbox("Select Programming Language", ["Python", "Java", "JavaScript", "C++", "Go"])

# Code Upload / Input Area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Source Code Input")
    uploaded_file = st.file_uploader("Upload Source Code File", type=["py", "java", "js", "cpp", "go"])
    
    if uploaded_file is not None:
        code_input = uploaded_file.getvalue().decode("utf-8")
    else:
        code_input = st.text_area("Or Paste Your Code Here:", height=350, value="""def login(user_input):
    api_key = "secret_1234567890"
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    return query""")

    run_button = st.button("🚀 Run Full AI Review", type="primary", use_container_width=True)

with col2:
    st.subheader("Interactive RAG Assistant")
    user_query = st.text_input("Ask a question about your code or OWASP standards:")
    if st.button("Ask Assistant"):
        if user_query and code_input:
            with st.spinner("Thinking..."):
                response = requests.post(f"{BACKEND_URL}/api/chat", json={
                    "query": user_query,
                    "code": code_input,
                    "language": language
                })
                if response.status_code == 200:
                    st.info(response.json()["reply"])
                else:
                    st.error("Error communicating with backend service.")

# Review Results Output Area
if run_button and code_input:
    with st.spinner("Agents Analyzing Code, Scanning Security Flaws & Building Fixes..."):
        try:
            res = requests.post(f"{BACKEND_URL}/api/review", json={
                "code": code_input,
                "language": language
            })
            
            if res.status_code == 200:
                data = res.json()
                
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📋 PR Summary", 
                    "🔍 Code Quality", 
                    "🚨 Security Audit", 
                    "🛠️ Suggested Remediation"
                ])
                
                with tab1:
                    st.markdown(data["pr_summary"])
                    
                with tab2:
                    st.markdown(data["analysis"])
                    
                with tab3:
                    st.markdown(data["security"])
                    
                with tab4:
                    st.markdown(data["remediation"])
            else:
                st.error("Failed to process code review request.")
        except Exception as e:
            st.error(f"Backend Server Connection Error: {e}")
