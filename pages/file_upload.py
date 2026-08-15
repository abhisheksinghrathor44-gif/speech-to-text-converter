import streamlit as st
import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import time
import os

st.title("📁 Upload Audio File Assistant")
st.write("Upload a meeting WAV file to generate text, summaries, and action items.")

if "file_transcript" not in st.session_state:
    st.session_state.file_transcript = ""
if "file_summary" not in st.session_state:
    st.session_state.file_summary = ""

uploaded_file = st.file_uploader("Choose a meeting WAV file", type=["wav"], key="file_uploader")

if uploaded_file is not None:
    st.audio(uploaded_file)
    if st.button("⚙️ Process Uploaded File", type="primary"):
        unique_filename = f"upload_audio_{int(time.time())}.wav"
        with open(unique_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with st.status("🛠️ Running Audio Pipeline...", expanded=True) as status:
            try:
                st.write("Converting speech to text...")
                recognizer = sr.Recognizer()
                with sr.AudioFile(unique_filename) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                    st.session_state.file_transcript = text
                
                st.write("Summarizing with BART...")
                model_id = "sshleifer/distilbart-cnn-12-6"
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
                
                inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
                summary_ids = model.generate(**inputs, max_length=130, min_length=15, do_sample=False)
                st.session_state.file_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                
                status.update(label="✅ Complete!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(unique_filename):
                    os.remove(unique_filename)

if st.session_state.file_transcript:
    st.divider()
    st.subheader("📝 Transcript")
    st.text_area("Transcript", st.session_state.file_transcript, height=150, disabled=True)
    st.subheader("📊 Summary")
    st.text_area("Summary", st.session_state.file_summary, height=150, disabled=True)