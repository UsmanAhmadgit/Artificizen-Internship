import streamlit as st
import requests
import time
from utils.file_limits import get_max_file_size

API_BASE_URL = "http://localhost:8000"

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "current_room_id" not in st.session_state:
    st.session_state["current_room_id"] = None
if "current_room_name" not in st.session_state:
    st.session_state["current_room_name"] = None


def logout():
    st.session_state["access_token"] = None
    st.session_state["current_room_id"] = None
    st.session_state["current_room_name"] = None
    st.rerun()

def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03) 

def render_auth_page():
    st.title("AI Legal Case Workspace")
    st.subheader("Authentication")
    
    tab_login, tab_register = st.tabs(["Login", "Register"])
    
    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Log In", use_container_width=True):
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                try:
                    response = requests.post(f"{API_BASE_URL}/auth/login", data={"username": email, "password": password})
                    if response.status_code == 200:
                        st.session_state["access_token"] = response.json()["access_token"]
                        st.rerun()
                    else:
                        st.error(response.json().get("detail", "Login failed. Please check your credentials."))
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the authentication server. Please ensure the backend is running.")

    with tab_register:
        username = st.text_input("Username", max_chars=50, help="Must be between 3 and 50 characters", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", max_chars=100, help="Must be at least 6 characters long", key="reg_password")
        
        if st.button("Register", use_container_width=True):
            if not username or not email or not password:
                st.warning("All fields are required.")
            elif len(username) < 3:
                st.error("Username must be at least 3 characters long.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                payload = {"username": username, "email": email, "password": password}
                try:
                    response = requests.post(f"{API_BASE_URL}/auth/register", json=payload)
                    if response.status_code == 201:
                        st.success("Registration successful. You can now log in.")
                    else:
                        st.error(response.json().get("detail", "Registration failed."))
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the registration server. Please ensure the backend is running.")

def render_rooms_page():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Workspace Rooms")
    with col2:
        st.write("")
        if st.button("Log Out", use_container_width=True):
            logout()

    st.divider()

    with st.expander("Create a New Room"):
        with st.form("create_room_form", clear_on_submit=True):
            room_name = st.text_input("Room Name")
            room_desc = st.text_input("Description (Optional)")
            if st.form_submit_button("Create Room") and room_name.strip():
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                try:
                    res = requests.post(f"{API_BASE_URL}/rooms/", json={"name": room_name.strip(), "description": room_desc.strip()}, headers=headers)
                    if res.status_code == 201:
                        st.rerun()
                    else:
                        st.error(res.json().get("detail", "Failed to create room."))
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the server to create a room.")

    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    
    try:
        response = requests.get(f"{API_BASE_URL}/rooms/", headers=headers)
        
        if response.status_code == 200:
            rooms = response.json()
            if not rooms:
                st.info("No rooms found. Create your first room.")
            for room in rooms:
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{room['name']}**")
                    if room.get("description"):
                        st.caption(room["description"])
                with c2:
                    if st.button("Enter Room", key=f"enter_{room['id']}", use_container_width=True):
                        st.session_state["current_room_id"] = room["id"]
                        st.session_state["current_room_name"] = room["name"]
                        st.rerun()
                st.divider()
        elif response.status_code == 401:
            st.error("Session expired. Please log in again.")
            logout()
        else:
            st.error("Failed to load rooms.")
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the server to load your rooms. Please ensure the backend is running.")


def render_sources(sources):
    if not sources:
        with st.expander("Sources", expanded=False):
            st.write("No sources found")
    else:
        with st.expander(f"Sources ({len(sources)})", expanded=False):
            for src in sources:
                st.markdown(f"**{src.get('filename', 'Unknown')}** | Type: {src.get('file_type', 'Unknown')} | Chunk: {src.get('chunk_index', '0')}")
                st.caption(f"_{src.get('excerpt', 'No excerpt available')}_")
                st.divider()


def render_room_view():
    room_id = st.session_state["current_room_id"]
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}

    st.sidebar.button("Back to Rooms", on_click=lambda: st.session_state.update({"current_room_id": None, "current_room_name": None}))
    st.sidebar.title(st.session_state["current_room_name"])
    st.sidebar.divider()
    
    st.sidebar.subheader("Upload Evidence")
    uploaded_file = st.sidebar.file_uploader("Select File", label_visibility="collapsed")

    if st.sidebar.button("Upload to Room", use_container_width=True) and uploaded_file:
        max_allowed = get_max_file_size(uploaded_file.name)
        limit_mb = max_allowed // (1024 * 1024)
        
        if uploaded_file.size > max_allowed:
            st.sidebar.error(f"File too large! Max allowed limit for this format is {limit_mb}MB.")
        else:
            with st.sidebar.spinner("Processing file..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    res = requests.post(f"{API_BASE_URL}/upload/{room_id}", files=files, headers=headers)
                    
                    if res.status_code == 200:
                        st.sidebar.success("Upload complete!")
                        time.sleep(1)  
                        st.rerun()
                    elif res.status_code == 413:
                        error_detail = res.json().get("detail", f"File exceeds {limit_mb}MB limit.")
                        st.sidebar.error(f"Upload Error: {error_detail}")
                    else:
                        error_detail = res.json().get("detail", "Upload failed.")
                        st.sidebar.error(f"Failed: {error_detail}")
                        
                except requests.exceptions.ConnectionError:
                    st.sidebar.error("Backend server is offline.")
                
    st.sidebar.divider()
    st.sidebar.subheader("Room Files")
    
    try:
        file_res = requests.get(f"{API_BASE_URL}/upload/{room_id}", headers=headers)
        if file_res.status_code == 200:
            files = file_res.json()
            if not files:
                st.sidebar.caption("No files uploaded yet.")
            for f in files:
                col1, col2 = st.sidebar.columns([4, 1])
                with col1:
                    if f['status'] == 'ready':
                        status_badge = ":green[[READY]]"
                    elif f['status'] == 'processing':
                        status_badge = ":orange[[PROCESSING]]"
                    else:
                        status_badge = ":red[[FAILED]]"
                        
                    st.markdown(f"**{f['filename']}**\n{status_badge}")
                with col2:
                    if st.button("X", key=f"del_{f['id']}", help="Delete File"):
                        requests.delete(f"{API_BASE_URL}/upload/{room_id}/{f['id']}", headers=headers)
                        st.rerun()
    except requests.exceptions.ConnectionError:
        st.sidebar.error("Cannot connect to server to load files.")

    st.title("Workspace Chat")
    
    limit_key = f"chat_limit_{room_id}"
    if limit_key not in st.session_state:
        st.session_state[limit_key] = 50
    
    try:
        current_limit = st.session_state[limit_key]
        history_res = requests.get(f"{API_BASE_URL}/chat/{room_id}/history?limit={current_limit}", headers=headers)
        
        if history_res.status_code == 200:
            chat_history = history_res.json()
            
            if len(chat_history) >= current_limit:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("⬆️ Load older messages", use_container_width=True):
                        st.session_state[limit_key] += 50
                        st.rerun()

            for msg in chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg["role"] == "assistant":
                        render_sources(msg.get("sources", []))
                        
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server to load chat history. Please ensure the backend is running.")
    
    if prompt := st.chat_input("Ask a question about the room's documents...", max_chars=2000):
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing context..."):
                try:
                    chat_res = requests.post(f"{API_BASE_URL}/chat/{room_id}", json={"query": prompt}, headers=headers)
                    if chat_res.status_code == 200:
                        result = chat_res.json()
                        st.write_stream(stream_text(result["answer"]))
                        render_sources(result.get("sources", []))
                    else:
                        st.error("Failed to get response from server.")
                except requests.exceptions.ConnectionError:
                    st.error("Connection lost. Cannot send message to the backend server.")
def main():
    st.set_page_config(page_title="Legal Workspace", layout="wide")

    if not st.session_state["access_token"]:
        render_auth_page()
    elif st.session_state["current_room_id"] is None:
        render_rooms_page()
    else:
        render_room_view()


if __name__ == "__main__":
    main()