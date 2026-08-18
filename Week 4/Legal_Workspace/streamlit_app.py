import streamlit as st
import requests
import time
from utils.file_limits import get_max_file_size

API_BASE_URL = ""

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "username" not in st.session_state:
    st.session_state["username"] = "User"
if "current_room_id" not in st.session_state:
    st.session_state["current_room_id"] = None
if "current_room_name" not in st.session_state:
    st.session_state["current_room_name"] = None


def logout():
    st.session_state["access_token"] = None
    st.session_state["current_room_id"] = None
    st.session_state["current_room_name"] = None
    st.session_state["username"] = "User"
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
                        data = response.json()
                        st.session_state["access_token"] = data["access_token"]
                        st.session_state["username"] = data.get("username", "User")
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
        st.title(f"Welcome, {st.session_state.get('username', 'User')} !")
        st.subheader("Your Workspace Rooms")
    with col2:
        st.write("")
        if st.button("Log Out", use_container_width=True):
            logout()

    st.divider()

    st.info(
        "**Welcome to your AI Legal Case Workspace!**\n\n"
        "Here you can create dedicated **Rooms** for each of your legal cases. "
        "Give your room a descriptive name (descriptions are optional). "
        "Inside a room, you can upload evidence files (documents, images, audio, video) "
        "and chat securely with an AI that specifically references those case files."
    )

    with st.expander("➕ Create a New Room"):
        with st.form("create_room_form", clear_on_submit=True):
            room_name = st.text_input("Room Name")
            room_desc = st.text_input("Description (Optional)")
            if st.form_submit_button("Create Room") and room_name.strip():
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/rooms/", 
                        json={"name": room_name.strip(), "description": room_desc.strip()}, 
                        headers=headers
                    )
                    if res.status_code == 201:
                        st.success("Room created successfully!")
                        time.sleep(0.5)
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
                st.info("No rooms found. Create your first room above.")
            
            for room in rooms:
                c1, c2, c3, c4 = st.columns([3.5, 1.5, 1, 1])
                
                with c1:
                    st.markdown(f"**{room['name']}**")
                    if room.get("description"):
                        st.caption(room["description"])
                
                with c2:
                    if st.button("Enter Room", key=f"enter_{room['id']}", use_container_width=True, type="primary"):
                        st.session_state["current_room_id"] = room["id"]
                        st.session_state["current_room_name"] = room["name"]
                        st.rerun()

                with c3:
                    with st.popover("✏️ Edit", use_container_width=True):
                        st.subheader("Edit Room")
                        with st.form(key=f"edit_form_{room['id']}"):
                            new_name = st.text_input("Room Name", value=room['name'])
                            new_desc = st.text_input("Description", value=room.get('description') or "")
                            
                            if st.form_submit_button("Save Changes"):
                                if not new_name.strip():
                                    st.error("Room name cannot be empty.")
                                else:
                                    try:
                                        update_payload = {
                                            "name": new_name.strip(),
                                            "description": new_desc.strip() if new_desc.strip() else None
                                        }
                                        res = requests.put(
                                            f"{API_BASE_URL}/rooms/{room['id']}", 
                                            json=update_payload, 
                                            headers=headers
                                        )
                                        if res.status_code == 200:
                                            st.success("Room updated!")
                                            time.sleep(0.5)
                                            st.rerun()
                                        else:
                                            st.error(res.json().get("detail", "Failed to update room."))
                                    except requests.exceptions.ConnectionError:
                                        st.error("Server offline.")

                with c4:
                    with st.popover("🗑️ Delete", use_container_width=True):
                        st.markdown("**Confirm Deletion**")
                        st.caption(f"Are you sure you want to delete **{room['name']}**? All files and messages in this room will be removed.")
                        if st.button("Confirm Delete", key=f"confirm_del_{room['id']}", type="primary", use_container_width=True):
                            try:
                                res = requests.delete(f"{API_BASE_URL}/rooms/{room['id']}", headers=headers)
                                if res.status_code == 204:
                                    if st.session_state.get("current_room_id") == room["id"]:
                                        st.session_state["current_room_id"] = None
                                        st.session_state["current_room_name"] = None
                                    st.success("Room deleted.")
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    try:
                                        error_msg = res.json().get("detail", "Failed to delete room.")
                                    except:
                                        error_msg = f"Server error ({res.status_code}). Failed to delete room."
                                    st.error(error_msg)
                            except requests.exceptions.ConnectionError:
                                st.error("Server offline.")

                st.divider()

        elif response.status_code == 401:
            st.error("Session expired. Please log in again.")
            logout()
        else:
            st.error("Failed to load rooms.")
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the server to load your rooms. Please ensure the backend is running.")

    st.write("") 
    with st.expander("⚠️ Account Settings"):
        st.warning("Deleting your account is permanent. All your rooms, files, and chat history will be completely erased.")
        if st.checkbox("I understand, I want to delete my account"):
            if st.button("Delete Account Permanently", type="primary"):
                try:
                    del_res = requests.delete(f"{API_BASE_URL}/auth/account", headers=headers)
                    if del_res.status_code == 204:
                        st.success("Account deleted successfully. Logging you out...")
                        time.sleep(1.5)
                        logout()
                    else:
                        try:
                            error_msg = del_res.json().get("detail", "Failed to delete account.")
                        except:
                            error_msg = f"Server error ({del_res.status_code}). Failed to delete account."
                        st.error(error_msg)
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the server to delete account.")

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


@st.dialog("📖 Workspace Instructions")
def instruction_modal():
    st.markdown("""
    ### 📂 Uploading Evidence
    Upload files to build the context for your case. The AI processes these files so you can chat with them.
    
    **Supported File Types & Behaviors:**
    *   📄 **Documents (PDF, DOCX, PPTX) — Limit: 20 MB**
        *   The system extracts text, paragraphs, and tables. 
        *   *Bonus:* If there are pictures inside the documents, any text inside those pictures will also be automatically extracted!
    *   🖼️ **Images (PNG, JPG, JPEG, WEBP) — Limit: 10 MB**
        *   Upload single images (like scanned letters or screenshots). The text inside them is automatically scanned and used as context.
    *   🎥 **Videos (MP4, MKV, MOV, AVI, WEBM) — Limit: 200 MB**
        *   To save space, only the audio track is extracted. It is then transcribed into text and stored as context.
    *   🎵 **Audio (MP3, WAV, M4A, AAC, FLAC) — Limit: 30 MB**
        *   Speech is automatically transcribed and stored as context.
    *   📝 **Text Data (TXT, MD, CSV) — Limit: 5 MB**
        *   Standard text files are read directly.

    ---
    ### 💬 Chatting with the AI
    Ask specific questions about your uploaded case files. 
    *   **Verify Answers:** Below every AI response, look for the collapsible **"Sources"** window. Click it to view the exact files and text snippets the AI used to generate its answer!
    """)


def render_room_view():
    room_id = st.session_state["current_room_id"]
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}

    st.sidebar.button("Back to Rooms", on_click=lambda: st.session_state.update({"current_room_id": None, "current_room_name": None}))
    st.sidebar.title(st.session_state["current_room_name"])
    st.sidebar.divider()
    if st.sidebar.button("📖 View Instructions", use_container_width=True):
        instruction_modal()
    
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
                        del_req = requests.delete(f"{API_BASE_URL}/upload/{room_id}/{f['id']}", headers=headers)
                        if del_req.status_code == 200:
                            st.rerun()
                        else:
                            st.sidebar.error("Failed to delete file.")
        else:
            st.sidebar.error("Failed to fetch room files.")
    except requests.exceptions.ConnectionError:
        st.sidebar.error("Cannot connect to server to load files.")

    st.sidebar.divider()
    with st.sidebar.expander("⚠️ Room Settings"):
        st.caption("Clearing history removes all messages for everyone in this room.")
        if st.checkbox("Confirm clear history"):
            if st.button("🗑️ Clear Chat", type="primary", use_container_width=True):
                try:
                    res = requests.delete(f"{API_BASE_URL}/chat/{room_id}/history", headers=headers)
                    if res.status_code == 200:
                        st.session_state[f"chat_limit_{room_id}"] = 50  
                        st.rerun()
                    else:
                        st.error(res.json().get("detail", "Failed to clear history."))
                except requests.exceptions.ConnectionError:
                    st.error("Server offline.")

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
                _, col2, _ = st.columns([1, 2, 1])
                with col2:
                    if st.button("⬆️ Load older messages", use_container_width=True):
                        st.session_state[limit_key] += 50
                        st.rerun()

            for msg in chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg["role"] == "assistant":
                        render_sources(msg.get("sources", []))
        else:
            st.error("Failed to load chat history.")
                        
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