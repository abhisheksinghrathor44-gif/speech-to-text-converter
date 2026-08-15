import streamlit as st

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🚀",
    layout="centered"
)

# Define the pages using the clean filenames in your pages/ folder
pg = st.navigation([
    st.Page("pages/live_recording.py", title="Live Recording", icon="🎙️"),
    st.Page("pages/file_upload.py", title="Upload File", icon="📁")
])

pg.run()