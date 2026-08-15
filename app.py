import streamlit as st

st.set_page_config(
    page_title="AI Speech To Text",
    page_icon="🚀",
    layout="centered"
)

# Define the pages in your app
pg = st.navigation([
    st.Page("pages/1_🎙️_Live_Recording.py", title="Live Recording", icon="🎙️"),
    st.Page("pages/2_📁_File_Upload.py", title="Upload Audio File", icon="📁")
])

# Run the selected page
pg.run()